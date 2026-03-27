#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SESSION_FILE } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function captureJoinQuantSession(options = {}) {
  const username = process.env.JOINQUANT_USERNAME;
  const password = process.env.JOINQUANT_PASSWORD;
  const url = options.url || 'https://www.joinquant.com/algorithm/index/list';
  const headed = options.headed === true;

  if (!username || !password) {
    throw new Error('Missing JOINQUANT_USERNAME or JOINQUANT_PASSWORD in .env');
  }

  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  const page = await context.newPage();

  console.log('Navigating to JoinQuant...');
  await page.goto('https://www.joinquant.com/user/login/index?type=login');

  // Handle login
  await page.locator('text=密码登录').click();
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="pwd"]', password);
  await page.locator('input[type="checkbox"]').check();
  await page.click('button:has-text("登")');

  await page.waitForURL(u => !u.href.includes('/login/'), { timeout: 30000 });
  console.log('Logged in successfully.');

  await page.goto(url);
  await page.waitForTimeout(2000);

  const cookies = await context.cookies();
  const sessionPayload = {
    capturedAt: new Date().toISOString(),
    cookies: cookies
  };

  if (!fs.existsSync(path.dirname(SESSION_FILE))) {
    fs.mkdirSync(path.dirname(SESSION_FILE), { recursive: true });
  }
  fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionPayload, null, 2));
  console.log(`Session saved to ${SESSION_FILE}`);

  await browser.close();
  return sessionPayload;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  captureJoinQuantSession({ headed: process.argv.includes('--headed') }).catch(console.error);
}
