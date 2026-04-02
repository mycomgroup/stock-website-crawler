#!/usr/bin/env node
/**
 * 交互式捕获回测 API
 * 打开浏览器等待用户手动操作，同时监听所有网络请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function interactiveCapture() {
  console.log('\n' + '='.repeat(70));
  console.log('交互式捕获回测 API');
  console.log('='.repeat(70));
  console.log('\n请在浏览器中:');
  console.log('  1. 点击一个策略进入编辑');
  console.log('  2. 设置回测参数');
  console.log('  3. 点击运行回测按钮');
  console.log('  4. 等待回测完成');
  console.log('  5. 完成后关闭浏览器');
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

  // 收集所有 API 调用
  const apiCalls = [];

  // 监听请求
  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    if (method === 'POST' && url.includes('/platform/')) {
      const postData = request.postData() || '';
      apiCalls.push({
        id: apiCalls.length,
        url,
        method,
        postData,
        headers: request.headers(),
        time: Date.now()
      });

      // 实时打印
      const endpoint = url.split('?')[0].split('/platform/')[1]?.split('/')[0] || url.split('/').pop();
      console.log(`\n[${apiCalls.length}] POST ${endpoint}`);
      if (postData) {
        // 解析参数
        const params = new URLSearchParams(postData);
        const keyParams = {};
        for (const [key, value] of params) {
          if (key !== 'isajax' && key !== 'datatype' && value.length < 100) {
            keyParams[key] = value;
          }
        }
        if (Object.keys(keyParams).length > 0) {
          console.log('  参数:', JSON.stringify(keyParams));
        }
      }
    }
  });

  // 监听响应
  page.on('response', async response => {
    const url = response.url();
    const request = response.request();
    if (request.method() === 'POST' && url.includes('/platform/')) {
      const call = apiCalls.find(c => c.url === url && !c.status);
      if (call) {
        call.status = response.status();
        try {
          const text = await response.text();
          call.response = text;

          // 解析 JSONP 响应
          const jsonpMatch = text.match(/\((.+)\)/s);
          if (jsonpMatch) {
            try {
              const json = JSON.parse(jsonpMatch[1]);
              call.responseJson = json;
              if (json.errorcode !== undefined) {
                console.log(`  响应: errorcode=${json.errorcode}`);
                if (json.result && typeof json.result === 'object') {
                  const keys = Object.keys(json.result).slice(0, 5);
                  console.log(`  result keys: ${keys.join(', ')}`);
                }
              }
            } catch (e) {}
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 打开策略页面
    console.log('\n打开策略研究页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded'
    });

    // 等待用户操作，浏览器关闭时自动退出
    console.log('\n等待用户操作...');
    console.log('脚本将持续监听网络请求直到浏览器关闭');

    // 等待浏览器关闭
    await browser.waitForEvent('disconnected', { timeout: 300000 }); // 5分钟超时

  } catch (e) {
    if (e.message.includes('disconnected')) {
      console.log('\n浏览器已关闭');
    } else {
      console.error('\n错误:', e.message);
    }
  }

  // 保存捕获的数据
  console.log('\n' + '='.repeat(70));
  console.log('保存捕获数据');
  console.log('='.repeat(70));

  // 分析回测相关 API
  const backtestApis = apiCalls.filter(c =>
    c.url.includes('backtest') ||
    c.url.includes('run') ||
    (c.postData && (c.postData.includes('backtest') || c.postData.includes('run')))
  );

  const algorithmApis = apiCalls.filter(c =>
    c.url.includes('algorithm') ||
    c.url.includes('algo') ||
    (c.postData && c.postData.includes('algo'))
  );

  console.log(`\n总计捕获: ${apiCalls.length} 个 POST 请求`);
  console.log(`回测相关: ${backtestApis.length} 个`);
  console.log(`策略相关: ${algorithmApis.length} 个`);

  // 保存详细数据
  const result = {
    total: apiCalls.length,
    backtestApis,
    algorithmApis,
    allCalls: apiCalls,
    timestamp: Date.now()
  };

  const outputPath = path.join(OUTPUT_ROOT, 'interactive-capture-result.json');
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
  console.log(`\n保存到: ${outputPath}`);

  // 打印回测 API 详情
  if (backtestApis.length > 0) {
    console.log('\n回测 API 详情:');
    backtestApis.forEach((api, i) => {
      console.log(`\n${i + 1}. ${api.url}`);
      console.log(`   参数: ${api.postData}`);
      if (api.responseJson) {
        console.log(`   响应: ${JSON.stringify(api.responseJson).slice(0, 200)}`);
      }
    });
  }

  // 打印策略 API 详情
  if (algorithmApis.length > 0) {
    console.log('\n策略 API 详情:');
    algorithmApis.forEach((api, i) => {
      console.log(`\n${i + 1}. ${api.url}`);
      console.log(`   参数: ${api.postData}`);
      if (api.responseJson) {
        console.log(`   响应: ${JSON.stringify(api.responseJson).slice(0, 200)}`);
      }
    });
  }

  return result;
}

interactiveCapture().catch(console.error);