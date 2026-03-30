import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '.env') });

const SESSION_FILE = path.join(__dirname, 'data', 'session.json');
const AUTH_STATE_FILE = path.join(__dirname, 'data', 'auth-state.json');
const SCREENSHOT_DIR = path.join(__dirname, 'data', 'screenshots');

class RiceQuantAuth {
  constructor() {
    this.username = process.env.RICEQUANT_USERNAME;
    this.password = process.env.RICEQUANT_PASSWORD;
    
    if (!this.username || !this.password) {
      throw new Error('RICEQUANT_USERNAME and RICEQUANT_PASSWORD must be set in .env');
    }
    
    console.log('Username:', this.username);
    
    // 确保目录存在
    if (!fs.existsSync(SCREENSHOT_DIR)) {
      fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    }
    if (!fs.existsSync(path.dirname(SESSION_FILE))) {
      fs.mkdirSync(path.dirname(SESSION_FILE), { recursive: true });
    }
  }

  async takeScreenshot(page, name) {
    const timestamp = Date.now();
    const filepath = path.join(SCREENSHOT_DIR, `${name}-${timestamp}.png`);
    await page.screenshot({ path: filepath, fullPage: false });
    console.log('  Screenshot:', filepath);
    return filepath;
  }

  async saveAuthState(context, metadata = {}) {
    // 保存 Playwright state
    const state = await context.storageState();
    const stateData = {
      ...state,
      savedAt: new Date().toISOString(),
      metadata
    };
    fs.writeFileSync(AUTH_STATE_FILE, JSON.stringify(stateData, null, 2));
    console.log('  Auth state saved:', AUTH_STATE_FILE);
    
    // 同时保存为 session.json 格式
    const sessionData = {
      cookies: state.cookies,
      timestamp: Date.now(),
      savedAt: new Date().toISOString()
    };
    fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
    console.log('  Session saved:', SESSION_FILE);
  }

  async checkLoginStatus(page) {
    try {
      // 方法1: 检查 URL
      const url = page.url();
      console.log('  Current URL:', url);
      
      if (url.includes('/workspace') || url.includes('/strategy')) {
        return true;
      }
      
      // 方法2: 检查是否有用户头像/用户名显示
      const userElement = await page.$('[class*="avatar"], [class*="user-name"], [class*="username"]');
      if (userElement) {
        return true;
      }
      
      // 方法3: 调用 API 检查
      const loginStatus = await page.evaluate(async () => {
        try {
          const response = await fetch('/api/user/isLogin.do', { method: 'POST' });
          return await response.json();
        } catch {
          return { code: -1 };
        }
      });
      
      return loginStatus.code === 0;
    } catch (e) {
      console.log('  Check login error:', e.message);
      return false;
    }
  }

  async doLogin(page) {
    console.log('\n=== Starting Login Process ===\n');
    
    // 1. 访问首页
    console.log('1. Navigating to RiceQuant...');
    await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle', timeout: 30000 });
    await this.takeScreenshot(page, '01-homepage');
    
    // 2. 点击登录按钮
    console.log('2. Clicking login button...');
    
    const loginButtonSelectors = [
      'button:has-text("登录")',
      'a:has-text("登录")',
      '[class*="login"]:has-text("登录")',
      'text=登录'
    ];
    
    for (const selector of loginButtonSelectors) {
      try {
        const btn = await page.$(selector);
        if (btn && await btn.isVisible()) {
          await btn.click();
          console.log('  Clicked:', selector);
          break;
        }
      } catch (e) {}
    }
    
    await page.waitForTimeout(1500);
    await this.takeScreenshot(page, '02-login-modal');
    
    // 3. 切换到密码登录（如果需要）
    console.log('3. Checking for password login tab...');
    
    const passwordTabSelectors = [
      'text=密码登录',
      'text=账号密码登录',
      '[class*="password"]:has-text("密码")',
      'li:has-text("密码")',
      'span:has-text("密码")'
    ];
    
    for (const selector of passwordTabSelectors) {
      try {
        const tab = await page.$(selector);
        if (tab && await tab.isVisible()) {
          await tab.click();
          console.log('  Clicked password tab:', selector);
          await page.waitForTimeout(500);
          break;
        }
      } catch (e) {}
    }
    
    await this.takeScreenshot(page, '03-password-form');
    
    // 4. 填写用户名
    console.log('4. Filling username...');
    
    const usernameSelectors = [
      'input[placeholder*="手机"]',
      'input[placeholder*="用户"]',
      'input[placeholder*="账号"]',
      'input[name="username"]',
      'input[name="mobile"]',
      'input[name="phone"]',
      'input[type="text"]',
      'input[type="tel"]'
    ];
    
    let usernameFilled = false;
    for (const selector of usernameSelectors) {
      try {
        const input = await page.$(selector);
        if (input && await input.isVisible()) {
          await input.click();
          await input.fill('');
          await input.type(this.username, { delay: 50 });
          console.log('  Filled username with:', selector);
          usernameFilled = true;
          break;
        }
      } catch (e) {}
    }
    
    if (!usernameFilled) {
      console.log('  WARNING: Could not find username input!');
    }
    
    await page.waitForTimeout(300);
    
    // 5. 填写密码
    console.log('5. Filling password...');
    
    const passwordSelectors = [
      'input[type="password"]',
      'input[placeholder*="密码"]',
      'input[name="password"]',
      'input[name="pwd"]'
    ];
    
    let passwordFilled = false;
    for (const selector of passwordSelectors) {
      try {
        const input = await page.$(selector);
        if (input && await input.isVisible()) {
          await input.click();
          await input.fill('');
          await input.type(this.password, { delay: 50 });
          console.log('  Filled password with:', selector);
          passwordFilled = true;
          break;
        }
      } catch (e) {}
    }
    
    if (!passwordFilled) {
      console.log('  WARNING: Could not find password input!');
    }
    
    await this.takeScreenshot(page, '04-filled-form');
    
    // 6. 点击登录按钮
    console.log('6. Clicking submit button...');
    
    await page.waitForTimeout(500);
    
    const submitSelectors = [
      'button[type="submit"]',
      'button:has-text("登 录")',
      'button:has-text("登录")',
      '[class*="submit"]:has-text("登")',
      'input[type="submit"]'
    ];
    
    for (const selector of submitSelectors) {
      try {
        const btn = await page.$(selector);
        if (btn && await btn.isVisible()) {
          await btn.click();
          console.log('  Clicked submit:', selector);
          break;
        }
      } catch (e) {}
    }
    
    // 7. 等待登录结果
    console.log('7. Waiting for login result...');
    
    await page.waitForTimeout(2000);
    await this.takeScreenshot(page, '05-after-submit');
    
    // 检查是否有验证码
    const captcha = await page.$('[class*="captcha"], [class*="verify"], img[src*="captcha"]');
    if (captcha) {
      console.log('\n  !!! CAPTCHA DETECTED !!!');
      console.log('  Waiting 30 seconds for manual captcha solving...');
      await page.waitForTimeout(30000);
      await this.takeScreenshot(page, '06-after-captcha');
    }
    
    // 检查错误信息
    const errorElement = await page.$('[class*="error"], [class*="message"]');
    if (errorElement) {
      const errorText = await errorElement.textContent().catch(() => null);
      if (errorText && errorText.includes('错误')) {
        console.log('  Login error:', errorText);
      }
    }
    
    // 8. 检查登录状态
    await page.waitForTimeout(2000);
    const isLoggedIn = await this.checkLoginStatus(page);
    
    if (isLoggedIn) {
      console.log('\n  ✓ LOGIN SUCCESSFUL!');
      await this.takeScreenshot(page, '07-login-success');
      return true;
    } else {
      console.log('\n  ✗ Login may have failed');
      await this.takeScreenshot(page, '08-login-failed');
      return false;
    }
  }

  async run() {
    console.log('\n' + '='.repeat(60));
    console.log('RiceQuant Auto Login');
    console.log('='.repeat(60));
    
    const browser = await chromium.launch({
      headless: false,
      slowMo: 100,
      args: ['--start-maximized']
    });
    
    let context;
    
    // 尝试使用保存的状态
    if (fs.existsSync(AUTH_STATE_FILE)) {
      console.log('\nTrying saved auth state...');
      try {
        context = await browser.newContext({
          storageState: AUTH_STATE_FILE,
          viewport: { width: 1400, height: 900 }
        });
        
        const page = await context.newPage();
        await page.goto('https://www.ricequant.com/workspace', { waitUntil: 'networkidle', timeout: 15000 });
        
        const isLoggedIn = await this.checkLoginStatus(page);
        
        if (isLoggedIn) {
          console.log('✓ Saved auth state is valid!\n');
          await browser.close();
          return true;
        } else {
          console.log('✗ Saved auth state expired');
        }
      } catch (e) {
        console.log('Error using saved state:', e.message);
      }
    }
    
    // 需要重新登录
    console.log('\nPerforming fresh login...\n');
    
    context = await browser.newContext({
      viewport: { width: 1400, height: 900 }
    });
    
    const page = await context.newPage();
    
    try {
      const success = await this.doLogin(page);
      
      if (success) {
        // 导航到 workspace 确认登录
        await page.goto('https://www.ricequant.com/workspace', { waitUntil: 'networkidle' });
        await page.waitForTimeout(2000);
        
        await this.saveAuthState(context, { source: 'auto-login' });
        await browser.close();
        return true;
      } else {
        // 等待用户手动完成登录
        console.log('\n' + '='.repeat(60));
        console.log('Auto login may have failed.');
        console.log('Please complete login manually in the browser.');
        console.log('Waiting 60 seconds...');
        console.log('='.repeat(60));
        
        await page.waitForTimeout(60000);
        
        const isLoggedIn = await this.checkLoginStatus(page);
        if (isLoggedIn) {
          await this.saveAuthState(context, { source: 'manual' });
          await browser.close();
          return true;
        }
        
        await browser.close();
        return false;
      }
    } catch (e) {
      console.error('Error:', e.message);
      await browser.close();
      return false;
    }
  }
}

// 运行
const auth = new RiceQuantAuth();
auth.run().then(success => {
  console.log('\n' + '='.repeat(60));
  if (success) {
    console.log('✓ Authentication successful!');
    console.log('\nNext steps:');
    console.log('  node list-strategies.js');
    console.log('  node run-skill.js --id <strategyId> --file <path>');
  } else {
    console.log('✗ Authentication failed!');
    console.log('\nPlease check:');
    console.log('  1. Username and password in .env file');
    console.log('  2. Manual login in browser');
  }
  console.log('='.repeat(60));
  process.exit(success ? 0 : 1);
}).catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});