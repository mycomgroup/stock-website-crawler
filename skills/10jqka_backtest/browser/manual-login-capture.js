import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { SESSION_FILE, DATA_DIR } from '../paths.js';

const START_URL = 'https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest';

async function main() {
  console.log('启动浏览器进行手动登录捕获...');
  
  const browser = await chromium.launch({
    headless: false, // 必须为false以便用户手动登录
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
  });
  
  // 如果有旧session，尝试加载
  try {
    if (fs.existsSync(SESSION_FILE)) {
      const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
      if (session.cookies && session.cookies.length > 0) {
        await context.addCookies(session.cookies);
        console.log(`加载了 ${session.cookies.length} 个旧cookies`);
      }
    }
  } catch (e) {
    console.log('无有效旧session，需要全新登录');
  }

  const page = await context.newPage();
  const apiCapture = [];
  
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('api') || url.includes('10jqka.com.cn/tradebacktest')) {
      const contentType = response.headers()['content-type'] || '';
      if (contentType.includes('application/json') || contentType.includes('text/html') || url.includes('.json')) {
        try {
          const req = response.request();
          const record = {
            url,
            method: req.method(),
            postData: req.postData(),
            status: response.status(),
            timestamp: Date.now()
          };
          
          if (url.includes('yieldbacktest') || url.includes('info') || url.includes('condition')) {
            const body = await response.text();
            record.responseBody = body.substring(0, 1000);
            apiCapture.push(record);
            
            // 如果成功调用了回测API且没有报错-401，说明登录成功并且获取到了正常功能
            if (response.status() === 200 && !body.includes('-401')) {
               console.log(`\n✓ 成功捕获关键API: ${url}`);
               await saveSession(context, page, apiCapture);
            }
          }
        } catch(e) {}
      }
    }
  });

  console.log(`正在打开: ${START_URL}`);
  await page.goto(START_URL, { waitUntil: 'load', timeout: 60000 });
  
  console.log('\n=========================================');
  console.log('请在打开的浏览器中:');
  console.log('1. 如果需要登录，请手动登录（可能需要解决验证码/扫码）');
  console.log('2. 登录成功后，随便输入一个回测公式并点击"运行回测"');
  console.log('3. 脚本会自动捕获您的登录状态并保存');
  console.log('=========================================\n');
  
  // 等待2分钟供用户操作
  await page.waitForTimeout(120000);
  
  // 退出前最后保存一次
  await saveSession(context, page, apiCapture);
  await browser.close();
  console.log('浏览器已关闭');
}

async function saveSession(context, page, apiCapture) {
  const cookies = await context.cookies();
  const sessionData = {
    cookies,
    timestamp: Date.now(),
    url: page.url()
  };
  
  fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
  fs.writeFileSync(
    path.join(DATA_DIR, 'api-capture.json'), 
    JSON.stringify(apiCapture, null, 2)
  );
  
  console.log(`\n✅ Session已保存至: ${SESSION_FILE}`);
  console.log(`✅ 共捕获 ${cookies.length} 个Cookie，已准备好API请求。`);
}

main().catch(console.error);
