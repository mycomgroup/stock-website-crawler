const { chromium } = require('playwright');

const URL = 'https://www.lixinger.com/open/api/my-apis';
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';

(async () => {
  const browser = await chromium.launch({
    headless: false,
    channel: 'chrome', // 使用系统已安装的 Chrome
  });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 可能跳转到登录页，或页面上有登录入口
    const currentUrl = page.url();
    if (currentUrl.includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
      // 已在登录页或页面上有密码框
    } else {
      // 尝试点击「登录」链接
      const loginLink = page.locator('text=登录').first();
      if (await loginLink.count() > 0) {
        await loginLink.click();
        await page.waitForTimeout(2000);
      }
    }

    // 手机号/账号输入：常见 placeholder 或 name
    const phoneSelectors = [
      'input[placeholder*="手机"]',
      'input[placeholder*="账号"]',
      'input[type="tel"]',
      'input[name="phone"]',
      'input[name="username"]',
      'input[name="account"]',
    ];
    let phoneInput = null;
    for (const sel of phoneSelectors) {
      const el = page.locator(sel).first();
      if (await el.count() > 0) {
        phoneInput = el;
        break;
      }
    }
    if (!phoneInput) {
      phoneInput = page.locator('input').first();
    }
    await phoneInput.fill(ACCOUNT);

    // 密码框
    const pwdInput = page.locator('input[type="password"]').first();
    await pwdInput.fill(PASSWORD);

    // 登录按钮
    const submitSelectors = [
      'button:has-text("登录")',
      'button:has-text("登 录")',
      'a:has-text("登录")',
      '[type="submit"]',
      'button[type="button"]:has-text("登录")',
    ];
    for (const sel of submitSelectors) {
      const btn = page.locator(sel).first();
      if (await btn.count() > 0) {
        await btn.click();
        break;
      }
    }

    await page.waitForTimeout(5000);
    console.log('当前 URL:', page.url());
    await page.screenshot({ path: 'after-login.png' });
    console.log('已截图 after-login.png');
  } catch (e) {
    console.error(e);
    await page.screenshot({ path: 'error.png' });
    console.log('已保存错误截图 error.png');
  }

  await browser.close();
})();
