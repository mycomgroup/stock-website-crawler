#!/usr/bin/env node
/**
 * THSQuant 交互式API捕获工具
 * 用户手动操作平台，脚本捕获所有API请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '..');

async function interactiveCapture() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 交互式API捕获工具');
  console.log('='.repeat(70));
  console.log('\n请在浏览器中完成以下操作，脚本会捕获所有API请求:');
  console.log('  1. 登录平台');
  console.log('  2. 创建新策略');
  console.log('  3. 输入策略代码');
  console.log('  4. 保存策略');
  console.log('  5. 运行回测');
  console.log('  6. 查看回测结果');
  console.log('\n账号信息:');
  console.log(`  Username: ${username}`);
  console.log(`  Password: ${password}`);

  // 加载session
  let cookies = [];
  if (fs.existsSync(SESSION_FILE)) {
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    cookies = session.cookies || [];
  }

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  if (cookies.length > 0) await context.addCookies(cookies);
  const page = await context.newPage();

  // 捕获所有请求
  const capturedRequests = [];
  let requestId = 0;

  // 监听请求
  page.on('request', request => {
    const url = request.url();
    // 过滤静态资源，只关注API请求
    if (!url.includes('.css') && !url.includes('.js') && !url.includes('.png') &&
        !url.includes('.jpg') && !url.includes('.gif') && !url.includes('.woff') &&
        !url.includes('google-analytics') && !url.includes('cbasspider')) {

      const id = requestId++;
      capturedRequests.push({
        id,
        url: url,
        path: url.split('?')[0],
        query: url.split('?')[1] || '',
        method: request.method(),
        postData: request.postData(),
        headers: {},
        time: Date.now(),
        status: null,
        response: null
      });

      // 实时打印API调用
      if (url.includes('/platform/') || url.includes('.do')) {
        console.log(`\n[${id}] ${request.method()} ${url.split('?')[0]}`);
        if (request.postData()) {
          console.log(`    Body: ${request.postData().substring(0, 80)}`);
        }
      }
    }
  });

  // 监听响应
  page.on('response', async response => {
    const url = response.url();
    if (!url.includes('.css') && !url.includes('.js') && !url.includes('.png') &&
        !url.includes('.jpg') && !url.includes('.gif') && !url.includes('.woff') &&
        !url.includes('google-analytics') && !url.includes('cbasspider')) {

      try {
        const body = await response.text();
        const req = capturedRequests.find(r => r.url === url && r.status === null);
        if (req) {
          req.status = response.status();
          req.response = body.substring(0, 1500);
          req.responseHeaders = Object.fromEntries(response.headers());

          // 打印响应摘要
          if (url.includes('/platform/') || url.includes('.do')) {
            console.log(`    Status: ${req.status}`);
            if (body.length < 200) {
              console.log(`    Response: ${body}`);
            } else {
              // 尝试解析JSON显示errorcode
              try {
                const json = JSON.parse(body);
                console.log(`    Response: errorcode=${json.errorcode}, errormsg=${json.errormsg || ''}`);
                if (json.result) {
                  const resultStr = JSON.stringify(json.result).substring(0, 100);
                  console.log(`    Result: ${resultStr}`);
                }
              } catch (e) {
                console.log(`    Response: ${body.substring(0, 80)}...`);
              }
            }
          }
        }
      } catch (e) {}
    }
  });

  try {
    // 打开平台
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded'
    });

    console.log('\n' + '='.repeat(70));
    console.log('浏览器已打开，请手动完成以下操作:');
    console.log('='.repeat(70));
    console.log('\n建议操作顺序:');
    console.log('  1. 登录 (右上角登录按钮)');
    console.log('  2. 点击"策略研究"或"我的策略"');
    console.log('  3. 点击"新建策略"');
    console.log('  4. 输入策略名称和代码');
    console.log('  5. 点击"保存"');
    console.log('  6. 点击"运行回测"');
    console.log('  7. 查看回测结果');
    console.log('\n完成操作后，按回车键保存捕获的API...');

    // 使用readline等待用户输入
    const rl = readline.createInterface({ input, output });
    await rl.question('\n按回车键完成捕获并保存...');
    rl.close();

    // 保存session
    const newCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: newCookies,
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    // 分析捕获的API
    console.log('\n' + '='.repeat(70));
    console.log('分析捕获的API请求');
    console.log('='.repeat(70));

    const completeRequests = capturedRequests.filter(r => r.status !== null);
    const platformRequests = completeRequests.filter(r => r.url.includes('/platform/'));

    console.log(`\n总捕获: ${capturedRequests.length} 个请求`);
    console.log(`完整捕获: ${completeRequests.length} 个请求`);
    console.log(`平台API: ${platformRequests.length} 个请求`);

    // 保存完整数据
    const fullPath = path.join(OUTPUT_ROOT, 'captured-all.json');
    fs.writeFileSync(fullPath, JSON.stringify(capturedRequests, null, 2));
    console.log(`\n保存: ${fullPath}`);

    // 分类API
    const apiEndpoints = {};
    platformRequests.forEach(req => {
      const key = `${req.method} ${req.path}`;
      if (!apiEndpoints[key]) {
        apiEndpoints[key] = {
          method: req.method,
          path: req.path,
          samples: []
        };
      }
      apiEndpoints[key].samples.push({
        query: req.query,
        postData: req.postData,
        status: req.status,
        response: req.response
      });
    });

    // 保存API端点汇总
    const endpointsPath = path.join(OUTPUT_ROOT, 'api-endpoints.json');
    fs.writeFileSync(endpointsPath, JSON.stringify(apiEndpoints, null, 2));
    console.log(`保存: ${endpointsPath}`);

    // 打印发现的API端点
    console.log('\n' + '='.repeat(70));
    console.log('发现的THSQuant API端点:');
    console.log('='.repeat(70));

    Object.keys(apiEndpoints).forEach(key => {
      const ep = apiEndpoints[key];
      console.log(`\n${ep.method} ${ep.path}`);
      console.log(`  调用次数: ${ep.samples.length}`);

      // 显示第一个样本
      const sample = ep.samples[0];
      if (sample.query) {
        console.log(`  Query: ${sample.query.substring(0, 80)}`);
      }
      if (sample.postData) {
        console.log(`  Body: ${sample.postData.substring(0, 100)}`);
      }
      console.log(`  Status: ${sample.status}`);

      // 尝试解析响应
      try {
        const json = JSON.parse(sample.response);
        console.log(`  Response: errorcode=${json.errorcode}`);
        if (json.result) {
          const resultType = typeof json.result;
          console.log(`  Result类型: ${resultType}`);
        }
      } catch (e) {
        if (sample.response) {
          console.log(`  Response: ${sample.response.substring(0, 60)}...`);
        }
      }
    });

    // 生成API使用示例
    console.log('\n' + '='.repeat(70));
    console.log('API调用示例代码:');
    console.log('='.repeat(70));

    Object.keys(apiEndpoints).forEach(key => {
      const ep = apiEndpoints[key];
      if (ep.method === 'POST' && ep.path.includes('/platform/')) {
        console.log(`\n// ${ep.path}`);
        console.log(`curl -X POST 'https://quant.10jqka.com.cn${ep.path}' \\`);
        console.log(`  -H 'Cookie: QUANT_RESEARCH_SESSIONID=<your_session>' \\`);
        console.log(`  -H 'Content-Type: application/x-www-form-urlencoded' \\`);
        if (ep.samples[0].postData) {
          console.log(`  -d '${ep.samples[0].postData}'`);
        }
      }
    });

    await browser.close();

    return platformRequests;

  } catch (error) {
    console.error('\n错误:', error.message);

    // 保存已捕获的数据
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'captured-partial.json'),
      JSON.stringify(capturedRequests, null, 2));

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

interactiveCapture().then(results => {
  console.log(`\n✓ 完成，捕获 ${results.length} 个平台API请求`);
  console.log('\n请查看以下文件:');
  console.log('  - data/captured-all.json (完整捕获)');
  console.log('  - data/api-endpoints.json (API端点汇总)');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});