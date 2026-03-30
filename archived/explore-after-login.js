import { chromium } from 'playwright';
import fs from 'node:fs';

async function exploreAfterLogin() {
  console.log('=== Exploring RiceQuant After Login ===\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 拦截请求
  const requests = [];
  page.on('request', request => {
    const url = request.url();
    if (url.includes('api') || url.includes('.do') || url.includes('quant')) {
      requests.push({
        method: request.method(),
        url: url,
        postData: request.postData()
      });
    }
  });
  
  try {
    console.log('Opening login page...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    // 登录
    console.log('Logging in...');
    const loginBtn = await page.$('button:has-text("登录")');
    if (loginBtn) {
      await loginBtn.click();
      await page.waitForTimeout(2000);
    }
    
    // 切换到密码登录
    const passwordOption = await page.locator('text=密码登录').first();
    if (await passwordOption.count() > 0) {
      await passwordOption.click();
      await page.waitForTimeout(1000);
    }
    
    await page.waitForSelector('input[type="password"]', { timeout: 5000, state: 'visible' });
    
    // 填写表单
    const usernameInput = await page.$('input[placeholder="国内手机号或邮箱"]');
    const passwordInput = await page.$('input[type="password"][placeholder*="密码"]');
    await usernameInput.fill('13311390323');
    await passwordInput.fill('3228552');
    
    // 点击登录
    const loginSubmitBtn = await page.locator('button:has-text("登录/注册")').first();
    await loginSubmitBtn.click({ force: true });
    
    console.log('Waiting for redirect...');
    await page.waitForTimeout(5000);
    
    const currentUrl = page.url();
    console.log(`Current URL: ${currentUrl}`);
    
    // 检查页面内容
    if (currentUrl.includes('/welcome') || currentUrl.includes('/login')) {
      console.log('\nStill on welcome/login page. Checking if login actually succeeded...');
      
      // 检查是否有错误提示
      const errors = await page.$$('.el-message--error, .error, .login-failed');
      if (errors.length > 0) {
        for (const err of errors) {
          const text = await err.textContent();
          console.log(`Error message: ${text}`);
        }
      }
    } else {
      console.log('✓ Redirected to main page!');
    }
    
    // 访问量化页面
    console.log('\nNavigating to quant page...');
    await page.goto('https://www.ricequant.com/quant', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    console.log(`URL after navigation: ${page.url()}`);
    
    // 列出捕获的API请求
    console.log('\nCaptured API requests:');
    const uniqueRequests = [...new Map(requests.map(r => [r.url, r])).values()];
    uniqueRequests.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req.method} ${req.url}`);
      if (req.postData) {
        console.log(`     POST: ${req.postData.substring(0, 100)}`);
      }
    });
    
    // 保存完整请求列表
    fs.writeFileSync('api-requests.json', JSON.stringify(uniqueRequests, null, 2));
    console.log('\n✓ Saved to api-requests.json');
    
    // 获取cookies
    const cookies = await context.cookies();
    fs.writeFileSync('cookies.json', JSON.stringify(cookies, null, 2));
    console.log(`✓ Saved ${cookies.length} cookies to cookies.json`);
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

exploreAfterLogin();
