#!/usr/bin/env node
/**
 * 探测果仁网回测 API 的真实请求格式
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE } from '../paths.js';

async function probe() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const requests = [];

  const browser = await chromium.launch({ headless: false });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  await ctx.addCookies(session.cookies);
  const page = await ctx.newPage();

  page.on('request', req => {
    const url = req.url();
    if (url.includes('guorn.com') && !url.includes('static') && !url.includes('google')) {
      requests.push({ method: req.method(), url, body: req.postData(), headers: req.headers() });
    }
  });
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('guorn.com') && !url.includes('static') && !url.includes('google')) {
      const entry = requests.findLast(r => r.url === url);
      if (entry) {
        entry.status = resp.status();
        try { entry.response = (await resp.text()).slice(0, 500); } catch {}
      }
    }
  });

  console.log('Loading strategy page...');
  await page.goto('https://guorn.com/stock');
  await page.waitForTimeout(4000);

  fs.mkdirSync(DATA_ROOT, { recursive: true });
  await page.screenshot({ path: path.join(DATA_ROOT, 'probe-1-loaded.png') });

  // 点击"创建策略"
  const createBtn = page.locator('a:has-text("创建策略"), button:has-text("创建策略")').first();
  if (await createBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    console.log('Clicking 创建策略...');
    await createBtn.click();
    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(DATA_ROOT, 'probe-2-created.png') });
  }

  // 找回测按钮
  const backtestBtn = page.locator('a:has-text("开始回测"), button:has-text("开始回测")').first();
  const visible = await backtestBtn.isVisible({ timeout: 5000 }).catch(() => false);
  console.log('Backtest button visible:', visible);

  if (visible) {
    console.log('Clicking 开始回测...');
    await backtestBtn.click();
    await page.waitForTimeout(15000);
    await page.screenshot({ path: path.join(DATA_ROOT, 'probe-3-backtest.png') });
  } else {
    console.log('Backtest button not found, waiting 30s for manual interaction...');
    await page.waitForTimeout(30000);
  }

  // 输出所有 POST 请求
  const posts = requests.filter(r => r.method === 'POST');
  console.log('\nPOST requests:', posts.length);
  for (const r of posts) {
    console.log('---');
    console.log('URL:', r.url);
    console.log('Status:', r.status);
    if (r.body) console.log('Body:', r.body.slice(0, 500));
    if (r.response) console.log('Response:', r.response.slice(0, 200));
  }

  console.log('\nAll guorn.com requests:', requests.length);
  requests.forEach(r => console.log(r.method, r.url.replace('https://guorn.com', '')));

  fs.writeFileSync(path.join(DATA_ROOT, 'probed-requests.json'), JSON.stringify(requests, null, 2));
  console.log('\nSaved to data/probed-requests.json');

  await browser.close();
}

probe().catch(console.error);
