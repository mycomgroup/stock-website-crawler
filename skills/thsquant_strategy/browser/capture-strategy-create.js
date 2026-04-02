#!/usr/bin/env node
/**
 * THSQuant 策略创建流程捕获
 * 从主页点击新建策略，捕获完整的创建和回测流程
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureStrategyCreate() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 策略创建流程捕获');
  console.log('='.repeat(70));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const apiCalls = [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 监听所有请求
  const capturedRequests = new Map();

  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    const postData = request.postData() || '';

    const key = `${method} ${url.split('?')[0]}`;
    if (!capturedRequests.has(key)) {
      capturedRequests.set(key, {
        url,
        method,
        postData,
        time: Date.now(),
        count: 0
      });
    }
    capturedRequests.get(key).count++;

    if (method === 'POST') {
      apiCalls.push({
        id: apiCalls.length,
        url,
        method,
        postData,
        time: Date.now()
      });

      if (url.includes('/platform/')) {
        const endpoint = url.split('/platform/')[1]?.split('/')[0] || url;
        console.log(`\n[${apiCalls.length}] POST /${endpoint}`);

        // 解析参数
        try {
          const params = new URLSearchParams(postData);
          const important = {};
          for (const [k, v] of params) {
            if (!['isajax', 'datatype', 'callback'].includes(k)) {
              important[k] = v.length > 100 ? v.slice(0, 100) + '...' : v;
            }
          }
          if (Object.keys(important).length > 0) {
            console.log('  参数:', JSON.stringify(important));
          }
        } catch (e) {
          if (postData.length < 300) {
            console.log('  Body:', postData);
          }
        }
      }
    }
  });

  // 监听响应
  page.on('response', async response => {
    const url = response.url();
    const req = response.request();

    if (req.method() === 'POST') {
      const call = apiCalls.find(c => c.url === url && !c.status);

      if (call) {
        call.status = response.status();
        try {
          const text = await response.text();
          const match = text.match(/\((.+)\)/s);
          if (match) {
            try {
              call.responseJson = JSON.parse(match[1]);
              const json = call.responseJson;

              if (json.errorcode !== undefined) {
                console.log(`  响应: errorcode=${json.errorcode}`);

                if (json.errormsg) {
                  console.log(`  消息: ${json.errormsg}`);
                }

                // 显示重要的 result 字段
                if (json.result) {
                  if (typeof json.result === 'object') {
                    const keys = Object.keys(json.result).slice(0, 8);
                    console.log(`  result keys: ${keys.join(', ')}`);
                  } else if (typeof json.result === 'string') {
                    console.log(`  result: ${json.result.slice(0, 50)}`);
                  }
                }
              }
            } catch (e) {}
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 1. 打开策略研究主页
    console.log('\n步骤1: 打开策略研究主页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'main-page.png') });

    // 2. 获取页面结构
    console.log('\n步骤2: 分析页面结构...');
    const pageStructure = await page.evaluate(() => {
      // 获取新建按钮
      const newBtns = Array.from(document.querySelectorAll('.new_btn, button, a'))
        .filter(el => {
          const text = el.textContent || '';
          return text.includes('新建') || text.includes('创建');
        })
        .map(el => ({
          text: el.textContent?.trim(),
          className: el.className?.slice(0, 50),
          id: el.id
        }));

      // 获取策略列表
      const strategyList = document.querySelector('.strategy-list, tbody, .list-container');
      const strategies = strategyList ?
        Array.from(strategyList.querySelectorAll('tr, .item, .strategy-item')).slice(0, 5)
          .map(el => ({
            text: el.textContent?.trim().slice(0, 100),
            className: el.className?.slice(0, 30)
          })) : [];

      // 查找策略链接
      const strategyLinks = Array.from(document.querySelectorAll('a[href*="algo"]'))
        .slice(0, 5)
        .map(a => ({
          href: a.href,
          text: a.textContent?.trim().slice(0, 30)
        }));

      return { newBtns, strategies, strategyLinks };
    });

    console.log('\n新建按钮:', pageStructure.newBtns);
    console.log('策略项数量:', pageStructure.strategies.length);
    console.log('策略链接:', pageStructure.strategyLinks);

    // 3. 点击新建策略
    console.log('\n步骤3: 点击新建策略...');

    const newStrategyBtn = await page.$('.new_btn-newstrategy, button:has-text("新建策略")');

    if (newStrategyBtn) {
      console.log('找到新建策略按钮，点击...');
      await newStrategyBtn.click();
      await page.waitForTimeout(5000);

      await page.screenshot({ path: path.join(OUTPUT_ROOT, 'after-new-click.png') });

      // 检查是否打开了新窗口或跳转
      const currentUrl = page.url();
      console.log('当前 URL:', currentUrl);

    } else {
      console.log('未找到新建策略按钮');

      // 尝试点击已有的策略进行编辑
      if (pageStructure.strategyLinks.length > 0) {
        console.log('点击第一个策略链接...');
        await page.click('a[href*="algo"]');
        await page.waitForTimeout(5000);
      }
    }

    // 4. 等待并收集更多请求
    console.log('\n步骤4: 等待页面加载...');
    await page.waitForTimeout(10000);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'final-page.png'), fullPage: true });

    // 5. 尝试找到并点击运行/回测按钮
    console.log('\n步骤5: 查找回测按钮...');

    // 在所有 frames 中查找
    const allFrames = page.frames();
    console.log(`检查 ${allFrames.length} 个 frame`);

    for (const frame of allFrames) {
      try {
        const buttons = await frame.evaluate(() => {
          return Array.from(document.querySelectorAll('button, a, [role="button"]'))
            .map(el => ({
              text: el.textContent?.trim().slice(0, 30),
              className: el.className?.slice(0, 40),
              id: el.id
            }))
            .filter(b => b.text);
        });

        if (buttons.length > 0) {
          console.log(`\nFrame ${frame.url().slice(0, 50)}: ${buttons.length} 个按钮`);
          buttons.forEach(b => console.log(`  "${b.text}" class="${b.className}"`));
        }
      } catch (e) {}
    }

    // 6. 保持浏览器打开让用户手动操作
    console.log('\n' + '='.repeat(70));
    console.log('请手动在浏览器中操作:');
    console.log('  1. 创建新策略或选择已有策略');
    console.log('  2. 输入策略代码');
    console.log('  3. 设置回测参数');
    console.log('  4. 点击运行回测');
    console.log('='.repeat(70));

    console.log('\n脚本将持续监听 API 调用 60 秒...');
    await page.waitForTimeout(60000);

    // 保存 session
    const newCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: newCookies,
      timestamp: Date.now()
    }, null, 2));

    await browser.close();

    // 分析结果
    console.log('\n' + '='.repeat(70));
    console.log('分析捕获结果');
    console.log('='.repeat(70));

    const backtestApis = apiCalls.filter(c =>
      c.url.includes('backtest') ||
      c.url.includes('run') ||
      (c.postData && (c.postData.includes('backtest') || c.postData.includes('run')))
    );

    const algoApis = apiCalls.filter(c =>
      c.url.includes('algo') || c.url.includes('algorithm')
    );

    const createApis = apiCalls.filter(c =>
      c.url.includes('add') || c.url.includes('create') ||
      (c.postData && (c.postData.includes('add') || c.postData.includes('create')))
    );

    console.log(`\n总 POST 请求: ${apiCalls.length}`);
    console.log(`回测相关: ${backtestApis.length}`);
    console.log(`策略相关: ${algoApis.length}`);
    console.log(`创建相关: ${createApis.length}`);

    // 保存详细结果
    const result = {
      totalCalls: apiCalls.length,
      backtestApis,
      algoApis,
      createApis,
      allCalls: apiCalls,
      timestamp: Date.now()
    };

    const outputPath = path.join(OUTPUT_ROOT, 'strategy-create-capture.json');
    fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
    console.log(`\n保存到: ${outputPath}`);

    // 打印重要 API
    if (backtestApis.length > 0) {
      console.log('\n★ 回测 API:');
      backtestApis.forEach(api => {
        console.log(`\n  URL: ${api.url}`);
        console.log(`  参数: ${api.postData}`);
      });
    }

    if (createApis.length > 0) {
      console.log('\n★ 创建 API:');
      createApis.forEach(api => {
        console.log(`\n  URL: ${api.url}`);
        console.log(`  参数: ${api.postData}`);
      });
    }

    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'capture-error.png') });

    // 保存已捕获的数据
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'capture-error-log.json'),
      JSON.stringify({ error: error.message, apiCalls }, null, 2));

    await browser.close();
    throw error;
  }
}

captureStrategyCreate().catch(console.error);