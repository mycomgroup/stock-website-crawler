import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function manualLoginAndCapture(options = {}) {
  const { headed = true, timeout = 60000 } = options;
  
  console.log('Launching browser for THSQuant manual login...');
  console.log('Please login manually within', timeout/1000, 'seconds');
  
  const browser = await chromium.launch({
    headless: false,  // Always show browser for manual login
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
          apiCall.response = body.substring(0, 1000);
        }
      } catch (e) {}
    }
  });
  
  try {
    console.log('\n' + '='.repeat(60));
    console.log('INSTRUCTIONS:');
    console.log('1. Browser window will open');
    console.log('2. Login with credentials:');
    console.log('   Username: mx_kj1ku00qp');
    console.log('   Password: f09173228552');
    console.log('3. Navigate to strategy page');
    console.log('4. Press Ctrl+C or close browser when done');
    console.log('='.repeat(60) + '\n');
    
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    
    // Wait for manual login
    console.log('Waiting for manual login...');
    
    // Check periodically for login status
    let loggedIn = false;
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      await page.waitForTimeout(2000);
      
      // Check if logged in
      const html = await page.content();
      if (html.includes('header-usr-logined') || 
          html.includes('HI！') ||
          html.includes('用户名')) {
        loggedIn = true;
        console.log('\n✓ Detected login! Waiting for you to navigate...');
        
        // Wait more time to let user navigate and trigger APIs
        await page.waitForTimeout(30000);
        break;
      }
      
      process.stdout.write(`\rWaiting... (${Math.floor((Date.now() - startTime)/1000)}s)`);
    }
    
    console.log('\n\nCapturing session and APIs...');
    
    // Save cookies
    const cookies = await context.cookies();
    const sessionData = {
      cookies,
      timestamp: Date.now(),
      url: page.url()
    };
    
    fs.mkdirSync(path.dirname(SESSION_FILE), { recursive: true });
    fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
    console.log('✓ Session saved');
    
    // Save API calls
    const apiPath = path.join(OUTPUT_ROOT, 'manual-login-api-capture.json');
    fs.writeFileSync(apiPath, JSON.stringify(apiCalls, null, 2));
    console.log('✓ API calls saved');
    
    console.log(`\nCaptured ${apiCalls.length} API calls`);
    
    // Print unique endpoints
    const uniqueUrls = [...new Set(apiCalls.map(c => c.url.split('?')[0]))];
    console.log('\nUnique API endpoints:');
    uniqueUrls.forEach(url => {
      console.log('  ', url);
    });
    
    // Print successful calls
    console.log('\nSuccessful API calls with responses:');
    apiCalls.filter(c => c.status === 200 && c.response).forEach(call => {
      console.log(`\n${call.method} ${call.url}`);
      if (call.postData) {
        console.log('  Post:', call.postData);
      }
      console.log('  Response:', call.response);
    });
    
    await browser.close();
    return { sessionData, apiCalls };
    
  } catch (error) {
    console.error('\nError:', error.message);
    await browser.close();
    throw error;
  }
}

manualLoginAndCapture({ timeout: 90000 }).catch(e => {
  console.error('\nFailed:', e.message);
  process.exit(1);
});