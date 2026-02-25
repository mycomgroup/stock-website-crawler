const { chromium } = require('playwright');

const TEST_URL = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';

async function doLogin(page) {
  const loginLink = page.locator('text=登录').first();
  if (await loginLink.count() > 0) {
    await loginLink.click();
    await page.waitForTimeout(2000);
  }
  const phoneSelectors = ['input[placeholder*="手机"]', 'input[placeholder*="账号"]', 'input[type="tel"]', 'input[name="phone"]', 'input[name="username"]'];
  let phoneInput = page.locator('input').first();
  for (const sel of phoneSelectors) {
    const el = page.locator(sel).first();
    if (await el.count() > 0) {
      phoneInput = el;
      break;
    }
  }
  await phoneInput.fill(ACCOUNT);
  const pwdInput = page.locator('input[type="password"]').first();
  await pwdInput.fill(PASSWORD);
  const btn = page.locator('button:has-text("登录"), a:has-text("登录"), [type="submit"]').first();
  if (await btn.count() > 0) await btn.click();
  await page.waitForTimeout(4000);
}

(async () => {
  const browser = await chromium.launch({ headless: false, channel: 'chrome' });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(TEST_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // 检查是否需要登录
  if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
    console.log('需要登录，开始登录...');
    await doLogin(page);
    await page.goto(TEST_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
    console.log('登录完成');
  } else {
    console.log('已登录状态');
  }

  console.log('页面已加载，开始提取示例...\n');

  const result = await page.evaluate(() => {
    const examples = [];
    
    // 查找所有"获取"按钮附近的示例代码
    const buttons = Array.from(document.querySelectorAll('button, a')).filter(el => 
      el.textContent && el.textContent.trim().startsWith('获取')
    );
    
    buttons.forEach((btn, i) => {
      const btnText = btn.textContent.trim();
      const container = btn.closest('div, section, [class*="example"], [class*="demo"]');
      if (container) {
        const codeEl = container.querySelector('textarea, pre code, code');
        if (codeEl) {
          const code = (codeEl.value || codeEl.textContent || codeEl.innerText || '').trim();
          examples.push({
            index: i,
            buttonText: btnText,
            code: code,
            codeLength: code.length
          });
        }
      }
    });
    
    return { examples, totalExamples: examples.length };
  });

  console.log('提取结果:');
  console.log(JSON.stringify(result, null, 2));
  
  await page.screenshot({ path: 'debug-page-logged-in.png', fullPage: true });
  console.log('\n已保存截图: debug-page-logged-in.png');
  
  console.log('\n等待30秒后关闭...');
  await page.waitForTimeout(30000);
  
  await browser.close();
})();
