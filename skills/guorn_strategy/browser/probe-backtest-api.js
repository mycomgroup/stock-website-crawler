#!/usr/bin/env node
/**
 * 探测果仁网回测 API 的真实请求格式
 * 策略：加载页面后通过 JS 拦截 XMLHttpRequest 和 fetch，然后触发回测
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE } from '../paths.js';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));

const browser = await chromium.launch({ headless: false }); // headed 模式，方便观察
const ctx = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
});
await ctx.addCookies(session.cookies);
const page = await ctx.newPage();

// 拦截所有网络请求
const captured = [];
page.on('request', req => {
  if (req.url().includes('guorn.com') && !req.url().includes('static') && !req.url().includes('google')) {
    captured.push({
      method: req.method(),
      url: req.url(),
      body: req.postData(),
      headers: req.headers()
    });
  }
});
page.on('response', async resp => {
  if (resp.url().includes('guorn.com') && !resp.url().includes('static') && !resp.url().includes('google')) {
    const entry = captured.findLast(r => r.url === resp.url());
    if (entry) {
      entry.status = resp.status();
      try { entry.response = await resp.text(); } catch {}
    }
  }
});

console.log('Loading strategy page...');
await page.goto('https://guorn.com/stock');
await page.waitForTimeout(5000);

// 注入 XHR 拦截器
await page.evaluate(() => {
  const origOpen = XMLHttpRequest.prototype.open;
  const origSend = XMLHttpRequest.prototype.send;
  window._xhrLog = [];
  
  XMLHttpRequest.prototype.open = function(method, url, ...args) {
    this._method = method;
    this._url = url;
    return origOpen.apply(this, [method, url, ...args]);
  };
  
  XMLHttpRequest.prototype.send = function(body) {
    window._xhrLog.push({ method: this._method, url: this._url, body });
    return origSend.apply(this, [body]);
  };
  
  // 也拦截 fetch
  const origFetch = window.fetch;
  window.fetch = async function(url, opts = {}) {
    window._xhrLog.push({ method: opts.method || 'GET', url, body: opts.body });
    return origFetch.apply(this, [url, opts]);
  };
  
  console.log('XHR interceptor installed');
});

// 检查页面状态
const pageTitle = await page.title();
console.log('Page title:', pageTitle);

// 找所有可见的按钮
const allBtns = await page.locator('a:visible, button:visible').all();
console.log('Visible buttons/links:', allBtns.length);
for (const btn of allBtns.slice(0, 20)) {
  const txt = await btn.textContent().catch(() => '');
  if (txt.trim()) console.log(' -', JSON.stringify(txt.trim().slice(0, 40)));
}

// 截图
fs.mkdirSync(DATA_ROOT, { recursive: true });
await page.screenshot({ path: path.join(DATA_ROOT, 'probe-state.png'), fullPage: true });
console.log('Screenshot saved to data/probe-state.png');

// 等待用户手动操作（如果 headed 模式）
console.log('\nWaiting 30s for manual interaction...');
console.log('Please click "开始回测" in the browser window');
await page.waitForTimeout(30000);

// 获取拦截到的 XHR
const xhrLog = await page.evaluate(() => window._xhrLog || []);
console.log('\nXHR/fetch calls captured:', xhrLog.length);
xhrLog.filter(r => r.method === 'POST').forEach(r => {
  console.log('POST', r.url);
  if (r.body) console.log('body:', String(r.body).slice(0, 300));
});

// 保存所有捕获的请求
const allData = { playwright: captured, xhr: xhrLog };
fs.writeFileSync(path.join(DATA_ROOT, 'probed-requests.json'), JSON.stringify(allData, null, 2));
console.log('Saved to data/probed-requests.json');

await browser.close();

