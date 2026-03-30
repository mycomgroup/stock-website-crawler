import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = path.join(__dirname, '..', 'data', 'session.json');
const TRACES_FILE = path.join(__dirname, '..', 'data', 'api_traces.json');

async function captureRiceQuantAPI() {
  console.log('=== RiceQuant API Capture ===\n');
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 200
  });
  
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  
  // 收集所有请求
  const requests = [];
  const apiCalls = [];
  
  page.on('request', request => {
    const url = request.url();
    requests.push({
      url,
      method: request.method(),
      resourceType: request.resourceType()
    });
    
    // 只记录 XHR/Fetch 请求
    if (request.resourceType() === 'xhr' || request.resourceType() === 'fetch') {
      const headers = request.headers();
      apiCalls.push({
        url,
        method: request.method(),
        headers,
        postData: request.postData()
      });
    }
  });
  
  page.on('response', async response => {
    const url = response.url();
    const request = apiCalls.find(c => c.url === url);
    
    if (request) {
      request.status = response.status();
      request.responseHeaders = response.headers();
      
      try {
        const body = await response.text();
        request.responseBody = body.substring(0, 500);
      } catch (e) {
        request.responseBody = '[unable to read]';
      }
    }
  });
  
  try {
    // 1. 访问首页
    console.log('1. Navigating to RiceQuant...');
    await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    // 2. 尝试点击登录
    console.log('2. Looking for login...');
    try {
      const loginBtn = await page.locator('button:has-text("登录"), a:has-text("登录")').first();
      if (await loginBtn.isVisible({ timeout: 3000 })) {
        await loginBtn.click();
        await page.waitForTimeout(2000);
        console.log('   Clicked login button');
      }
    } catch (e) {
      console.log('   No login button found (might be logged in)');
    }
    
    // 3. 检查当前状态
    const currentUrl = page.url();
    console.log(`3. Current URL: ${currentUrl}`);
    
    // 4. 访问 workspace
    console.log('4. Navigating to workspace...');
    await page.goto('https://www.ricequant.com/workspace', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    // 5. 检查是否成功进入 workspace
    const workspaceUrl = page.url();
    console.log(`   Workspace URL: ${workspaceUrl}`);
    
    // 6. 获取 cookies
    const cookies = await context.cookies();
    console.log('\n5. Cookies:');
    cookies.forEach(c => console.log(`   ${c.name}: ${c.value.substring(0, 40)}...`));
    
    // 7. 保存 session
    const sessionData = {
      cookies,
      timestamp: Date.now()
    };
    
    const dataDir = path.dirname(SESSION_FILE);
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
    
    fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
    console.log(`\n   Session saved to: ${SESSION_FILE}`);
    
    // 8. 如果在 workspace，尝试更多操作
    if (workspaceUrl.includes('workspace')) {
      console.log('\n6. Exploring workspace...');
      
      // 等待页面加载
      await page.waitForTimeout(2000);
      
      // 尝试点击策略列表
      try {
        const strategyLink = await page.locator('text=策略, a[href*="strategy"]').first();
        if (await strategyLink.isVisible({ timeout: 3000 })) {
          await strategyLink.click();
          await page.waitForTimeout(2000);
          console.log('   Clicked strategy link');
        }
      } catch (e) {
        console.log('   Could not find strategy link');
      }
    }
    
    // 9. 保存 API traces
    fs.writeFileSync(TRACES_FILE, JSON.stringify(apiCalls, null, 2));
    console.log(`\n7. API traces saved: ${TRACES_FILE}`);
    console.log(`   Total requests: ${requests.length}`);
    console.log(`   API calls: ${apiCalls.length}`);
    
    // 10. 打印关键 API
    console.log('\n=== API Calls ===');
    apiCalls.slice(0, 10).forEach(call => {
      console.log(`${call.method} ${call.url}`);
      if (call.status) console.log(`   Status: ${call.status}`);
      if (call.responseBody) {
        try {
          const json = JSON.parse(call.responseBody);
          console.log(`   Response: ${JSON.stringify(json).substring(0, 100)}`);
        } catch {
          console.log(`   Response: ${call.responseBody.substring(0, 100)}`);
        }
      }
    });
    
    // 保持浏览器打开
    console.log('\n=== Browser will stay open for 30 seconds ===');
    console.log('You can manually navigate to see more API calls...');
    await page.waitForTimeout(30000);
    
  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
    console.log('\nDone!');
  }
}

captureRiceQuantAPI();