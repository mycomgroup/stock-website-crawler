#!/usr/bin/env node
/**
 * 点击策略进入编辑并捕获回测 API
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function clickStrategyAndCapture() {
  console.log('\n' + '='.repeat(70));
  console.log('点击策略并捕获回测 API');
  console.log('='.repeat(70));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const apiCalls = [];

  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 监听请求
  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    const postData = request.postData() || '';

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
        } catch (e) {}
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
              }
            } catch (e) {}
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 1. 打开主页
    console.log('\n步骤1: 打开主页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    await page.waitForTimeout(3000);

    // 2. 点击第一个策略名称
    console.log('\n步骤2: 点击第一个策略...');

    // 策略名称作为链接
    const strategyName = 'PSY交易策略';
    const strategyLocator = page.locator(`text="${strategyName}"`).first();

    if (await strategyLocator.isVisible()) {
      console.log(`点击策略: "${strategyName}"`);
      await strategyLocator.click();
      await page.waitForTimeout(8000);
    } else {
      console.log('未找到策略链接，尝试其他方式...');

      // 查找所有包含策略名的元素
      const allText = await page.evaluate(() => {
        const links = document.querySelectorAll('a, span, div');
        return Array.from(links).map(el => el.textContent?.trim()).filter(t => t && t.length < 30).slice(0, 30);
      });
      console.log('页面文本:', allText);
    }

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'after-strategy-click.png'), fullPage: true });

    // 检查当前 URL
    console.log('当前 URL:', page.url());

    // 3. 分析页面
    console.log('\n步骤3: 分析当前页面...');
    const currentInfo = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]'))
        .filter(el => el.textContent?.trim())
        .slice(0, 20)
        .map(el => ({
          text: el.textContent?.trim().slice(0, 30),
          className: el.className?.slice(0, 40)
        }));

      // 查找回测/运行按钮
      const backtestBtns = buttons.filter(b =>
        b.text.includes('回测') || b.text.includes('运行') ||
        b.text.includes('测试') || b.text.includes('保存')
      );

      return { buttons, backtestBtns };
    });

    console.log('回测相关按钮:', currentInfo.backtestBtns);

    // 4. 尝试点击回测按钮
    if (currentInfo.backtestBtns.length > 0) {
      console.log('\n步骤4: 点击回测按钮...');

      for (const btn of currentInfo.backtestBtns) {
        try {
          const locator = page.locator(`text="${btn.text}"`).first();
          if (await locator.isVisible()) {
            console.log(`点击: "${btn.text}"`);
            await locator.click();
            await page.waitForTimeout(5000);
            break;
          }
        } catch (e) {}
      }
    }

    // 截图最终状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'final-backtest-state.png'), fullPage: true });

    // 5. 等待用户操作
    console.log('\n请手动操作浏览器...');
    console.log('脚本将监听 45 秒');
    await page.waitForTimeout(45000);

    // 保存 session
    const newCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: newCookies,
      timestamp: Date.now()
    }, null, 2));

    await browser.close();

    // 分析结果
    console.log('\n' + '='.repeat(70));
    console.log('捕获结果');
    console.log('='.repeat(70));

    const backtestApis = apiCalls.filter(c =>
      c.url.includes('backtest') ||
      c.url.includes('run') ||
      (c.postData && (c.postData.includes('backtest') || c.postData.includes('run')))
    );

    const algoApis = apiCalls.filter(c =>
      c.url.includes('algo') || c.url.includes('algorithm')
    );

    const editApis = apiCalls.filter(c =>
      c.url.includes('edit') || c.url.includes('save') ||
      (c.postData && (c.postData.includes('edit') || c.postData.includes('save')))
    );

    console.log(`\n总 POST 请求: ${apiCalls.length}`);
    console.log(`回测相关: ${backtestApis.length}`);
    console.log(`策略相关: ${algoApis.length}`);
    console.log(`编辑相关: ${editApis.length}`);

    // 打印重要 API
    [...backtestApis, ...editApis].forEach(api => {
      console.log(`\n★ ${api.url}`);
      console.log(`  参数: ${api.postData}`);
      if (api.responseJson) {
        console.log(`  响应: ${JSON.stringify(api.responseJson).slice(0, 200)}`);
      }
    });

    // 保存结果
    const result = {
      totalCalls: apiCalls.length,
      backtestApis,
      algoApis,
      editApis,
      allCalls: apiCalls,
      timestamp: Date.now()
    };

    fs.writeFileSync(path.join(OUTPUT_ROOT, 'strategy-click-capture.json'), JSON.stringify(result, null, 2));

    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'click-error.png') });
    await browser.close();
    throw error;
  }
}

clickStrategyAndCapture().catch(console.error);