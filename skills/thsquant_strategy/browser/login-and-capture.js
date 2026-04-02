import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function loginAndCaptureAPIs(options = {}) {
  const { headed = true } = options;
  
  console.log('Launching browser for THSQuant login...');
  
  const browser = await chromium.launch({
    headless: !headed,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  const page = await context.newPage();
  
  const apiCalls = [];
  
  page.on('request', request => {
    const url = request.url();
    if (url.includes('quant.10jqka.com.cn') && 
        (url.includes('/platform/') || url.includes('.do') || url.includes('.json'))) {
      apiCalls.push({
        url,
        method: request.method(),
        postData: request.postData(),
        timestamp: Date.now()
      });
    }
  });
  
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('quant.10jqka.com.cn') && 
        (url.includes('/platform/') || url.includes('.do') || url.includes('.json'))) {
      try {
        const body = await response.text();
        const apiCall = apiCalls.find(c => c.url === url);
        if (apiCall) {
          apiCall.status = response.status();
          apiCall.response = body.substring(0, 500);
        }
      } catch (e) {}
    }
  });
  
  try {
    console.log('Navigating to THSQuant...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    
    await page.waitForTimeout(3000);
    
    // Check login status
    const loginButton = await page.$('#header_signup, .header-usr-left, a[href*="login"]');
    
    if (loginButton) {
      console.log('Found login button, clicking...');
      await loginButton.click();
      await page.waitForTimeout(2000);
      
      // Wait for login iframe
      console.log('Waiting for login iframe...');
      await page.waitForSelector('iframe', { timeout: 10000 }).catch(() => {
        console.log('No iframe found, trying direct login...');
      });
      
      // Try to interact with login form
      const frames = page.frames();
      for (const frame of frames) {
        const usernameInput = await frame.$('input[type="text"], input[name="username"], input[name="phone"], input[placeholder*="账号"], input[placeholder*="手机"]');
        const passwordInput = await frame.$('input[type="password"]');
        
        if (usernameInput && passwordInput) {
          console.log('Found login form in frame:', frame.name());
          
          const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
          const password = process.env.THSQUANT_PASSWORD || 'f09173228552';
          
          console.log('Filling credentials...');
          await usernameInput.fill(username);
          await page.waitForTimeout(500);
          await passwordInput.fill(password);
          await page.waitForTimeout(500);
          
          // Click login button
          const submitBtn = await frame.$('button[type="submit"], .btn-login, .login-btn, input[type="submit"]');
          if (submitBtn) {
            console.log('Clicking login button...');
            await submitBtn.click();
          } else {
            console.log('Pressing Enter...');
            await passwordInput.press('Enter');
          }
          
          await page.waitForTimeout(5000);
          break;
        }
      }
      
      // Wait for login to complete
      await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
      await page.waitForTimeout(5000);
    }
    
    // Check if logged in
    const userElement = await page.$('#header-usr-logined, .header-usr-new');
    if (userElement) {
      console.log('✓ Successfully logged in!');
    } else {
      console.log('⚠ Login status unclear, continuing...');
    }
    
    // Navigate to strategy page to capture APIs
    console.log('Navigating to strategy list...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    await page.waitForTimeout(5000);
    
    // Try to interact with strategy interface
    console.log('Looking for strategy elements...');
    
    // Click on strategy list or similar
    try {
      await page.click('#study_mystrategy').catch(() => {});
      await page.waitForTimeout(3000);
      
      // Look for strategy list items
      const strategyItems = await page.$$('.strategy-item, .item-list li');
      if (strategyItems.length > 0) {
        console.log(`Found ${strategyItems.length} strategies`);
        // Click first strategy to trigger API
        await strategyItems[0].click().catch(() => {});
        await page.waitForTimeout(3000);
      }
    } catch (e) {
      console.log('Strategy interaction failed:', e.message);
    }
    
    // Save cookies
    const cookies = await context.cookies();
    const sessionData = {
      cookies,
      timestamp: Date.now(),
      url: page.url()
    };
    
    fs.mkdirSync(path.dirname(SESSION_FILE), { recursive: true });
    fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
    console.log(`Session saved to ${SESSION_FILE}`);
    
    // Save API calls
    const apiPath = path.join(OUTPUT_ROOT, 'logged-in-api-capture.json');
    fs.writeFileSync(apiPath, JSON.stringify(apiCalls, null, 2));
    console.log(`API calls saved to ${apiPath}`);
    
    console.log(`\nCaptured ${apiCalls.length} API calls`);
    
    // Print unique endpoints
    const uniqueUrls = [...new Set(apiCalls.map(c => c.url.split('?')[0]))];
    console.log('\nUnique API endpoints:');
    uniqueUrls.forEach(url => {
      console.log('  ', url);
    });
    
    // Print successful calls with responses
    console.log('\nSuccessful API calls:');
    apiCalls.filter(c => c.status === 200 && c.response).forEach(call => {
      console.log(`\n${call.method} ${call.url}`);
      if (call.postData) {
        console.log('  Post:', call.postData.substring(0, 100));
      }
      console.log('  Response:', call.response.substring(0, 200));
    });
    
    await browser.close();
    return { sessionData, apiCalls };
    
  } catch (error) {
    console.error('Error:', error.message);
    await browser.close();
    throw error;
  }
}

loginAndCaptureAPIs({ headed: true }).catch(console.error);