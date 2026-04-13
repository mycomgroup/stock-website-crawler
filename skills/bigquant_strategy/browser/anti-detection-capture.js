/**
 * BigQuant 防封版Session捕获
 * 使用反检测措施避免被封禁
 */

import { AntiDetection, SessionManager } from '../lib/anti-detection.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SESSION_FILE = path.join(__dirname, '../data/session.json');
const BIGQUANT_URL = 'https://bigquant.com';

/**
 * 使用反检测措施捕获BigQuant session
 */
async function captureSessionWithAntiDetection() {
  console.log('🛡️ Starting anti-detection session capture for BigQuant...');
  
  const sessionManager = new SessionManager(SESSION_FILE, {
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7天
    validateUrl: 'https://bigquant.com/api/user/info'
  });
  
  // 检查现有session
  if (await sessionManager.isValid()) {
    console.log('✅ Existing session is valid');
    return await sessionManager.load();
  }
  
  console.log('⚠️ No valid session found, starting browser capture...');
  
  // 创建反检测浏览器
  const browser = await AntiDetection.setupBrowser({
    headless: false // 显示浏览器用于手动登录
  });
  
  try {
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      locale: 'zh-CN',
      timezoneId: 'Asia/Shanghai'
    });
    
    const page = await context.newPage();
    
    // 注入反检测脚本
    console.log('🎭 Injecting anti-detection scripts...');
    await AntiDetection.injectAntiDetection(page);
    
    // 设置真实headers
    await AntiDetection.setRealisticHeaders(page, {
      'Referer': BIGQUANT_URL,
      'Origin': BIGQUANT_URL
    });
    
    // 访问登录页
    console.log('🌐 Navigating to BigQuant...');
    await page.goto(BIGQUANT_URL, {
      waitUntil: 'networkidle'
    });
    
    // 模拟人类行为
    await AntiDetection.simulateHumanBehavior(page);
    await AntiDetection.randomDelay(2000, 4000);
    
    // 等待用户手动登录
    console.log('\n📝 Please login manually in the browser...');
    console.log('⏳ Waiting for login completion (timeout: 5 minutes)...\n');
    
    // 等待登录成功的标志
    await page.waitForFunction(
      () => {
        // 检查是否有用户信息或登录成功的标志
        return document.cookie.includes('sessionid') || 
               document.cookie.includes('token') ||
               window.location.pathname !== '/login';
      },
      { timeout: 300000 } // 5分钟超时
    );
    
    console.log('✅ Login detected!');
    
    // 再次模拟人类行为
    await AntiDetection.simulateHumanBehavior(page);
    await AntiDetection.randomDelay(1000, 2000);
    
    // 捕获session数据
    console.log('📦 Capturing session data...');
    const cookies = await context.cookies();
    const localStorage = await page.evaluate(() => {
      const items = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        items[key] = localStorage.getItem(key);
      }
      return items;
    });
    
    const session = {
      cookies,
      localStorage,
      userAgent: await page.evaluate(() => navigator.userAgent),
      capturedAt: new Date().toISOString()
    };
    
    // 保存session
    await sessionManager.save(session);
    console.log(`✅ Session saved to: ${SESSION_FILE}`);
    
    // 验证session
    console.log('🔍 Validating session...');
    const isValid = await sessionManager.isValid();
    console.log(isValid ? '✅ Session is valid' : '❌ Session validation failed');
    
    return session;
    
  } finally {
    await browser.close();
  }
}

/**
 * 使用现有session创建页面
 */
async function createPageWithSession(browser) {
  const sessionManager = new SessionManager(SESSION_FILE);
  const session = await sessionManager.load();
  
  if (!session) {
    throw new Error('No session found. Please run captureSessionWithAntiDetection first.');
  }
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    userAgent: session.userAgent
  });
  
  // 添加cookies
  await context.addCookies(session.cookies);
  
  const page = await context.newPage();
  
  // 恢复localStorage
  if (session.localStorage) {
    await page.addInitScript((storage) => {
      for (const [key, value] of Object.entries(storage)) {
        localStorage.setItem(key, value);
      }
    }, session.localStorage);
  }
  
  // 注入反检测
  await AntiDetection.injectAntiDetection(page);
  
  return { page, context };
}

/**
 * 主函数
 */
async function main() {
  try {
    const session = await captureSessionWithAntiDetection();
    
    console.log('\n📊 Session Summary:');
    console.log(`- Cookies: ${session.cookies.length}`);
    console.log(`- LocalStorage items: ${Object.keys(session.localStorage || {}).length}`);
    console.log(`- User-Agent: ${session.userAgent}`);
    console.log(`- Captured at: ${session.capturedAt}`);
    
    console.log('\n✅ Session capture completed successfully!');
    console.log('\n💡 You can now use this session in your scripts with:');
    console.log('   import { createPageWithSession } from "./anti-detection-capture.js"');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export {
  captureSessionWithAntiDetection,
  createPageWithSession,
  SESSION_FILE
};
