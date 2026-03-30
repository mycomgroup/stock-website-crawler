#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function analyzeGuornLoginAPI(options = {}) {
  const username = process.env.GUORN_USERNAME;
  const password = process.env.GUORN_PASSWORD;
  const headed = options.headed === true;

  if (!username || !password) {
    throw new Error('Missing GUORN_USERNAME or GUORN_PASSWORD in .env');
  }

  const apiCalls = [];

  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  const page = await context.newPage();

  // Intercept network requests
  page.on('request', request => {
    const url = request.url();
    // Only capture guorn.com API calls
    if (url.includes('guorn.com') && 
        !url.includes('.css') && 
        !url.includes('.js') && 
        !url.includes('.png') && 
        !url.includes('.jpg') && 
        !url.includes('.gif') && 
        !url.includes('.woff') &&
        !url.includes('.woff2') &&
        !url.includes('.ttf') &&
        !url.includes('google-analytics') &&
        !url.includes('googleapis')) {
      apiCalls.push({
        type: 'request',
        method: request.method(),
        url: url,
        headers: request.headers(),
        postData: request.postData(),
        timestamp: new Date().toISOString()
      });
    }
  });

  // Capture response body for login API
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('guorn.com/user/login') && response.request().method() === 'POST') {
      try {
        const body = await response.text();
        const entry = apiCalls.findLast(r => r.url === url && r.type === 'request');
        if (entry) {
          entry.responseBody = body;
        }
      } catch (e) {}
    }
  });

  console.log('Navigating to Guorn login page...');
  await page.goto('https://guorn.com/user/login');
  await page.waitForTimeout(3000);

  console.log('Logging in...');
  // Try to find and click password login tab
  try {
    const tabs = await page.locator('a, div, span, button').filter({ hasText: '密码登录' }).all();
    for (const tab of tabs) {
      if (await tab.isVisible()) {
        console.log('Found password login tab, clicking...');
        await tab.click();
        await page.waitForTimeout(1500);
        break;
      }
    }
  } catch (e) {
    console.log('No password tab found, trying direct login...');
  }

  // Try multiple selectors for phone input
  const phoneSelectors = [
    'input[name="account"]',
    'input[placeholder*="手机"]',
    'input[placeholder*="账号"]',
    'input[type="text"]'
  ];
  
  let phoneInput;
  for (const sel of phoneSelectors) {
    const input = page.locator(sel).first();
    if (await input.isVisible({ timeout: 2000 }).catch(() => false)) {
      phoneInput = input;
      console.log(`Found phone input with selector: ${sel}`);
      break;
    }
  }
  
  if (!phoneInput) {
    throw new Error('Could not find phone input field');
  }
  await phoneInput.fill(username);

  // Fill password
  const passwordInput = page.locator('input[type="password"]:visible').first();
  await passwordInput.fill(password);

  // Click login button
  const loginButton = page.locator('button:visible:has-text("登录"), input[type="submit"]:visible').first();
  await loginButton.click();

  await page.waitForTimeout(5000);
  console.log('Login attempted, current URL:', page.url());

  // Check if login was successful
  const isLoggedIn = !page.url().includes('/user/login');
  console.log('Login successful:', isLoggedIn);

  // Save captured API calls
  const apiCallsFile = path.join(DATA_ROOT, 'login-api-calls.json');
  fs.mkdirSync(DATA_ROOT, { recursive: true });
  fs.writeFileSync(apiCallsFile, JSON.stringify(apiCalls, null, 2));
  console.log(`API calls saved to ${apiCallsFile}`);

  // Save cookies
  const cookies = await context.cookies();
  const sessionPayload = {
    capturedAt: new Date().toISOString(),
    cookies: cookies
  };
  const sessionFile = path.join(DATA_ROOT, 'session.json');
  fs.writeFileSync(sessionFile, JSON.stringify(sessionPayload, null, 2));
  console.log(`Session saved to ${sessionFile}`);

  await browser.close();
  return { apiCalls, sessionPayload, isLoggedIn };
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  analyzeGuornLoginAPI({ headed: process.argv.includes('--headed') }).catch(console.error);
}
