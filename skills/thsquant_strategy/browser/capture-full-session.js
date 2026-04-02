import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

async function captureFullSession() {
  console.log('Launching browser for complete login and API capture...');
  console.log('\nPlease perform the following steps manually:');
  console.log('1. Click "登录" button in the top right');
  console.log('2. Enter credentials:');
  console.log('   Username: mx_kj1ku00qp');
  console.log('   Password: f09173228552');
  console.log('3. Click login');
  console.log('4. Navigate to strategy pages (click on different menus)');
  console.log('5. Wait for browser to auto-close after 60 seconds\n');
  
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100
  });
  
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  const page = await context.newPage();
  
  const allRequests = [];
  const allResponses = [];
  
  // Capture ALL requests
  page.on('request', req => {
    const url = req.url();
    allRequests.push({
      url,
      method: req.method(),
      postData: req.postData(),
      time: Date.now()
    });
  });
  
  page.on('response', async res => {
    const url = res.url();
    try {
      const text = await res.text().catch(() => '');
      allResponses.push({
        url,
        status: res.status(),
        body: text.substring(0, 1000),
        time: Date.now()
      });
    } catch (e) {}
  });
  
  try {
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded'
    });
    
    console.log('Page loaded. Waiting 60 seconds for manual login...');
    
    // Wait 60 seconds for user to login manually
    for (let i = 60; i > 0; i--) {
      await page.waitForTimeout(1000);
      
      // Check login status
      try {
        const content = await page.content();
        if (content.includes('HI！') || content.includes('header-usr-logined')) {
          console.log(`\n✓ Login detected at ${i}s remaining!`);
          
          // Navigate to trigger more APIs
          console.log('Navigating to capture APIs...');
          
          try {
            await page.click('#study_mystrategy').catch(() => {});
            await page.waitForTimeout(2000);
            
            await page.goto('https://quant.10jqka.com.cn/view/study-research.html').catch(() => {});
            await page.waitForTimeout(3000);
            
            await page.goto('https://quant.10jqka.com.cn/view/trade.html').catch(() => {});
            await page.waitForTimeout(3000);
            
            // Go back to strategy page
            await page.goto('https://quant.10jqka.com.cn/view/study-index.html').catch(() => {});
            await page.waitForTimeout(2000);
            
          } catch (e) {}
          
          // Wait more to capture async requests
          await page.waitForTimeout(5000);
          break;
        }
      } catch (e) {}
      
      if (i % 10 === 0) {
        process.stdout.write(`\r${i} seconds remaining...`);
      }
    }
    
    console.log('\n\nSaving session...');
    
    // Save cookies
    const cookies = await context.cookies();
    fs.mkdirSync(path.dirname(SESSION_FILE), { recursive: true });
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies,
      timestamp: Date.now()
    }, null, 2));
    
    // Save all captured data
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'all-requests.json'), JSON.stringify(allRequests, null, 2));
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'all-responses.json'), JSON.stringify(allResponses, null, 2));
    
    console.log('✓ Session and API data saved');
    
    // Print strategy-related APIs
    const strategyApis = allResponses.filter(r => 
      r.url.includes('strategy') || 
      r.url.includes('backtest') ||
      r.url.includes('quant.10jqka') && r.status === 200
    );
    
    console.log(`\nFound ${strategyApis.length} potential strategy APIs:`);
    strategyApis.forEach(api => {
      console.log(`\n${api.status} ${api.url}`);
      if (api.body && api.body.length > 0) {
        console.log('Response preview:', api.body.substring(0, 200));
      }
    });
    
    await browser.close();
    
  } catch (e) {
    console.error('Error:', e.message);
    await browser.close();
  }
}

captureFullSession().catch(console.error);