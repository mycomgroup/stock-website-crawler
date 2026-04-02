import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureAPIs(options = {}) {
  const { headed = false } = options;
  
  console.log('Launching browser to capture THSQuant APIs...');
  
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
  
  // Intercept all network requests
  page.on('request', request => {
    const url = request.url();
    if (url.includes('/api/') || url.includes('/v1/') || url.includes('.do')) {
      apiCalls.push({
        url,
        method: request.method(),
        postData: request.postData()
      });
    }
  });
  
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/api/') || url.includes('/v1/') || url.includes('.do')) {
      try {
        const body = await response.text();
        const apiCall = apiCalls.find(c => c.url === url);
        if (apiCall) {
          apiCall.status = response.status();
          apiCall.response = body.substring(0, 500);
        }
      } catch (e) {
        // Ignore
      }
    }
  });
  
  try {
    console.log('Navigating to THSQuant...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    
    await page.waitForTimeout(5000);
    
    // Try to interact with the page to trigger more API calls
    console.log('Interacting with page...');
    
    // Try to click on strategy research
    try {
      await page.click('#study_mystrategy').catch(() => {});
      await page.waitForTimeout(3000);
    } catch (e) {}
    
    // Try to navigate to different sections
    try {
      await page.goto('https://quant.10jqka.com.cn/view/study-research.html').catch(() => {});
      await page.waitForTimeout(3000);
    } catch (e) {}
    
    console.log(`Captured ${apiCalls.length} API calls`);
    
    // Save results
    const outputPath = path.join(OUTPUT_ROOT, 'api-capture.json');
    fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(apiCalls, null, 2));
    console.log('Saved to:', outputPath);
    
    // Print API calls
    apiCalls.forEach(call => {
      console.log(`\n${call.method} ${call.url}`);
      if (call.postData) {
        console.log('  Post:', call.postData.substring(0, 100));
      }
      if (call.response) {
        console.log('  Response:', call.response.substring(0, 100));
      }
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

captureAPIs({ headed }).catch(console.error);