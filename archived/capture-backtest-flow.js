import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

async function captureBacktestFlow() {
  console.log('=== Capturing RiceQuant Backtest Flow ===\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 捕获所有请求
  const apiRequests = [];
  page.on('request', request => {
    const url = request.url();
    if (url.includes('ricequant.com/api') || url.includes('.do')) {
      apiRequests.push({
        method: request.method(),
        url: url,
        postData: request.postData(),
        headers: request.headers()
      });
    }
  });
  
  // 捕获响应
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('ricequant.com/api')) {
      try {
        const body = await response.text();
        if (body.length < 5000) {
          console.log(`Response ${response.status()}: ${url}`);
          console.log(`  ${body.substring(0, 200)}`);
        }
      } catch (e) {}
    }
  });
  
  try {
    // 登录流程
    console.log('1. Logging in...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    const loginBtn = await page.$('button:has-text("登录")');
    if (loginBtn) await loginBtn.click();
    await page.waitForTimeout(2000);
    
    const passwordOption = await page.locator('text=密码登录').first();
    if (await passwordOption.count() > 0) {
      await passwordOption.click();
      await page.waitForTimeout(1000);
    }
    
    await page.waitForSelector('input[type="password"]', { timeout: 5000, state: 'visible' });
    
    const usernameInput = await page.$('input[placeholder="国内手机号或邮箱"]');
    const passwordInput = await page.$('input[type="password"][placeholder*="密码"]');
    await usernameInput.fill('13311390323');
    await passwordInput.fill('3228552');
    
    const loginSubmitBtn = await page.$('.el-dialog.user-status button.btn--submit');
    if (loginSubmitBtn) {
      await loginSubmitBtn.click();
      console.log('✓ Login button clicked');
    }
    
    await page.waitForTimeout(5000);
    
    // 清除之前的请求
    apiRequests.length = 0;
    
    // 导航到策略页面
    console.log('\n2. Navigating to strategy page...');
    await page.goto('https://www.ricequant.com/quant/strategys', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    // 点击"新建策略"按钮
    console.log('\n3. Looking for "New Strategy" button...');
    await page.screenshot({ path: 'strategies-page.png' });
    
    const newBtnSelectors = [
      'button:has-text("新建")',
      'button:has-text("创建")',
      'button:has-text("新建策略")',
      'a:has-text("新建")',
      '.el-button:has-text("新建")',
      '[class*="create"]',
      '[class*="new"]'
    ];
    
    let foundNewBtn = false;
    for (const selector of newBtnSelectors) {
      try {
        const btn = await page.$(selector);
        if (btn && await btn.isVisible()) {
          await btn.click();
          console.log(`✓ Clicked: ${selector}`);
          foundNewBtn = true;
          break;
        }
      } catch (e) {}
    }
    
    if (!foundNewBtn) {
      console.log('Could not find "New Strategy" button');
      // 列出所有可见按钮
      const buttons = await page.$$('button');
      console.log('\nVisible buttons:');
      for (const btn of buttons) {
        if (await btn.isVisible()) {
          const text = await btn.textContent();
          console.log(`  - "${text?.trim()}"`);
        }
      }
    }
    
    await page.waitForTimeout(3000);
    
    // 列出捕获的API请求
    console.log('\n4. Captured API requests:');
    const uniqueUrls = new Set();
    const filtered = apiRequests.filter(r => {
      if (uniqueUrls.has(r.url)) return false;
      uniqueUrls.add(r.url);
      return true;
    });
    
    filtered.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req.method} ${req.url}`);
      if (req.postData) {
        console.log(`     POST: ${req.postData.substring(0, 300)}`);
      }
    });
    
    // 保存到文件
    fs.writeFileSync('backtest-flow-requests.json', JSON.stringify(filtered, null, 2));
    console.log('\n✓ Saved to backtest-flow-requests.json');
    
    await page.screenshot({ path: 'after-new-btn.png' });
    console.log('✓ Screenshot saved to after-new-btn.png');
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

captureBacktestFlow();
