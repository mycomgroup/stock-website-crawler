#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function analyzeBacktestAPI(options = {}) {
  const headed = options.headed === true;
  const apiCalls = [];

  // Load session
  let sessionPayload;
  if (fs.existsSync(SESSION_FILE)) {
    sessionPayload = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    console.log('Loaded session from', SESSION_FILE);
  } else {
    throw new Error('No session file found. Run capture-session.js first.');
  }

  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  
  // Set cookies from session
  await context.addCookies(sessionPayload.cookies);
  
  const page = await context.newPage();

  // Intercept network requests
  page.on('request', request => {
    const url = request.url();
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

  page.on('response', async response => {
    const url = response.url();
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
      const entry = apiCalls.findLast(r => r.url === url && r.type === 'request');
      if (entry) {
        entry.statusCode = response.status();
        try {
          entry.responseBody = await response.text();
        } catch (e) {}
      }
    }
  });

  console.log('Navigating to strategy page...');
  await page.goto('https://guorn.com/stock');
  await page.waitForTimeout(3000);

  // Check if still logged in
  const isLoggedIn = !page.url().includes('/user/login');
  console.log('Logged in:', isLoggedIn);

  if (!isLoggedIn) {
    console.log('Session expired, need to re-login');
    await browser.close();
    return;
  }

  // Run backtest
  console.log('Running backtest...');
  const backtestButton = page.locator('button:has-text("开始回测"), a:has-text("开始回测")').first();
  if (await backtestButton.isVisible({ timeout: 5000 }).catch(() => false)) {
    console.log('Found backtest button, clicking...');
    await backtestButton.click();
    await page.waitForTimeout(10000);
  } else {
    console.log('Backtest button not found');
  }

  // Save captured API calls
  const apiCallsFile = path.join(DATA_ROOT, 'backtest-api-calls.json');
  fs.mkdirSync(DATA_ROOT, { recursive: true });
  fs.writeFileSync(apiCallsFile, JSON.stringify(apiCalls, null, 2));
  console.log(`API calls saved to ${apiCallsFile}`);

  // Print summary of API calls
  console.log('\n=== API Call Summary ===');
  const uniqueUrls = [...new Set(apiCalls.map(r => r.url))];
  for (const url of uniqueUrls) {
    const calls = apiCalls.filter(r => r.url === url);
    const methods = [...new Set(calls.map(r => r.method))];
    console.log(`${methods.join(',')} ${url}`);
  }

  await browser.close();
  return apiCalls;
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  analyzeBacktestAPI({ headed: process.argv.includes('--headed') }).catch(console.error);
}
