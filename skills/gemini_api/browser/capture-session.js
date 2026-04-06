import { chromium } from 'playwright';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { PATHS } from '../paths.js';
import { ENV } from '../load-env.js';

/**
 * 使用 Playwright 打开浏览器，让用户完成 Google OAuth 登录
 * 登录成功后保存 cookies 到 session.json
 */
export async function captureSession(options = {}) {
  const {
    headless = ENV.HEADLESS,
    useProfile = ENV.CHROME_PROFILE_PATH,
    timeout = 600000 // 10 minutes for user to login
  } = options;

  console.log('🚀 启动浏览器进行登录...');
  
  // Ensure data directory exists
  if (!existsSync(PATHS.data)) {
    mkdirSync(PATHS.data, { recursive: true });
  }

  const launchOptions = {
    headless: false, // Always show browser for login
    timeout
  };

  // Don't use existing profile for fresh login
  // if (useProfile) {
  //   console.log(`📂 使用现有 Chrome profile: ${useProfile}`);
  //   launchOptions.channel = 'chrome';
  //   launchOptions.args = [`--user-data-dir=${useProfile}`];
  // }

  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();

  try {
    console.log('🌐 打开 Google Gemini 登录页面...');
    await page.goto('https://gemini.google.com/', {
      waitUntil: 'domcontentloaded',
      timeout
    });

    console.log('');
    console.log('🔐 请在浏览器中完成登录...');
    console.log('   - 使用你的 Google 账号登录');
    console.log('   - 脚本会等待 5 分钟让你完成登录');
    console.log('');
    console.log('⏳ 等待 300 秒（5分钟）...');
    console.log('');

    // Wait 300 seconds for user to login
    await page.waitForTimeout(300000);

    console.log('✅ 等待完成，开始捕获 cookies...');
    console.log('⏳ 再等待 3 秒确保所有 cookies 都已设置...');
    await page.waitForTimeout(3000);

    // Capture cookies
    const cookies = await context.cookies();
    
    // Filter important cookies
    const importantCookies = cookies.filter(cookie => {
      const name = cookie.name.toLowerCase();
      return name.includes('auth') || 
             name.includes('session') || 
             name.includes('cf') ||
             name.includes('token');
    });

    console.log(`📦 捕获到 ${importantCookies.length} 个关键 cookies`);
    
    // Log cookie names for debugging
    importantCookies.forEach(cookie => {
      console.log(`   - ${cookie.name} (domain: ${cookie.domain})`);
    });

    // Save session data
    const sessionData = {
      capturedAt: new Date().toISOString(),
      cookies: importantCookies,
      userAgent: await page.evaluate(() => navigator.userAgent)
    };

    writeFileSync(
      PATHS.sessionFile,
      JSON.stringify(sessionData, null, 2),
      'utf-8'
    );

    console.log(`💾 Session 数据已保存到: ${PATHS.sessionFile}`);
    console.log('');
    console.log('✨ 下次使用时将自动加载 session，无需重新登录');

    return sessionData;

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    throw error;
  } finally {
    await browser.close();
  }
}

/**
 * 验证 session 是否仍然有效
 */
export async function validateSessionInBrowser(sessionData) {
  console.log('🔍 验证 session 有效性...');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: sessionData.userAgent || 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  // Restore cookies
  await context.addCookies(sessionData.cookies);

  const page = await context.newPage();

  try {
    await page.goto('https://gemini.google.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 15000
    });

    await page.waitForTimeout(2000);

    // Check if redirected to login page
    const currentUrl = page.url();
    const isValid = currentUrl.includes('gemini.google.com') && !currentUrl.includes('/signin');

    if (isValid) {
      console.log('✅ Session 有效');
    } else {
      console.log('❌ Session 已失效，需要重新登录');
    }

    await browser.close();
    return isValid;

  } catch (error) {
    console.error('❌ 验证失败:', error.message);
    await browser.close();
    return false;
  }
}
