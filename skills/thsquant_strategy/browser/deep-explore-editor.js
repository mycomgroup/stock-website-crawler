#!/usr/bin/env node
/**
 * THSQuant 编辑器页面深度探索
 * 解决 iframe 或动态加载问题
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function deepExploreEditor() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 编辑器深度探索');
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
        const endpoint = url.split('/platform/')[1]?.split('?')[0] || url;
        console.log(`\n[${apiCalls.length}] POST ${endpoint}`);

        if (postData.length < 500) {
          const params = new URLSearchParams(postData);
          const important = {};
          for (const [k, v] of params) {
            if (!['isajax', 'datatype', 'callback'].includes(k)) {
              important[k] = v.length > 80 ? v.slice(0, 80) + '...' : v;
            }
          }
          if (Object.keys(important).length > 0) {
            console.log('  参数:', JSON.stringify(important));
          }
        }
      }
    }
  });

  // 监听响应
  page.on('response', async response => {
    const url = response.url();
    const call = apiCalls.find(c => c.url === url && !c.status);

    if (call) {
      call.status = response.status();
      try {
        const text = await response.text();
        const match = text.match(/\((.+)\)/s);
        if (match) {
          try {
            call.responseJson = JSON.parse(match[1]);
            if (call.responseJson.errorcode !== undefined) {
              console.log(`  响应: errorcode=${call.responseJson.errorcode}`);
            }
          } catch (e) {}
        }
      } catch (e) {}
    }
  });

  try {
    // 1. 打开主页面
    console.log('\n打开策略研究主页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    await page.waitForTimeout(3000);

    // 2. 检查是否有 iframe
    console.log('\n检查 iframe...');
    const frames = page.frames();
    console.log(`发现 ${frames.length} 个 frame`);

    // 分析主页面内容
    const mainPageInfo = await page.evaluate(() => {
      // 查找所有 iframe
      const iframes = document.querySelectorAll('iframe');
      const iframeInfo = Array.from(iframes).map(f => ({
        src: f.src,
        id: f.id,
        className: f.className
      }));

      // 查找策略列表项
      const strategyItems = document.querySelectorAll('tr, .strategy-item, [class*="algo"]');
      const items = Array.from(strategyItems).slice(0, 5).map(el => ({
        text: el.textContent?.trim().slice(0, 50),
        className: el.className?.slice(0, 30)
      }));

      // 查找新建按钮
      const newButtons = Array.from(document.querySelectorAll('button, a, [class*="new"], [class*="create"]'))
        .filter(el => {
          const text = el.textContent || '';
          return text.includes('新建') || text.includes('创建') || text.includes('new');
        })
        .map(el => ({
          text: el.textContent?.trim().slice(0, 20),
          className: el.className?.slice(0, 30)
        }));

      return { iframeInfo, items, newButtons };
    });

    console.log('\niframe 信息:', mainPageInfo.iframeInfo);
    console.log('策略项:', mainPageInfo.items.length);
    console.log('新建按钮:', mainPageInfo.newButtons);

    // 3. 尝试点击策略项进入编辑
    console.log('\n尝试进入策略编辑...');

    // 查找并点击第一个策略
    const strategyRow = await page.$('tr[class*="strategy"], .strategy-row, tbody tr');
    if (strategyRow) {
      console.log('找到策略行，双击进入编辑...');
      await strategyRow.dblclick();
      await page.waitForTimeout(5000);
    } else {
      console.log('未找到策略行，尝试直接打开编辑器 URL...');

      // 直接打开编辑器页面
      await page.goto('https://quant.10jqka.com.cn/platform/study/html/editor.html?algo_id=67c935e607887b957629ad72', {
        waitUntil: 'networkidle',
        timeout: 60000
      });

      await page.waitForTimeout(10000);
    }

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'editor-state.png'), fullPage: true });

    // 4. 深度分析编辑器页面
    console.log('\n深度分析编辑器页面...');

    // 检查所有 frames
    const allFrames = page.frames();
    for (let i = 0; i < allFrames.length; i++) {
      const frame = allFrames[i];
      console.log(`\nFrame ${i}: ${frame.url()}`);

      try {
        const frameContent = await frame.evaluate(() => {
          // 查找按钮
          const buttons = Array.from(document.querySelectorAll('button, a, input[type="button"], [role="button"]'))
            .slice(0, 20)
            .map(el => ({
              text: (el.textContent || el.value || '').trim().slice(0, 30),
              tag: el.tagName,
              className: el.className?.toString().slice(0, 40),
              id: el.id
            }))
            .filter(b => b.text);

          // 查找输入框
          const inputs = Array.from(document.querySelectorAll('input, select, textarea'))
            .map(el => ({
              name: el.name,
              id: el.id,
              type: el.type,
              placeholder: el.placeholder,
              value: (el.value || '').slice(0, 30)
            }))
            .filter(i => i.name || i.id);

          // 查找回测相关元素
          const backtestBtns = Array.from(document.querySelectorAll('*'))
            .filter(el => {
              const text = (el.textContent || '').toLowerCase();
              const cls = (el.className || '').toString().toLowerCase();
              return text.includes('回测') || text.includes('运行') ||
                     cls.includes('backtest') || cls.includes('run');
            })
            .slice(0, 5)
            .map(el => ({
              text: el.textContent?.trim().slice(0, 30),
              tag: el.tagName,
              className: el.className?.toString().slice(0, 40)
            }));

          return { buttons, inputs, backtestBtns };
        });

        console.log(`  按钮 (${frameContent.buttons.length}):`);
        frameContent.buttons.forEach(b => {
          console.log(`    ${b.tag}: "${b.text}" class="${b.className}"`);
        });

        console.log(`  输入框 (${frameContent.inputs.length}):`);
        frameContent.inputs.forEach(i => {
          console.log(`    ${i.type}: name="${i.name}" value="${i.value}"`);
        });

        console.log(`  回测按钮 (${frameContent.backtestBtns.length}):`);
        frameContent.backtestBtns.forEach(b => {
          console.log(`    ${b.tag}: "${b.text}" class="${b.className}"`);
        });

        // 如果找到回测按钮，尝试点击
        if (frameContent.backtestBtns.length > 0) {
          console.log('\n尝试点击回测按钮...');

          for (const btn of frameContent.backtestBtns) {
            try {
              // 在 frame 中查找并点击
              const locator = frame.locator(`text="${btn.text}"`).first();
              if (await locator.isVisible()) {
                console.log(`点击: "${btn.text}"`);
                await locator.click();
                await page.waitForTimeout(5000);
                break;
              }
            } catch (e) {
              continue;
            }
          }
        }

      } catch (e) {
        console.log(`  无法访问 frame: ${e.message}`);
      }
    }

    // 5. 保持浏览器打开
    console.log('\n浏览器保持打开 30 秒...');
    await page.waitForTimeout(30000);

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

    console.log(`\n总请求: ${apiCalls.length}`);
    console.log(`回测相关: ${backtestApis.length}`);

    if (backtestApis.length > 0) {
      console.log('\n回测 API 详情:');
      backtestApis.forEach(api => {
        console.log(`\n  URL: ${api.url}`);
        console.log(`  参数: ${api.postData}`);
        if (api.responseJson) {
          console.log(`  响应: ${JSON.stringify(api.responseJson).slice(0, 200)}`);
        }
      });
    }

    // 保存结果
    const result = {
      totalCalls: apiCalls.length,
      backtestApis,
      allCalls: apiCalls,
      timestamp: Date.now()
    };

    fs.writeFileSync(path.join(OUTPUT_ROOT, 'deep-explore-result.json'), JSON.stringify(result, null, 2));

    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'deep-explore-error.png') });
    await browser.close();
    throw error;
  }
}

deepExploreEditor().catch(console.error);