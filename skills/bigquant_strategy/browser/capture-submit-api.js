#!/usr/bin/env node
/**
 * 专门捕获"提交模拟"按钮的 API 请求
 * 同时也捕获"全部运行"的完整流程
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

const browser = await chromium.launch({ headless: false });
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
  viewport: { width: 1440, height: 900 }
});
await context.addCookies(session.cookies);

const captured = [];
const interesting = [];

// 捕获所有 bigquant.com 请求（排除静态资源）
context.on('request', req => {
  const url = req.url();
  const method = req.method();
  if (!url.includes('bigquant.com')) return;
  if (url.match(/\.(js|css|png|svg|woff|ttf|wasm|gif|jpg|ico)(\?|$)/)) return;
  if (url.includes('google-analytics') || url.includes('baidu') || url.includes('telemetry')) return;

  const entry = {
    method, url,
    postData: req.postData()?.slice(0, 1000),
    time: new Date().toISOString()
  };
  captured.push(entry);

  // 高亮关键请求
  const path = url.replace('https://bigquant.com', '');
  const isKey = path.includes('task') || path.includes('run') || path.includes('submit') ||
    path.includes('paper') || path.includes('trading') || path.includes('kernel') ||
    path.includes('session') || path.includes('execute') || path.includes('aiflow') ||
    path.includes('mint') || path.includes('notebook') || path.includes('backtest');

  if (isKey) {
    interesting.push(entry);
    console.log(`\n🔑 [${method}] ${path}`);
    if (entry.postData) console.log(`   body: ${entry.postData.slice(0, 300)}`);
  }
});

context.on('response', async resp => {
  const url = resp.url();
  if (!url.includes('bigquant.com')) return;
  if (url.match(/\.(js|css|png|svg|woff|ttf|wasm|gif|jpg|ico)(\?|$)/)) return;

  const path = url.replace('https://bigquant.com', '');
  const isKey = path.includes('task') || path.includes('run') || path.includes('submit') ||
    path.includes('paper') || path.includes('trading') || path.includes('kernel') ||
    path.includes('session') || path.includes('execute') || path.includes('aiflow') ||
    path.includes('mint') || path.includes('notebook') || path.includes('backtest');

  if (isKey) {
    try {
      const body = await resp.text();
      console.log(`   ← ${resp.status()} ${body.slice(0, 400)}`);
      const entry = interesting.find(e => e.url === url && !e.response);
      if (entry) entry.response = { status: resp.status(), body: body.slice(0, 1000) };
    } catch(e) {}
  }
});

const page = await context.newPage();
console.log('打开 AIStudio...\n');
await page.goto(studioUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

console.log('='.repeat(60));
console.log('请在浏览器中操作:');
console.log('1. 等待 VS Code 加载完成');
console.log('2. 打开一个 .ipynb notebook');
console.log('3. 点击"提交模拟"按钮');
console.log('4. 观察控制台输出');
console.log('='.repeat(60));

const save = () => {
  const outPath = path.join(__dirname, '../data/captured-submit-api.json');
  fs.writeFileSync(outPath, JSON.stringify({ all: captured, interesting }, null, 2));
};

setInterval(save, 3000);

process.on('SIGINT', () => {
  save();
  const outPath = path.join(__dirname, '../data/captured-submit-api.json');
  console.log(`\n已保存到 ${outPath}`);
  console.log(`关键请求 ${interesting.length} 个，总请求 ${captured.length} 个`);
  browser.close().then(() => process.exit(0));
});

await new Promise(() => {});
