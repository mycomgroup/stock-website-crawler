#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function debugGuornLogin(options = {}) {
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

  // Debug: List all visible elements
  console.log('\n=== Page Content Summary ===');
  
  // Find all input fields
  const inputs = await page.locator('input:visible').all();
  console.log('\nVisible inputs:');
  for (const input of inputs) {
    const type = await input.getAttribute('type');
    const name = await input.getAttribute('name');
    const placeholder = await input.getAttribute('placeholder');
    const id = await input.getAttribute('id');
    console.log(`  - type=${type}, name=${name}, placeholder=${placeholder}, id=${id}`);
  }

  // Find all buttons
  const buttons = await page.locator('button:visible, input[type="submit"]:visible').all();
  console.log('\nVisible buttons:');
  for (const btn of buttons) {
    const text = await btn.textContent();
    const type = await btn.getAttribute('type');
    console.log(`  - text="${text?.trim()}", type=${type}`);
  }

  // Find all links with "登录" text
  const links = await page.locator('a:visible, span:visible, div:visible').filter({ hasText: '登录' }).all();
  console.log('\nElements with "登录" text:');
  for (const link of links) {
    const tag = await link.evaluate(el => el.tagName);
    const text = await link.textContent();
    console.log(`  - tag=${tag}, text="${text?.trim().slice(0, 50)}"`);
  }

  // Try to click password login tab
  console.log('\n=== Attempting Login ===');
  try {
    const passwordTab = page.locator('text=密码登录').first();
    if (await passwordTab.isVisible({ timeout: 2000 })) {
      console.log('Clicking password login tab...');
      await passwordTab.click();
      await page.waitForTimeout(1500);
    }
  } catch (e) {
    console.log('No password tab found');
  }

  // Find and fill phone input
  const phoneInput = page.locator('input[name="account"]').first();
  if (await phoneInput.isVisible({ timeout: 2000 }).catch(() => false)) {
    console.log('Filling phone input...');
    await phoneInput.fill(username);
  } else {
    console.log('Phone input not visible');
  }

  // Find and fill password input
  const passwordInput = page.locator('input[type="password"]:visible').first();
  if (await passwordInput.isVisible({ timeout: 2000 }).catch(() => false)) {
    console.log('Filling password input...');
    await passwordInput.fill(password);
  } else {
    console.log('Password input not visible');
  }

  // Find and click login button
  const loginButton = page.locator('button:visible').filter({ hasText: '登录' }).first();
  if (await loginButton.isVisible({ timeout: 2000 }).catch(() => false)) {
    console.log('Clicking login button...');
    await loginButton.click();
    await page.waitForTimeout(5000);
  } else {
    console.log('Login button not visible');
  }

  console.log('\n=== Login Result ===');
  console.log('Current URL:', page.url());
  console.log('Login successful:', !page.url().includes('/user/login'));

  // Save cookies
  const cookies = await context.cookies();
  const sessionPayload = {
    capturedAt: new Date().toISOString(),
    cookies: cookies
  };
  const sessionFile = path.join(DATA_ROOT, 'session.json');
  fs.mkdirSync(DATA_ROOT, { recursive: true });
  fs.writeFileSync(sessionFile, JSON.stringify(sessionPayload, null, 2));
  console.log(`\nSession saved to ${sessionFile}`);

  await browser.close();
  return { isLoggedIn: !page.url().includes('/user/login'), sessionPayload };
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  debugGuornLogin({ headed: process.argv.includes('--headed') }).catch(console.error);
}
