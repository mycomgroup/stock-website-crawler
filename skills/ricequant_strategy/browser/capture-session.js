import { chromium } from 'playwright';

const API_BASE = 'https://www.ricequant.com/api';

/**
 * 通过API直接登录RiceQuant
 * RiceQuant使用JWT token认证，不需要浏览器模拟
 */
export async function captureRiceQuantSession(credentials) {
  console.log('Authenticating with RiceQuant API...');
  
  try {
    // 尝试直接通过API登录
    const loginResponse = await fetch(`${API_BASE}/v2/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
      },
      body: JSON.stringify({
        username: credentials.username,
        password: credentials.password
      })
    });
    
    if (!loginResponse.ok) {
      const errorText = await loginResponse.text();
      throw new Error(`Login failed: ${loginResponse.status} - ${errorText}`);
    }
    
    const loginData = await loginResponse.json();
    console.log('API login successful');
    
    // 构造类似cookie的会话数据
    const cookies = [
      {
        name: 'session',
        value: loginData.token || loginData.access_token || loginData.session,
        domain: 'ricequant.com',
        path: '/'
      }
    ];
    
    return {
      cookies,
      csrfToken: loginData.csrf_token || '',
      token: loginData.token || loginData.access_token || '',
      timestamp: Date.now()
    };
    
  } catch (apiError) {
    console.log('API login failed, trying browser automation...', apiError.message);
    
    // 如果API登录失败，尝试浏览器方式
    return await captureViaBrowser(credentials);
  }
}

/**
 * 通过浏览器捕获会话（备用方案）
 */
async function captureViaBrowser(credentials) {
  console.log('Launching browser for RiceQuant...');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    // 访问登录页面
    console.log('Navigating to ricequant.com/login...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    
    // 等待SPA加载
    await page.waitForTimeout(3000);
    
    // 点击登录按钮打开模态框
    console.log('Looking for login button...');
    const loginBtn = await page.$('button:has-text("登录")');
    if (loginBtn) {
      await loginBtn.click();
      console.log('Clicked login button');
      await page.waitForTimeout(3000);
    }
    
    // 截图查看当前状态
    await page.screenshot({ path: 'login-step1.png' });
    console.log('✓ Screenshot saved to login-step1.png');
    
    console.log('Looking for visible login form...');
    
    // 切换到密码登录模式
    console.log('Switching to password login mode...');
    const passwordOption = await page.locator('text=密码登录').first();
    if (await passwordOption.count() > 0) {
      await passwordOption.click();
      console.log('✓ Switched to password login mode');
      await page.waitForTimeout(1000);
    }
    
    // 等待密码输入框出现
    await page.waitForSelector('input[type="password"]', { timeout: 5000, state: 'visible' });
    
    // RiceQuant的密码登录模式有：
    // - 输入框5: type=text, placeholder=国内手机号或邮箱
    // - 输入框8: type=password, placeholder=密码 (不少于6位)
    
    const usernameInput = await page.$('input[placeholder="国内手机号或邮箱"]');
    const passwordInput = await page.$('input[type="password"][placeholder*="密码"]');
    
    if (!usernameInput) {
      throw new Error('Could not find username input field');
    }
    if (!passwordInput) {
      throw new Error('Could not find password input field');
    }
    
    // 填写账号
    await usernameInput.click();
    await usernameInput.fill(credentials.username);
    console.log('✓ Filled username');
    
    // 填写密码
    await passwordInput.click();
    await passwordInput.fill(credentials.password);
    console.log('✓ Filled password');
    
    // 截图查看填写状态
    await page.screenshot({ path: 'login-step2.png' });
    console.log('✓ Screenshot saved to login-step2.png');
    
    // 点击模态框内的登录按钮
    const loginSubmitBtn = await page.$('.el-dialog.user-status button.btn--submit');
    if (loginSubmitBtn) {
      await loginSubmitBtn.click();
      console.log('✓ Clicked login button');
    } else {
      // 备用方案
      const modalBtns = await page.$$('.el-dialog.user-status button');
      for (const btn of modalBtns) {
        const text = await btn.textContent();
        const visible = await btn.isVisible();
        if (visible && text && text.trim() === '登录') {
          await btn.click();
          console.log('✓ Clicked login button (fallback)');
          break;
        }
      }
    }
    
    // 等待登录完成
    console.log('Waiting for login to complete...');
    await page.waitForTimeout(5000);
    
    // 检查是否登录成功
    const currentUrl = page.url();
    console.log(`Current URL: ${currentUrl}`);
    
    if (!currentUrl.includes('/login')) {
      console.log('✓ Login successful!');
    }
    
    // 获取cookies
    const cookies = await context.cookies();
    console.log(`✓ Captured ${cookies.length} cookies`);
    
    return {
      cookies,
      csrfToken: '',
      timestamp: Date.now()
    };
    
  } catch (error) {
    console.error('Browser capture failed:', error);
    await page.screenshot({ path: 'login-error.png', fullPage: true });
    throw error;
  } finally {
    await browser.close();
  }
}
