import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '.env') });

async function analyzePage() {
  const browser = await chromium.launch({ 
    headless: true,
    slowMo: 100
  });
  
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  
  console.log('1. Navigating to RiceQuant...');
  await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle' });
  
  console.log('2. Clicking login button...');
  await page.click('button:has-text("登录")');
  await page.waitForTimeout(1000);
  
  console.log('3. Clicking password login tab...');
  await page.click('text=密码登录');
  await page.waitForTimeout(500);
  
  console.log('\n=== Analyzing Login Form ===\n');
  
  // 获取所有 input 元素
  const inputs = await page.$$('input');
  console.log(`Found ${inputs.length} input elements:\n`);
  
  for (let i = 0; i < inputs.length; i++) {
    const input = inputs[i];
    const tagName = await input.evaluate(el => el.tagName);
    const type = await input.getAttribute('type') || 'text';
    const name = await input.getAttribute('name') || '';
    const placeholder = await input.getAttribute('placeholder') || '';
    const className = await input.getAttribute('class') || '';
    const id = await input.getAttribute('id') || '';
    const isVisible = await input.isVisible();
    
    console.log(`Input ${i + 1}:`);
    console.log(`  Type: ${type}`);
    console.log(`  Name: ${name}`);
    console.log(`  Placeholder: ${placeholder}`);
    console.log(`  Class: ${className.substring(0, 50)}...`);
    console.log(`  ID: ${id}`);
    console.log(`  Visible: ${isVisible}`);
    console.log('');
  }
  
  // 获取所有 button 元素
  const buttons = await page.$$('button');
  console.log(`\nFound ${buttons.length} button elements:\n`);
  
  for (let i = 0; i < buttons.length; i++) {
    const button = buttons[i];
    const text = await button.textContent() || '';
    const type = await button.getAttribute('type') || '';
    const className = await button.getAttribute('class') || '';
    const isVisible = await button.isVisible();
    
    console.log(`Button ${i + 1}:`);
    console.log(`  Text: ${text.trim()}`);
    console.log(`  Type: ${type}`);
    console.log(`  Class: ${className.substring(0, 50)}...`);
    console.log(`  Visible: ${isVisible}`);
    console.log('');
  }
  
  // 保存页面 HTML
  const html = await page.content();
  fs.writeFileSync(path.join(__dirname, 'data', 'login-form.html'), html);
  console.log('\nHTML saved to data/login-form.html');
  
  // 截图
  await page.screenshot({ path: path.join(__dirname, 'data', 'login-form.png') });
  console.log('Screenshot saved to data/login-form.png');
  
  // 等待用户查看
  console.log('\nWaiting 30 seconds for manual inspection...');
  await page.waitForTimeout(30000);
  
  await browser.close();
}

analyzePage().catch(console.error);