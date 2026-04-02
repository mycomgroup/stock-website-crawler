#!/usr/bin/env node
/**
 * THSQuant 真实API捕获
 * 打开浏览器让用户操作，捕获所有API请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureRealAPIs() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 真实API捕获');
  console.log('='.repeat(70));

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  // 添加cookies
  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }

  const page = await context.newPage();

  // 捕获所有请求
  const allRequests = [];
  let reqId = 0;

  page.on('request', req => {
    const url = req.url();
    const id = reqId++;

    // 过滤静态资源
    if (!url.includes('.css') && !url.includes('.js') && !url.includes('.png') &&
        !url.includes('.jpg') && !url.includes('.gif') && !url.includes('.woff') &&
        !url.includes('google-analytics') && !url.includes('cbasspider')) {

      allRequests.push({
        id,
        url,
        path: url.split('?')[0],
        query: url.split('?')[1] || '',
        method: req.method(),
        postData: req.postData(),
        headers: req.headers(),
        time: Date.now()
      });

      // 打印platform相关请求
      if (url.includes('/platform/')) {
        console.log(`\n[${id}] ${req.method()} ${url.split('?')[0]}`);
        if (req.postData()) {
          console.log(`    Body: ${req.postData().substring(0, 100)}`);
        }
      }
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    const req = allRequests.find(r => r.url === url && !r.status);

    if (req) {
      req.status = resp.status();
      try {
        const body = await resp.text();
        req.response = body.substring(0, 1000);

        if (url.includes('/platform/')) {
          console.log(`    Status: ${req.status}`);
          try {
            const json = JSON.parse(body);
            console.log(`    Response: errorcode=${json.errorcode || 'N/A'}`);
            if (json.result) {
              console.log(`    Result: ${JSON.stringify(json.result).substring(0, 80)}`);
            }
          } catch (e) {
            console.log(`    Response: ${body.substring(0, 80)}`);
          }
        }
      } catch (e) {}
    }
  });

  try {
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });

    console.log('\n' + '='.repeat(70));
    console.log('请在浏览器中执行以下操作以捕获API:');
    console.log('='.repeat(70));
    console.log('\n  1. 点击"策略研究"');
    console.log('  2. 查看策略列表');
    console.log('  3. 点击"新建策略"');
    console.log('  4. 查看回测列表');
    console.log('  5. 尝试运行回测');
    console.log('\n完成后按回车保存捕获的API...');

    // 等待用户输入
    await new Promise(resolve => {
      process.stdin.once('data', resolve);
    });

    // 分析捕获的API
    console.log('\n' + '='.repeat(70));
    console.log('分析捕获的API');
    console.log('='.repeat(70));

    const platformRequests = allRequests.filter(r => r.url.includes('/platform/'));

    console.log(`\n总捕获: ${allRequests.length} 个请求`);
    console.log(`Platform API: ${platformRequests.length} 个请求`);

    // 按路径分组
    const apiGroups = {};
    platformRequests.forEach(req => {
      if (!apiGroups[req.path]) {
        apiGroups[req.path] = {
          method: req.method,
          count: 0,
          samples: []
        };
      }
      apiGroups[req.path].count++;
      if (apiGroups[req.path].samples.length < 3) {
        apiGroups[req.path].samples.push({
          query: req.query,
          postData: req.postData,
          status: req.status,
          response: req.response
        });
      }
    });

    // 保存API端点
    const endpointsPath = path.join(OUTPUT_ROOT, 'captured-api-endpoints.json');
    fs.writeFileSync(endpointsPath, JSON.stringify(apiGroups, null, 2));
    console.log(`\n保存: ${endpointsPath}`);

    // 打印发现的端点
    console.log('\n发现的API端点:');
    Object.keys(apiGroups).forEach(path => {
      const ep = apiGroups[path];
      console.log(`\n${ep.method} ${path}`);
      console.log(`  调用次数: ${ep.count}`);

      const sample = ep.samples[0];
      if (sample.postData) {
        console.log(`  Body: ${sample.postData.substring(0, 80)}`);
      }
      if (sample.response) {
        try {
          const json = JSON.parse(sample.response);
          console.log(`  Response: errorcode=${json.errorcode || 'N/A'}`);
        } catch (e) {}
      }
    });

    // 保存完整请求
    const fullPath = path.join(OUTPUT_ROOT, 'captured-all-requests.json');
    fs.writeFileSync(fullPath, JSON.stringify(allRequests, null, 2));
    console.log(`\n完整请求: ${fullPath}`);

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    await browser.close();

    return apiGroups;

  } catch (error) {
    console.error('\n错误:', error.message);
    await browser.close();
    throw error;
  }
}

captureRealAPIs().then(() => {
  console.log('\n✓ 完成');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});