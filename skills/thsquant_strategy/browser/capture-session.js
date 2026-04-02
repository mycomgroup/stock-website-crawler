import { chromium } from 'playwright';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';
import fs from 'node:fs';
import path from 'node:path';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

export async function captureTHSQuantSession(credentials, options = {}) {
  const { headed = false } = options;
  
  console.log('Launching browser...');
  const browser = await chromium.launch({ 
    headless: !headed,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  
  const page = await context.newPage();
  
  try {
    console.log('Navigating to THSQuant login page...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    await page.waitForTimeout(2000);
    
    // Check if already logged in
    const currentUrl = page.url();
    if (!currentUrl.includes('login') && !currentUrl.includes('signin')) {
      const cookies = await context.cookies();
      const sessionData = {
        cookies,
        timestamp: Date.now(),
        url: currentUrl
      };
      
      console.log('Already logged in, capturing session...');
      await browser.close();
      return sessionData;
    }
    
    // Need to login
    console.log('Need to login...');
    
    // Wait for login form
    await page.waitForSelector('input[type="text"], input[name="username"], input[name="phone"]', {
      timeout: 10000
    }).catch(() => null);
    
    // Fill credentials
    const usernameInput = await page.$('input[type="text"], input[name="username"], input[name="phone"]');
    const passwordInput = await page.$('input[type="password"], input[name="password"]');
    
    if (usernameInput && passwordInput) {
      console.log('Filling credentials...');
      await usernameInput.fill(credentials.username);
      await passwordInput.fill(credentials.password);
      
      // Click login button
      const loginButton = await page.$('button[type="submit"], .login-btn, .btn-login');
      if (loginButton) {
        await loginButton.click();
      } else {
        await page.keyboard.press('Enter');
      }
      
      // Wait for login to complete
      await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
      await page.waitForTimeout(3000);
    }
    
    const cookies = await context.cookies();
    const sessionData = {
      cookies,
      timestamp: Date.now(),
      url: page.url()
    };
    
    console.log('Session captured successfully');
    await browser.close();
    
    return sessionData;
    
  } catch (error) {
    console.error('Error during login:', error.message);
    await browser.close();
    throw error;
  }
}