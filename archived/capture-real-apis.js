import { chromium } from 'playwright';
import fs from 'node:fs';

async function captureRealAPIs() {
  console.log('=== Capturing Real RiceQuant APIs ===\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 捕获所有请求
  const apiRequests = [];
  page.on('request', request => {
    const url = request.url();
    // 过滤掉静态资源
    if (url.includes('.js') || url.includes('.css') || url.includes('.png') || 
        url.includes('.jpg') || url.includes('.svg') || url.includes('.woff')) {
      return;
    }
    // 只捕获ricequant域名的请求
    if (url.includes('ricequant.com')) {
      apiRequests.push({
        method: request.method(),
        url: url,
        postData: request.postData(),
        headers: request.headers()
      });
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
    await page.waitForTimeout(5000);
    
    // 列出捕获的API请求
    console.log('\n3. Captured API requests on strategy page:');
    const uniqueUrls = new Set();
    const filtered = apiRequests.filter(r => {
      if (uniqueUrls.has(r.url)) return false;
      uniqueUrls.add(r.url);
      // 排除登录检查等通用请求
      if (r.url.includes('isLogin.do') || r.url.includes('collect') || r.url.includes('plausible')) {
        return false;
      }
      return true;
    });
    
    filtered.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req.method} ${req.url}`);
      if (req.postData) {
        console.log(`     POST: ${req.postData.substring(0, 200)}`);
      }
    });
    
    // 保存到文件
    fs.writeFileSync('real-api-requests.json', JSON.stringify(filtered, null, 2));
    console.log('\n✓ Saved to real-api-requests.json');
    
    // 获取cookies
    const cookies = await context.cookies();
    console.log(`\n4. Cookies (${cookies.length}):`);
    cookies.forEach(c => {
      console.log(`  - ${c.name}: ${c.value.substring(0, 30)}...`);
    });
    
    // 保存cookies
    fs.writeFileSync('real-cookies.json', JSON.stringify(cookies, null, 2));
    console.log('✓ Saved to real-cookies.json');
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

captureRealAPIs();
