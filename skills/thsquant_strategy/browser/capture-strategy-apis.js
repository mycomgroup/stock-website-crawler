import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureStrategyAPIs(options = {}) {
  const { headed = false } = options;
  
  // Load session
  const sessionData = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = sessionData.cookies;
  
  console.log('Loading session with', cookies.length, 'cookies');
  
  const browser = await chromium.launch({
    headless: !headed,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  // Add session cookies
  await context.addCookies(cookies);
  
  const page = await context.newPage();
  
  const apiCalls = [];
  
  // Intercept all network requests
  page.on('request', request => {
    const url = request.url();
    if (url.includes('/api/') || url.includes('quant.') || url.includes('.json') || url.includes('strategy')) {
      apiCalls.push({
        url,
        method: request.method(),
        postData: request.postData()
      });
    }
  });
  
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/api/') || url.includes('quant.') || url.includes('.json') || url.includes('strategy')) {
      try {
        const body = await response.text();
        const apiCall = apiCalls.find(c => c.url === url);
        if (apiCall) {
          apiCall.status = response.status();
          apiCall.response = body.substring(0, 1000);
        }
      } catch (e) {
        // Ignore
      }
    }
  });
  
  try {
    console.log('Navigating to strategy page...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    
    await page.waitForTimeout(5000);
    
    // Try different URLs to capture APIs
    const urls = [
      'https://quant.10jqka.com.cn/view/study-index.html',
      'https://quant.10jqka.com.cn/view/study-research.html',
      'https://quant.10jqka.com.cn/view/trade.html'
    ];
    
    for (const url of urls) {
      try {
        console.log('Trying URL:', url);
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(3000);
      } catch (e) {
        console.log('  Failed:', e.message);
      }
    }
    
    console.log(`Captured ${apiCalls.length} API calls`);
    
    // Save results
    const outputPath = path.join(OUTPUT_ROOT, 'strategy-api-capture.json');
    fs.writeFileSync(outputPath, JSON.stringify(apiCalls, null, 2));
    console.log('Saved to:', outputPath);
    
    // Print unique API patterns
    const uniqueUrls = [...new Set(apiCalls.map(c => c.url.split('?')[0]))];
    console.log('\nUnique API endpoints:');
    uniqueUrls.forEach(url => {
      console.log('  ', url);
    });
    
    await browser.close();
    return apiCalls;
    
  } catch (error) {
    console.error('Error:', error.message);
    await browser.close();
    throw error;
  }
}

const args = process.argv.slice(2);
const headed = args.includes('--headed');

captureStrategyAPIs({ headed }).catch(console.error);