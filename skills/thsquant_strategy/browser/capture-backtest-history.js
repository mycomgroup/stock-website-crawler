#!/usr/bin/env node
/**
 * 访问回测历史页面捕获 API
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureBacktestHistory() {
  console.log('\n' + '='.repeat(70));
  console.log('回测历史页面 API 捕获');
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
      const call = {
        id: apiCalls.length,
        url,
        method,
        postData,
        time: Date.now()
      };
      apiCalls.push(call);

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
                if (json.result) {
                  if (typeof json.result === 'object') {
                    const keys = Object.keys(json.result).slice(0, 5);
                    if (keys.length > 0) console.log(`  result: ${keys.join(', ')}`);
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
    const strategyId = '67c935e607887b957629ad72';

    // 1. 访问回测历史页面
    console.log('\n步骤1: 访问回测历史页面...');
    const historyUrl = `https://quant.10jqka.com.cn/view/backreport-history.html#algoid/${strategyId}`;
    console.log(`URL: ${historyUrl}`);

    await page.goto(historyUrl, {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    await page.waitForTimeout(5000);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'backtest-history.png'), fullPage: true });

    // 2. 分析页面
    console.log('\n步骤2: 分析页面...');
    const pageInfo = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]'))
        .filter(el => el.textContent?.trim())
        .map(el => ({
          text: el.textContent?.trim().slice(0, 30),
          className: el.className?.slice(0, 40)
        }));

      // 查找回测记录
      const backtestItems = document.querySelectorAll('tr, .backtest-item, .item');
      const items = Array.from(backtestItems).slice(0, 5).map(el => ({
        text: el.textContent?.trim().slice(0, 80)
      }));

      return { buttons: buttons.slice(0, 20), items };
    });

    console.log('页面按钮:');
    pageInfo.buttons.forEach(b => console.log(`  "${b.text}"`));

    console.log('\n回测记录:');
    pageInfo.items.forEach(i => console.log(`  ${i.text}`));

    // 3. 尝试找到运行回测的入口
    console.log('\n步骤3: 查找运行回测入口...');

    // 检查是否有"运行回测"或类似按钮
    const runBtns = pageInfo.buttons.filter(b =>
      b.text.includes('运行') || b.text.includes('回测') || b.text.includes('新建回测')
    );

    console.log('运行按钮:', runBtns);

    // 4. 尝试直接访问策略编辑 API 获取更多信息
    console.log('\n步骤4: 尝试获取策略详情...');

    const strategyInfo = await page.evaluate(async (sid) => {
      try {
        // 尝试获取策略详情
        const resp = await fetch('/platform/algorithms/queryall2/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1&datatype=jsonp'
        });
        const text = await resp.text();
        const match = text.match(/\((.+)\)/s);
        if (match) {
          const json = JSON.parse(match[1]);
          const strategies = json.result?.strategys || [];
          return strategies.find(s => s.algo_id === sid) || null;
        }
      } catch (e) {
        return { error: e.message };
      }
    }, strategyId);

    console.log('策略信息:', strategyInfo);

    // 5. 尝试获取回测历史
    console.log('\n步骤5: 尝试获取回测历史...');

    const backtestHistory = await page.evaluate(async (sid) => {
      try {
        // 尝试获取回测列表
        const resp = await fetch('/platform/backtest/queryall/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: `isajax=1&algo_id=${sid}`
        });
        return await resp.json();
      } catch (e) {
        return { error: e.message };
      }
    }, strategyId);

    console.log('回测历史:', backtestHistory);

    // 6. 等待用户操作
    console.log('\n请手动操作浏览器...');
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
      c.url.includes('backtest')
    );

    console.log(`\n总 POST 请求: ${apiCalls.length}`);
    console.log(`回测相关: ${backtestApis.length}`);

    backtestApis.forEach(api => {
      console.log(`\n★ ${api.url}`);
      console.log(`  参数: ${api.postData}`);
      if (api.responseJson) {
        console.log(`  响应: ${JSON.stringify(api.responseJson).slice(0, 300)}`);
      }
    });

    // 保存结果
    const result = {
      strategyInfo,
      backtestHistory,
      totalCalls: apiCalls.length,
      backtestApis,
      allCalls: apiCalls,
      timestamp: Date.now()
    };

    fs.writeFileSync(path.join(OUTPUT_ROOT, 'backtest-history-capture.json'), JSON.stringify(result, null, 2));

    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'history-error.png') });
    await browser.close();
    throw error;
  }
}

captureBacktestHistory().catch(console.error);