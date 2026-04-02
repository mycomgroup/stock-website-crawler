#!/usr/bin/env node
/**
 * 捕获创建策略的真实请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureCreateRequest() {
  console.log('\n' + '='.repeat(70));
  console.log('捕获创建策略的真实请求');
  console.log('='.repeat(70));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  // 捕获所有请求
  const requests = [];

  page.on('request', req => {
    const url = req.url();
    if (url.includes('/platform/') || url.includes('algo')) {
      requests.push({
        url,
        method: req.method(),
        postData: req.postData(),
        headers: req.headers()
      });
      console.log(`\n[请求] ${req.method()} ${url.split('?')[0]}`);
      if (req.postData()) {
        console.log(`  Body: ${req.postData()}`);
      }
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/platform/')) {
      try {
        const text = await resp.text();
        console.log(`  Response: ${text.substring(0, 100)}`);
      } catch (e) {}
    }
  });

  try {
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    console.log('\n' + '='.repeat(70));
    console.log('请执行以下操作:');
    console.log('  1. 点击"策略研究"');
    console.log('  2. 点击"新建策略"');
    console.log('  3. 输入策略名称');
    console.log('  4. 点击"保存"');
    console.log('  5. (可选) 运行回测');
    console.log('\n完成后按回车保存捕获结果...');

    // 等待用户输入
    await new Promise(resolve => {
      process.stdin.once('data', resolve);
    });

    // 保存捕获结果
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'create-strategy-requests.json'),
      JSON.stringify(requests, null, 2));
    console.log(`\n保存: ${requests.length} 个请求`);

    // 分析创建相关的请求
    const createRequests = requests.filter(r =>
      r.url.includes('add') || r.url.includes('create') || r.url.includes('save')
    );

    console.log('\n创建相关请求:');
    createRequests.forEach(req => {
      console.log(`\n${req.method} ${req.url}`);
      console.log(`Body: ${req.postData}`);
    });

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);
    await browser.close();
    throw error;
  }
}

captureCreateRequest().catch(console.error);