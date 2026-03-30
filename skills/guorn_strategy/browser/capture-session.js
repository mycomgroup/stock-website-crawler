#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function captureGuornSession(options = {}) {
  const username = process.env.GUORN_USERNAME;
  const password = process.env.GUORN_PASSWORD;
  const headed = options.headed === true;

  if (!username || !password) {
    throw new Error('Missing GUORN_USERNAME or GUORN_PASSWORD in .env');
  }

  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  const page = await context.newPage();

  console.log('Navigating to Guorn login page...');
  await page.goto('https://guorn.com/user/login');
  await page.waitForTimeout(3000);

  console.log('Logging in...');
  // Fill phone/email input
  const phoneInput = page.locator('#login-Id');
  await phoneInput.fill(username);

  // Fill password input
  const passwordInput = page.locator('#login-password');
  await passwordInput.fill(password);

  // Click login button
  const loginButton = page.locator('button[type="submit"]:has-text("登录")');
  await loginButton.click();

  await page.waitForTimeout(5000);
  console.log('Login attempted, current URL:', page.url());

  // Check if login was successful
  const isLoggedIn = !page.url().includes('/user/login');
  console.log('Login successful:', isLoggedIn);

  if (!isLoggedIn) {
    // Take screenshot for debugging
    const screenshotPath = path.join(DATA_ROOT, 'login-failed.png');
    await page.screenshot({ path: screenshotPath });
    console.log(`Login failed, screenshot saved to ${screenshotPath}`);
    await browser.close();
    throw new Error('Login failed');
  }

  // Save cookies
  const cookies = await context.cookies();
  const sessionPayload = {
    capturedAt: new Date().toISOString(),
    cookies: cookies
  };
  const sessionFile = path.join(DATA_ROOT, 'session.json');
  fs.mkdirSync(DATA_ROOT, { recursive: true });
  fs.writeFileSync(sessionFile, JSON.stringify(sessionPayload, null, 2));
  console.log(`Session saved to ${sessionFile}`);

  await browser.close();
  return sessionPayload;
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  captureGuornSession({ headed: process.argv.includes('--headed') }).catch(console.error);
}
