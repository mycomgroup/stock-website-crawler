#!/usr/bin/env node
/**
 * 自动捕获回测 API 参数
 * 打开策略编辑页面，自动点击回测按钮，捕获完整 API 调用
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoCaptureBacktest(strategyId = '67c935e607887b957629ad72') {
  console.log('\n' + '='.repeat(70));
  console.log('自动捕获回测 API');
  console.log('='.repeat(70));
  console.log(`\n策略 ID: ${strategyId}`);

  // 加载 session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  // 收集 API 调用
  const apiCalls = [];
  let backtestRunApi = null;

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 监听所有 POST 请求
  page.on('request', request => {
    if (request.method() === 'POST') {
      const url = request.url();
      const postData = request.postData() || '';

      const call = {
        id: apiCalls.length,
        url,
        method: 'POST',
        postData,
        time: Date.now()
      };
      apiCalls.push(call);

      // 检测回测运行 API
      if (url.includes('backtest') && (url.includes('run') || postData.includes('run'))) {
        backtestRunApi = call;
        console.log('\n★ 检测到回测运行 API!');
        console.log(`  URL: ${url}`);
        console.log(`  参数: ${postData}`);
      }

      // 打印重要 API
      if (url.includes('/platform/')) {
        const endpoint = url.split('/platform/')[1]?.split('?')[0] || url;
        console.log(`\n[${apiCalls.length}] ${endpoint}`);
        if (postData && !postData.includes('isajax=1&datatype=jsonp')) {
          const params = new URLSearchParams(postData);
          const important = {};
          for (const [k, v] of params) {
            if (k !== 'isajax' && k !== 'datatype') {
              important[k] = v.length > 50 ? v.slice(0, 50) + '...' : v;
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
    const req = response.request();
    if (req.method() === 'POST') {
      const call = apiCalls.find(c => c.url === url && !c.response);
      if (call) {
        call.status = response.status();
        try {
          const text = await response.text();
          call.response = text.slice(0, 300);

          // 解析 JSONP
          const match = text.match(/\((.+)\)/s);
          if (match) {
            try {
              const json = JSON.parse(match[1]);
              call.responseJson = json;
              if (json.errorcode !== undefined) {
                console.log(`  响应: errorcode=${json.errorcode}`);
              }
            } catch (e) {}
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 直接打开策略编辑页面
    console.log('\n打开策略编辑页面...');
    const editorUrl = `https://quant.10jqka.com.cn/platform/study/html/editor.html?algo_id=${strategyId}`;
    await page.goto(editorUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

    console.log('等待页面加载...');
    await page.waitForTimeout(5000);

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'editor-initial.png') });

    // 检查登录状态
    const loginStatus = await page.evaluate(async () => {
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

    if (loginStatus.errorcode !== 0) {
      console.log('✗ 未登录');
      await browser.close();
      return { success: false, reason: 'not_logged_in' };
    }
    console.log('✓ 已登录');

    // 查找回测按钮 - 使用多种策略
    console.log('\n查找回测按钮...');

    // 先等待页面稳定
    await page.waitForTimeout(3000);

    // 尝试查找按钮
    const buttonSelectors = [
      // 常见回测按钮选择器
      'button:has-text("回测")',
      'button:has-text("运行")',
      'button:has-text("运行回测")',
      'a:has-text("回测")',
      '[class*="run-btn"]',
      '[class*="backtest-btn"]',
      '[class*="btn-run"]',
      '.run-button',
      '.backtest-button',
      // ID 选择器
      '[id*="run"]',
      '[id*="backtest"]',
      // 图标按钮
      'button:has(.icon-run)',
      'button:has(.icon-backtest)',
    ];

    let foundButton = null;
    for (const sel of buttonSelectors) {
      try {
        const locator = page.locator(sel);
        const count = await locator.count();
        if (count > 0) {
          const first = locator.first();
          if (await first.isVisible()) {
            foundButton = first;
            console.log(`✓ 找到按钮: ${sel}`);
            break;
          }
        }
      } catch (e) {
        continue;
      }
    }

    if (foundButton) {
      // 截图找到按钮的状态
      await page.screenshot({ path: path.join(OUTPUT_ROOT, 'before-click.png') });

      console.log('\n点击回测按钮...');
      await foundButton.click();

      console.log('等待回测 API 调用...');
      await page.waitForTimeout(10000);

      // 截图点击后状态
      await page.screenshot({ path: path.join(OUTPUT_ROOT, 'after-click.png') });

    } else {
      console.log('\n⚠ 未自动找到回测按钮');
      console.log('请手动点击回测按钮...');
      console.log('脚本将监听网络请求 30 秒');

      // 打印页面元素信息帮助调试
      const pageButtons = await page.evaluate(() => {
        const buttons = document.querySelectorAll('button, a.btn, [role="button"], input[type="button"]');
        return Array.from(buttons).map(b => ({
          text: b.textContent?.trim().slice(0, 30),
          class: b.className?.slice(0, 50),
          id: b.id,
          type: b.type || b.tagName
        })).filter(b => b.text || b.id);
      });

      console.log('\n页面按钮:');
      pageButtons.slice(0, 10).forEach(b => {
        console.log(`  ${b.type}: "${b.text}" class="${b.class}" id="${b.id}"`);
      });

      await page.waitForTimeout(30000);
    }

    // 等待更多请求
    console.log('\n继续监听 20 秒...');
    await page.waitForTimeout(20000);

    // 最终截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'final-state.png') });

    // 保存 session
    const newCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: newCookies,
      timestamp: Date.now()
    }, null, 2));

    await browser.close();

    // 分析结果
    console.log('\n' + '='.repeat(70));
    console.log('捕获结果分析');
    console.log('='.repeat(70));

    console.log(`\n总 POST 请求: ${apiCalls.length} 个`);

    // 找出回测相关的 API
    const backtestApis = apiCalls.filter(c =>
      c.url.includes('backtest') ||
      c.url.includes('run') ||
      (c.postData && (c.postData.includes('backtest') || c.postData.includes('run')))
    );

    const algoApis = apiCalls.filter(c =>
      c.url.includes('algo') || c.url.includes('algorithm')
    );

    console.log(`回测相关: ${backtestApis.length} 个`);
    console.log(`策略相关: ${algoApis.length} 个`);

    if (backtestApis.length > 0) {
      console.log('\n回测 API 详情:');
      backtestApis.forEach((api, i) => {
        console.log(`\n--- API ${i + 1} ---`);
        console.log(`URL: ${api.url}`);
        console.log(`状态: ${api.status}`);
        console.log(`参数: ${api.postData}`);
        if (api.response) {
          console.log(`响应: ${api.response}`);
        }
      });
    }

    // 保存完整结果
    const result = {
      strategyId,
      totalCalls: apiCalls.length,
      backtestApis,
      algoApis,
      allCalls: apiCalls,
      backtestRunApi,
      timestamp: Date.now()
    };

    const outputPath = path.join(OUTPUT_ROOT, 'auto-captured-backtest-api.json');
    fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
    console.log(`\n保存到: ${outputPath}`);

    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'error-screenshot.png') });

    // 保存已捕获数据
    const result = {
      strategyId,
      totalCalls: apiCalls.length,
      allCalls: apiCalls,
      error: error.message,
      timestamp: Date.now()
    };
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'auto-capture-error.json'), JSON.stringify(result, null, 2));

    await browser.close();
    throw error;
  }
}

// 命令行参数
const args = process.argv.slice(2);
const strategyId = args.find(a => !a.startsWith('--')) || '67c935e607887b957629ad72';

autoCaptureBacktest(strategyId)
  .then(result => {
    if (result.backtestApis?.length > 0) {
      console.log('\n✓ 成功捕获回测 API!');
    } else {
      console.log('\n⚠ 未捕获到回测 API，请手动操作后重试');
    }
  })
  .catch(console.error);