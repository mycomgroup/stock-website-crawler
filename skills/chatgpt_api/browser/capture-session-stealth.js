import { chromium } from 'playwright';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { PATHS } from '../paths.js';
import { ENV } from '../load-env.js';
import {
  resolveChromeProfile,
  formatResolvedChromeProfile,
  enhanceChromeProfileError
} from './chrome-profile.js';

/**
 * 使用 Playwright 打开浏览器，添加反检测措施
 * 登录成功后保存 cookies 到 session.json
 */
export async function captureSessionStealth(options = {}) {
  const {
    headless = ENV.HEADLESS,
    useProfile = ENV.CHROME_PROFILE_PATH,
    timeout = 600000 // 10 minutes for user to login
  } = options;

  console.log('🚀 启动浏览器进行登录（反检测模式）...');
  
  // Ensure data directory exists
  if (!existsSync(PATHS.data)) {
    mkdirSync(PATHS.data, { recursive: true });
  }

  let browser, context, page;

  try {
    // Launch with stealth settings
    const launchOptions = {
      headless: false,
      timeout,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials',
        '--disable-web-security',
        '--disable-features=BlockInsecurePrivateNetworkRequests'
      ]
    };

    if (useProfile) {
      const profileConfig = resolveChromeProfile(useProfile);
      console.log(`📂 使用 Chrome profile: ${formatResolvedChromeProfile(profileConfig)}`);

      try {
        context = await chromium.launchPersistentContext(profileConfig.userDataDir, {
          ...launchOptions,
          channel: 'chrome',
          args: [...launchOptions.args, ...profileConfig.launchArgs],
          viewport: { width: 1280, height: 800 },
          locale: 'zh-CN',
          timezoneId: 'Asia/Shanghai',
          permissions: ['geolocation', 'notifications'],
          colorScheme: 'light'
        });
      } catch (error) {
        throw enhanceChromeProfileError(error, profileConfig);
      }
      
      page = context.pages()[0] || await context.newPage();
      
    } else {
      browser = await chromium.launch(launchOptions);
      
      context = await browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        locale: 'zh-CN',
        timezoneId: 'Asia/Shanghai',
        permissions: ['geolocation', 'notifications'],
        colorScheme: 'light',
        deviceScaleFactor: 2,
        hasTouch: false,
        isMobile: false,
        javaScriptEnabled: true
      });

      page = await context.newPage();
    }

    // Add stealth scripts
    await page.addInitScript(() => {
      // Override navigator.webdriver
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });

      // Override chrome property
      window.chrome = {
        runtime: {}
      };

      // Override permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );

      // Override plugins
      Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
      });

      // Override languages
      Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh', 'en-US', 'en']
      });
    });

    console.log('🌐 打开 ChatGPT 登录页面...');
    await page.goto('https://chatgpt.com/', {
      waitUntil: 'networkidle',
      timeout
    });

    console.log('');
    console.log('🔐 请在浏览器中完成登录...');
    console.log('   - 可以使用 Google、Microsoft、Apple 或邮箱登录');
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
             name.includes('token') ||
             name.includes('secure');
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
    if (browser) {
      await browser.close();
    } else if (context) {
      await context.close();
    }
  }
}
