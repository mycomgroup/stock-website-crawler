#!/usr/bin/env node
/**
 * 捕获回测 API 的真实参数
 * 通过浏览器监听网络请求，获取运行回测时的完整参数
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureBacktestAPI() {
  console.log('\n' + '='.repeat(70));
  console.log('捕获回测 API 真实参数');
  console.log('='.repeat(70));

  // 加载 session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 收集 API 调用
  const apiCalls = [];

  // 监听所有请求
  page.on('request', request => {
    const url = request.url();
    if (url.includes('/platform/') && request.method() === 'POST') {
      const postData = request.postData();
      apiCalls.push({
        url,
        method: request.method(),
        postData,
        headers: request.headers(),
        time: Date.now()
      });
      console.log(`\n捕获请求: ${url.split('?')[0].split('/').pop()}`);
      if (postData) {
        console.log(`参数: ${postData.slice(0, 200)}...`);
      }
    }
  });

  // 监听响应
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/platform/') && response.request().method() === 'POST') {
      try {
        const text = await response.text();
        const call = apiCalls.find(c => c.url === url && !c.response);
        if (call) {
          call.response = text.slice(0, 500);
          call.status = response.status();
          console.log(`响应: ${text.slice(0, 100)}...`);
        }
      } catch (e) {}
    }
  });

  try {
    // 1. 打开策略页面
    console.log('\n步骤1: 打开策略研究页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(3000);

    // 2. 检查登录
    console.log('\n步骤2: 检查登录状态...');
    const loginCheck = await page.evaluate(async () => {
      try {
        const resp = await fetch('/platform/user/getauthdata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1'
        });
        return await resp.json();
      } catch (e) {
        return { errorcode: -1 };
      }
    });

    if (loginCheck.errorcode !== 0) {
      console.log('✗ 未登录，请先运行登录脚本');
      await browser.close();
      return;
    }
    console.log('✓ 已登录');

    // 3. 点击一个策略进入编辑
    console.log('\n步骤3: 点击策略进入编辑...');

    // 尝试点击策略列表中的第一个策略
    await page.waitForTimeout(2000);

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'strategy-list.png') });

    // 查找策略项
    const strategyItems = await page.$$('tr[class*="strategy"], .strategy-item, [class*="algo"]');
    if (strategyItems.length > 0) {
      console.log(`找到 ${strategyItems.length} 个策略项`);
      await strategyItems[0].click();
    } else {
      // 直接打开编辑器
      console.log('直接打开编辑器...');
      await page.goto('https://quant.10jqka.com.cn/platform/study/html/editor.html?algo_id=67c935e607887b957629ad72');
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'editor-page.png') });

    // 4. 查找并点击回测按钮
    console.log('\n步骤4: 查找回测按钮...');

    // 等待编辑器加载
    await page.waitForTimeout(3000);

    // 尝试各种回测按钮选择器
    const backtestSelectors = [
      'button:has-text("回测")',
      'button:has-text("运行")',
      'a:has-text("回测")',
      '[class*="backtest"]',
      '[class*="run"]',
      '.btn-run',
      '.run-btn'
    ];

    let foundBtn = false;
    for (const sel of backtestSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn && await btn.isVisible()) {
          console.log(`找到回测按钮: ${sel}`);
          foundBtn = true;

          // 点击回测按钮
          await btn.click();
          console.log('点击回测按钮');
          break;
        }
      } catch (e) {}
    }

    if (!foundBtn) {
      console.log('未找到回测按钮，尝试其他方式...');

      // 尝试在页面中查找回测相关元素
      const pageContent = await page.content();
      if (pageContent.includes('backtest') || pageContent.includes('回测')) {
        console.log('页面包含回测相关内容');
      }

      // 尝试点击页面中的运行相关元素
      await page.evaluate(() => {
        // 查找所有按钮
        const buttons = document.querySelectorAll('button, a.btn, [role="button"]');
        for (const btn of buttons) {
          const text = btn.textContent || '';
          if (text.includes('回测') || text.includes('运行') || text.includes('测试')) {
            console.log('找到按钮:', text);
            btn.click();
            return text;
          }
        }
        return null;
      });
    }

    // 5. 等待回测请求
    console.log('\n步骤5: 等待回测 API 调用...');
    await page.waitForTimeout(10000);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'after-backtest.png') });

    // 6. 分析捕获的 API
    console.log('\n步骤6: 分析捕获的 API 调用...');

    // 过滤出回测相关的 API
    const backtestApis = apiCalls.filter(c =>
      c.url.includes('backtest') ||
      c.url.includes('run') ||
      c.url.includes('algorithm')
    );

    console.log(`\n捕获到 ${apiCalls.length} 个请求`);
    console.log(`回测相关: ${backtestApis.length} 个`);

    // 保存结果
    const result = {
      allCalls: apiCalls,
      backtestCalls: backtestApis,
      timestamp: Date.now()
    };

    const outputPath = path.join(OUTPUT_ROOT, 'captured-backtest-api.json');
    fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
    console.log(`\n保存到: ${outputPath}`);

    // 打印详细信息
    if (backtestApis.length > 0) {
      console.log('\n回测 API 详情:');
      backtestApis.forEach((api, i) => {
        console.log(`\n${i + 1}. ${api.url.split('?')[0]}`);
        console.log(`   方法: ${api.method}`);
        console.log(`   参数: ${api.postData}`);
        if (api.response) {
          console.log(`   响应: ${api.response}`);
        }
      });
    }

    // 保持浏览器打开一段时间
    console.log('\n浏览器保持打开20秒...');
    await page.waitForTimeout(20000);

    await browser.close();
    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'capture-error.png') });

    // 保存已捕获的数据
    const result = {
      allCalls: apiCalls,
      timestamp: Date.now(),
      error: error.message
    };
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'captured-backtest-api-error.json'), JSON.stringify(result, null, 2));

    await browser.close();
    throw error;
  }
}

captureBacktestAPI().catch(console.error);