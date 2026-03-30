#!/usr/bin/env node
/**
 * 调试脚本：查看果仁网策略页面元素
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function debugPage() {
  // Load session
  let sessionPayload;
  if (fs.existsSync(SESSION_FILE)) {
    sessionPayload = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    console.log('Loaded session from', SESSION_FILE);
  } else {
    throw new Error('No session file found.');
  }

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  
  // Set cookies from session
  await context.addCookies(sessionPayload.cookies);
  
  const page = await context.newPage();

  console.log('Navigating to strategy page...');
  await page.goto('https://guorn.com/stock');
  await page.waitForTimeout(5000);

  // Take screenshot
  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'debug-step1.png'), fullPage: true });

  // List all buttons
  const buttons = await page.locator('button, a').all();
  console.log(`\nFound ${buttons.length} buttons/links`);
  
  for (let i = 0; i < Math.min(buttons.length, 30); i++) {
    try {
      const text = await buttons[i].textContent();
      const visible = await buttons[i].isVisible();
      if (visible && text.trim()) {
        console.log(`  [${i}] ${text.trim().slice(0, 50)}`);
      }
    } catch (e) {}
  }

  // List all inputs
  const inputs = await page.locator('input').all();
  console.log(`\nFound ${inputs.length} inputs`);
  
  for (let i = 0; i < Math.min(inputs.length, 20); i++) {
    try {
      const name = await inputs[i].getAttribute('name');
      const id = await inputs[i].getAttribute('id');
      const type = await inputs[i].getAttribute('type');
      const visible = await inputs[i].isVisible();
      if (visible) {
        console.log(`  [${i}] name=${name}, id=${id}, type=${type}`);
      }
    } catch (e) {}
  }

  // List all selects
  const selects = await page.locator('select').all();
  console.log(`\nFound ${selects.length} selects`);
  
  for (let i = 0; i < Math.min(selects.length, 10); i++) {
    try {
      const name = await selects[i].getAttribute('name');
      const id = await selects[i].getAttribute('id');
      const visible = await selects[i].isVisible();
      if (visible) {
        console.log(`  [${i}] name=${name}, id=${id}`);
        // List options
        const options = await selects[i].locator('option').all();
        for (let j = 0; j < Math.min(options.length, 5); j++) {
          const optText = await options[j].textContent();
          console.log(`      option[${j}]: ${optText?.trim().slice(0, 30)}`);
        }
      }
    } catch (e) {}
  }

  // Get HTML for analysis
  const html = await page.content();
  fs.writeFileSync(path.join(OUTPUT_ROOT, 'debug-page.html'), html);
  console.log('\nPage HTML saved to debug-page.html');

  console.log('\nDone. Browser will stay open for 30 seconds...');
  await page.waitForTimeout(30000);

  await browser.close();
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  debugPage().catch(console.error);
}
