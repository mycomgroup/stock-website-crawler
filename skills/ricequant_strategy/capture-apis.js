import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_STATE_FILE = path.join(__dirname, 'data', 'auth-state.json');

async function captureAPIs() {
  console.log('Launching browser to capture API calls...\n');
  
  const state = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf8'));
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: state,
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  
  const apiCalls = [];
  
  page.on('request', request => {
    if (request.resourceType() === 'xhr' || request.resourceType() === 'fetch') {
      apiCalls.push({
        url: request.url(),
        method: request.method(),
        postData: request.postData()
      });
    }
  });
  
  page.on('response', async response => {
    const call = apiCalls.find(c => c.url === response.url());
    if (call) {
      call.status = response.status();
      try {
        const text = await response.text();
        call.response = text.substring(0, 500);
      } catch (e) {}
    }
  });
  
  // 导航到策略页面
  console.log('Navigating to strategy page...');
  await page.goto('https://www.ricequant.com/quant/strategys', { waitUntil: 'networkidle' });
  
  await page.waitForTimeout(3000);
  
  console.log('\n=== API Calls ===\n');
  apiCalls.forEach((call, i) => {
    console.log(`${i + 1}. ${call.method} ${call.url}`);
    console.log(`   Status: ${call.status}`);
    if (call.response) {
      try {
        const json = JSON.parse(call.response);
        console.log(`   Response: ${JSON.stringify(json).substring(0, 200)}`);
      } catch {
        console.log(`   Response: ${call.response.substring(0, 200)}`);
      }
    }
    console.log('');
  });
  
  // 保存结果
  fs.writeFileSync(
    path.join(__dirname, 'data', 'captured-apis.json'), 
    JSON.stringify(apiCalls, null, 2)
  );
  
  console.log('API calls saved to data/captured-apis.json');
  
  // 保持浏览器打开
  console.log('\nWaiting 10 seconds...');
  await page.waitForTimeout(10000);
  
  await browser.close();
}

captureAPIs();