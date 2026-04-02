#!/usr/bin/env node
/**
 * 捕获 BigQuant AIStudio 运行 notebook 时的真实 HTTP 请求
 * 登录后打开 studio，等待用户点击运行，捕获所有网络请求
 */
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
const studioUrl = `https://bigquant.com/aistudio/studios/${studioId}/?folder=/home/aiuser/work`;

const browser = await chromium.launch({ headless: false, slowMo: 100 });
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
  viewport: { width: 1440, height: 900 }
});

await context.addCookies(session.cookies);

const captured = [];

// 拦截所有请求
context.on('request', req => {
  const url = req.url();
  const method = req.method();
  if (url.includes('bigquant.com') && !url.includes('.js') && !url.includes('.css') && !url.includes('.png') && !url.includes('.woff')) {
    const entry = { method, url, postData: req.postData()?.slice(0, 500), time: Date.now() };
    captured.push(entry);
    if (url.includes('api') || url.includes('kernel') || url.includes('session') || url.includes('execute') || url.includes('run') || url.includes('task')) {
      console.log(`[REQ] ${method} ${url.replace('https://bigquant.com', '')}`);
      if (entry.postData) console.log(`      body: ${entry.postData.slice(0, 200)}`);
    }
  }
});

context.on('response', async resp => {
  const url = resp.url();
  if (url.includes('bigquant.com') && (url.includes('kernel') || url.includes('session') || url.includes('execute') || url.includes('run') || url.includes('task') || url.includes('aiflow'))) {
    try {
      const body = await resp.text();
      console.log(`[RESP] ${resp.status()} ${url.replace('https://bigquant.com', '').slice(0, 80)}`);
      console.log(`       ${body.slice(0, 300)}`);
      // 更新 captured
      const entry = captured.find(e => e.url === url && !e.response);
      if (entry) entry.response = { status: resp.status(), body: body.slice(0, 500) };
    } catch(e) {}
  }
});

const page = await context.newPage();
console.log('打开 AIStudio...');
await page.goto(studioUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

console.log('\n=== 页面已打开 ===');
console.log('请在浏览器中:');
console.log('1. 等待 VS Code 加载完成');
console.log('2. 打开或创建一个 notebook (.ipynb)');
console.log('3. 点击"运行全部"或 Shift+Enter 运行 cell');
console.log('4. 观察控制台输出的 API 请求');
console.log('\n按 Ctrl+C 保存结果并退出\n');

// 每 5 秒保存一次
const saveInterval = setInterval(() => {
  const outPath = path.join(__dirname, '../data/captured-run-api.json');
  fs.writeFileSync(outPath, JSON.stringify(captured, null, 2));
  const interesting = captured.filter(e => e.url.includes('kernel') || e.url.includes('session') || e.url.includes('execute'));
  if (interesting.length > 0) {
    console.log(`\n[已捕获 ${interesting.length} 个关键请求，保存到 data/captured-run-api.json]`);
  }
}, 5000);

process.on('SIGINT', () => {
  clearInterval(saveInterval);
  const outPath = path.join(__dirname, '../data/captured-run-api.json');
  fs.writeFileSync(outPath, JSON.stringify(captured, null, 2));
  console.log(`\n已保存 ${captured.length} 个请求到 ${outPath}`);
  browser.close().then(() => process.exit(0));
});

// 保持运行
await new Promise(() => {});
