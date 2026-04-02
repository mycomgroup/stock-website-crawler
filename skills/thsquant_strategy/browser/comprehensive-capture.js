#!/usr/bin/env node
/**
 * THSQuant 全面API捕获工具
 * 捕获HTTP请求、WebSocket消息、iframe内部请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function comprehensiveCapture() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 全面API捕获工具');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

  console.log('\n账号信息:');
  console.log(`  Username: ${username}`);
  console.log(`  Password: ${password}`);

  // 加载session
  let cookies = [];
  if (fs.existsSync(SESSION_FILE)) {
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    cookies = session.cookies || [];
    console.log(`\n已有Session: ${cookies.length} cookies`);
  }

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--auto-open-devtools-for-tabs'  // 自动打开开发者工具
    ]
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  if (cookies.length > 0) await context.addCookies(cookies);
  const page = await context.newPage();

  // 捕获数据结构
  const capturedData = {
    httpRequests: [],
    websocketMessages: [],
    iframeRequests: [],
    consoleLogs: [],
    networkEvents: []
  };

  let requestId = 0;

  // 1. 监听所有HTTP请求
  page.on('request', request => {
    const url = request.url();
    const id = requestId++;

    const reqData = {
      id,
      url,
      method: request.method(),
      postData: request.postData(),
      headers: request.headers(),
      resourceType: request.resourceType(),
      frame: request.frame()?.url() || 'main',
      time: Date.now()
    };

    capturedData.httpRequests.push(reqData);

    // 实时显示重要请求
    if (url.includes('/platform/') || url.includes('.do') ||
        url.includes('strategy') || url.includes('backtest')) {
      console.log(`\n[HTTP ${id}] ${request.method()} ${url.split('?')[0]}`);
      if (request.postData()) {
        console.log(`    Body: ${request.postData().substring(0, 100)}`);
      }
    }
  });

  // 2. 监听响应
  page.on('response', async response => {
    const url = response.url();
    try {
      const req = capturedData.httpRequests.find(r => r.url === url && !r.status);
      if (req) {
        req.status = response.status();
        req.responseHeaders = Object.fromEntries(response.headers());

        try {
          const body = await response.text();
          req.response = body.substring(0, 1500);

          // 显示响应摘要
          if (url.includes('/platform/') || url.includes('.do')) {
            console.log(`    Status: ${req.status}`);
            try {
              const json = JSON.parse(body);
              console.log(`    Response: errorcode=${json.errorcode || 'N/A'}`);
              if (json.result) {
                const resultPreview = JSON.stringify(json.result).substring(0, 80);
                console.log(`    Result: ${resultPreview}`);
              }
            } catch (e) {
              if (body.length < 100) console.log(`    Response: ${body}`);
            }
          }
        } catch (e) {
          req.responseError = e.message;
        }
      }
    } catch (e) {}
  });

  // 3. 监听WebSocket
  page.on('websocket', ws => {
    console.log(`\n[WebSocket] ${ws.url()}`);

    ws.on('framesreceived', frames => {
      frames.forEach(frame => {
        capturedData.websocketMessages.push({
          type: 'received',
          url: ws.url(),
          data: frame.payload,
          time: Date.now()
        });
        console.log(`    WS Received: ${String(frame.payload).substring(0, 80)}`);
      });
    });

    ws.on('framessent', frames => {
      frames.forEach(frame => {
        capturedData.websocketMessages.push({
          type: 'sent',
          url: ws.url(),
          data: frame.payload,
          time: Date.now()
        });
        console.log(`    WS Sent: ${String(frame.payload).substring(0, 80)}`);
      });
    });
  });

  // 4. 监听Console
  page.on('console', msg => {
    capturedData.consoleLogs.push({
      type: msg.type(),
      text: msg.text(),
      time: Date.now()
    });
  });

  // 5. 监听网络错误
  page.on('requestfailed', request => {
    capturedData.networkEvents.push({
      type: 'failed',
      url: request.url(),
      error: request.failure()?.errorText,
      time: Date.now()
    });
  });

  try {
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });

    // 等待页面稳定
    await page.waitForTimeout(5000);

    // 检查当前页面结构
    console.log('\n分析页面结构...');

    // 检查iframe
    const frames = page.frames();
    console.log(`发现 ${frames.length} 个frame:`);
    frames.forEach((frame, i) => {
      try {
        const frameUrl = frame.url();
        console.log(`  Frame ${i}: ${frameUrl.substring(0, 60)}`);
      } catch (e) {}
    });

    // 检查是否有Vue/React应用
    const appInfo = await page.evaluate(() => {
      return {
        hasVue: !!window.Vue || !!window.__VUE__,
        hasReact: !!window.React || !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__,
        hasAngular: !!window.angular || !!window.ng,
        monacoEditor: !!window.monaco,
        codeMirror: !!window.CodeMirror,
        aceEditor: !!window.ace,
        localStorage: Object.keys(localStorage),
        sessionStorage: Object.keys(sessionStorage)
      };
    });
    console.log('\n页面技术栈:');
    console.log(`  Vue: ${appInfo.hasVue}`);
    console.log(`  React: ${appInfo.hasReact}`);
    console.log(`  Monaco Editor: ${appInfo.monacoEditor}`);
    console.log(`  LocalStorage keys: ${appInfo.localStorage.join(', ')}`);

    console.log('\n' + '='.repeat(70));
    console.log('请手动完成以下操作以触发更多API:');
    console.log('='.repeat(70));
    console.log('\n  1. 登录 (如果未登录)');
    console.log('  2. 点击"新建策略"');
    console.log('  3. 输入策略代码');
    console.log('  4. 点击"保存"');
    console.log('  5. 点击"运行回测"');
    console.log('  6. 查看结果');
    console.log('\n操作完成后按回车键保存...');

    // 等待用户输入
    const rl = readline.createInterface({ input, output });
    await rl.question('\n>>> 按回车完成捕获 >>> ');
    rl.close();

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    // 分析捕获的数据
    console.log('\n' + '='.repeat(70));
    console.log('捕获数据分析');
    console.log('='.repeat(70));

    // HTTP请求统计
    const httpComplete = capturedData.httpRequests.filter(r => r.status);
    const platformAPIs = httpComplete.filter(r => r.url.includes('/platform/'));
    const strategyAPIs = httpComplete.filter(r =>
      r.url.includes('strategy') || r.url.includes('backtest'));

    console.log(`\nHTTP请求统计:`);
    console.log(`  总请求: ${capturedData.httpRequests.length}`);
    console.log(`  有响应: ${httpComplete.length}`);
    console.log(`  Platform API: ${platformAPIs.length}`);
    console.log(`  策略/回测 API: ${strategyAPIs.length}`);

    console.log(`\nWebSocket消息: ${capturedData.websocketMessages.length}`);
    console.log(`Console日志: ${capturedData.consoleLogs.length}`);

    // 保存完整数据
    const fullPath = path.join(OUTPUT_ROOT, 'comprehensive-capture.json');
    fs.writeFileSync(fullPath, JSON.stringify(capturedData, null, 2));
    console.log(`\n完整数据: ${fullPath}`);

    // 分析API端点
    const apiEndpoints = {};
    platformAPIs.forEach(req => {
      const key = `${req.method} ${req.url.split('?')[0]}`;
      if (!apiEndpoints[key]) {
        apiEndpoints[key] = {
          count: 0,
          samples: []
        };
      }
      apiEndpoints[key].count++;
      apiEndpoints[key].samples.push({
        postData: req.postData,
        response: req.response,
        status: req.status
      });
    });

    // 保存API端点分析
    const endpointsPath = path.join(OUTPUT_ROOT, 'comprehensive-endpoints.json');
    fs.writeFileSync(endpointsPath, JSON.stringify(apiEndpoints, null, 2));
    console.log(`API端点: ${endpointsPath}`);

    // 打印发现的端点
    console.log('\n' + '='.repeat(70));
    console.log('发现的Platform API端点:');
    console.log('='.repeat(70));

    Object.keys(apiEndpoints).forEach(key => {
      const ep = apiEndpoints[key];
      console.log(`\n${key}`);
      console.log(`  调用次数: ${ep.count}`);
      const sample = ep.samples[0];
      if (sample.postData) {
        console.log(`  Body示例: ${sample.postData.substring(0, 80)}`);
      }
      if (sample.response) {
        try {
          const json = JSON.parse(sample.response);
          console.log(`  Response: errorcode=${json.errorcode || 'N/A'}`);
        } catch (e) {
          console.log(`  Response: ${sample.response.substring(0, 60)}`);
        }
      }
    });

    // WebSocket分析
    if (capturedData.websocketMessages.length > 0) {
      console.log('\n' + '='.repeat(70));
      console.log('WebSocket消息分析:');
      console.log('='.repeat(70));

      const wsUrls = [...new Set(capturedData.websocketMessages.map(m => m.url))];
      wsUrls.forEach(url => {
        console.log(`\nWebSocket URL: ${url}`);
        const messages = capturedData.websocketMessages.filter(m => m.url === url);
        console.log(`  消息数量: ${messages.length}`);
        messages.slice(0, 3).forEach(m => {
          console.log(`  ${m.type}: ${String(m.data).substring(0, 80)}`);
        });
      });
    }

    // Console日志分析
    const importantLogs = capturedData.consoleLogs.filter(l =>
      l.text.includes('API') || l.text.includes('error') ||
      l.text.includes('strategy') || l.text.includes('backtest'));

    if (importantLogs.length > 0) {
      console.log('\n相关Console日志:');
      importantLogs.forEach(log => {
        console.log(`  [${log.type}] ${log.text.substring(0, 100)}`);
      });
    }

    await browser.close();

    return capturedData;

  } catch (error) {
    console.error('\n错误:', error.message);

    fs.writeFileSync(path.join(OUTPUT_ROOT, 'capture-error.json'),
      JSON.stringify({ error: error.message, data: capturedData }, null, 2));

    try {
      fs.writeFileSync(SESSION_FILE, JSON.stringify({
        cookies: await context.cookies(),
        timestamp: Date.now()
      }, null, 2));
    } catch (e) {}

    await browser.close();
    throw error;
  }
}

comprehensiveCapture().then(data => {
  console.log('\n' + '='.repeat(70));
  console.log('✓ 捕获完成');
  console.log('='.repeat(70));
  console.log('\n请查看:');
  console.log('  - data/comprehensive-capture.json');
  console.log('  - data/comprehensive-endpoints.json');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});