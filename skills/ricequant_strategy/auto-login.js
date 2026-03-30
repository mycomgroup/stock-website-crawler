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
    console.log('  Screenshot:', path.basename(filepath));
  }

  async saveAuthState(context, metadata = {}) {
    const state = await context.storageState();
    const stateData = {
      ...state,
      savedAt: new Date().toISOString(),
      metadata
    };
    fs.writeFileSync(AUTH_STATE_FILE, JSON.stringify(stateData, null, 2));
    console.log('  Auth state saved:', AUTH_STATE_FILE);
    
    const sessionData = {
      cookies: state.cookies,
      timestamp: Date.now(),
      savedAt: new Date().toISOString()
    };
    fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
    console.log('  Session saved:', SESSION_FILE);
    
    // 打印 cookies
    console.log('\n  Cookies saved:');
    state.cookies.forEach(c => console.log(`    ${c.name}: ${c.value.substring(0, 50)}...`));
  }

  async doLogin(page) {
    console.log('\n=== Starting Login Process ===\n');
    
    // 1. 访问首页
    console.log('1. Navigating to RiceQuant...');
    await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle', timeout: 30000 });
    await this.takeScreenshot(page, '01-homepage');
    
    // 2. 点击登录按钮
    console.log('2. Clicking login button...');
    await page.click('button:has-text("登录")');
    await page.waitForTimeout(1000);
    await this.takeScreenshot(page, '02-login-modal');
    
    // 3. 点击密码登录 tab
    console.log('3. Clicking "密码登录" tab...');
    await page.click('text=密码登录');
    await page.waitForTimeout(800);
    await this.takeScreenshot(page, '03-password-tab');
    
    // 4. 填写用户名
    console.log('4. Filling username...');
    const usernameInput = await page.$('input[placeholder="国内手机号或邮箱"]');
    if (usernameInput) {
      await usernameInput.click();
      await page.waitForTimeout(100);
      await usernameInput.fill('');
      await page.waitForTimeout(100);
      // 逐字输入
      for (const char of this.username) {
        await usernameInput.press(char);
        await page.waitForTimeout(50);
      }
      console.log('  Filled username:', this.username);
    }
    await page.waitForTimeout(500);
    
    // 5. 填写密码
    console.log('5. Filling password...');
    const passwordInput = await page.$('input[type="password"]');
    if (passwordInput) {
      await passwordInput.click();
      await page.waitForTimeout(100);
      await passwordInput.fill('');
      await page.waitForTimeout(100);
      // 逐字输入
      for (const char of this.password) {
        await passwordInput.press(char);
        await page.waitForTimeout(50);
      }
      console.log('  Filled password');
    }
    await page.waitForTimeout(500);
    
    await this.takeScreenshot(page, '04-filled-form');
    
    // 6. 点击登录按钮
    console.log('6. Clicking submit button...');
    await page.click('button.btn--submit:has-text("登录")');
    console.log('  Clicked submit');
    
    // 7. 等待登录结果 - 增加等待时间
    console.log('7. Waiting for login result...');
    
    // 等待可能的跳转
    await page.waitForTimeout(3000);
    await this.takeScreenshot(page, '05-after-submit-3s');
    
    // 检查当前 URL
    let url = page.url();
    console.log('  URL after 3s:', url);
    
    // 等待更长时间
    await page.waitForTimeout(2000);
    url = page.url();
    console.log('  URL after 5s:', url);
    await this.takeScreenshot(page, '05-after-submit-5s');
    
    // 检查错误信息
    const errorSelectors = [
      '[class*="error"]',
      '[class*="message"]',
      '.el-message',
      '.el-notification'
    ];
    
    for (const selector of errorSelectors) {
      const errorEl = await page.$(selector);
      if (errorEl) {
        const isVisible = await errorEl.isVisible();
        if (isVisible) {
          const text = await errorEl.textContent();
          if (text && text.trim()) {
            console.log('  Error/Message found:', text.trim());
          }
        }
      }
    }
    
    // 检查是否成功登录到策略页面
    if (url.includes('/quant/strategys') || url.includes('/workspace')) {
      console.log('\n  ✓ LOGIN SUCCESSFUL! (redirected to strategy page)');
      await this.takeScreenshot(page, '06-login-success');
      return true;
    }
    
    // 尝试手动访问 workspace
    console.log('\n  Trying to access workspace directly...');
    try {
      await page.goto('https://www.ricequant.com/workspace', { 
        waitUntil: 'networkidle', 
        timeout: 15000 
      });
      await page.waitForTimeout(2000);
      
      url = page.url();
      console.log('  Workspace URL:', url);
      await this.takeScreenshot(page, '07-workspace');
      
      if (!url.includes('/welcome') && !url.includes('/login')) {
        console.log('\n  ✓ LOGIN SUCCESSFUL! (can access workspace)');
        return true;
      }
    } catch (e) {
      console.log('  Workspace access error:', e.message);
    }
    
    // 最后检查 cookies
    console.log('\n  Checking cookies...');
    const cookies = await page.context().cookies();
    const rqjwt = cookies.find(c => c.name === 'rqjwt');
    const sid = cookies.find(c => c.name === 'sid');
    
    console.log('  rqjwt:', rqjwt ? 'present' : 'missing');
    console.log('  sid:', sid ? 'present' : 'missing');
    
    if (rqjwt) {
      console.log('\n  ✓ LOGIN SUCCESSFUL! (rqjwt cookie present)');
      await this.takeScreenshot(page, '08-success-with-cookie');
      return true;
    }
    
    console.log('\n  ✗ Login appears to have failed');
    await this.takeScreenshot(page, '09-failed');
    return false;
  }

  async run() {
    console.log('\n' + '='.repeat(60));
    console.log('RiceQuant Auto Login');
    console.log('='.repeat(60));
    
    const browser = await chromium.launch({
      headless: false,
      slowMo: 30,
      args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
      viewport: { width: 1400, height: 900 }
    });
    
    const page = await context.newPage();
    
    try {
      const success = await this.doLogin(page);
      
      if (success) {
        await this.saveAuthState(context, { source: 'auto-login' });
        await browser.close();
        return true;
      } else {
        console.log('\n' + '='.repeat(60));
        console.log('Auto login failed.');
        console.log('Please check your credentials or try manual login.');
        console.log('Browser will stay open for 30 seconds...');
        console.log('='.repeat(60));
        
        await page.waitForTimeout(30000);
        
        // 再次检查
        const cookies = await context.cookies();
        const rqjwt = cookies.find(c => c.name === 'rqjwt');
        if (rqjwt) {
          console.log('\n✓ rqjwt cookie found after waiting!');
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
    console.log('\nYou can now run:');
    console.log('  node list-strategies.js');
    console.log('  node run-skill.js --id <id> --file <path>');
  } else {
    console.log('✗ Authentication failed!');
    console.log('\nPlease verify:');
    console.log('  1. Username and password in .env');
    console.log('  2. Account is not locked');
    console.log('  3. Try manual login in browser');
  }
  console.log('='.repeat(60));
  process.exit(success ? 0 : 1);
}).catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});