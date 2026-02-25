// 测试单个API的抓取
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const TEST_URL = 'https://www.lixinger.com/open/api/doc?api-key=cn/company/measures';
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';

async function doLogin(page) {
  const loginLink = page.locator('text=登录').first();
  if (await loginLink.count() > 0) {
    await loginLink.click();
    await page.waitForTimeout(2000);
  }
  const phoneSelectors = ['input[placeholder*="手机"]', 'input[placeholder*="账号"]', 'input[type="tel"]'];
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
  const btn = page.locator('button:has-text("登录"), [type="submit"]').first();
  if (await btn.count() > 0) await btn.click();
  await page.waitForTimeout(4000);
}

(async () => {
  const browser = await chromium.launch({ headless: false, channel: 'chrome' });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(TEST_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
    await doLogin(page);
    await page.goto(TEST_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
  }

  console.log('开始提取示例...\n');

  // 方法1: 查找"获取"按钮
  const buttons = await page.locator('button, a').evaluateAll(elements => 
    elements
      .map((el, index) => ({ text: el.textContent.trim(), index }))
      .filter(item => item.text.startsWith('获取'))
  );
  
  console.log(`找到 ${buttons.length} 个"获取"按钮`);
  
  // 方法2: 直接从textarea提取
  const textareaCode = await page.evaluate(() => {
    const textarea = document.querySelector('textarea');
    if (textarea) {
      return (textarea.value || '').trim();
    }
    return '';
  });
  
  console.log(`\ntextarea内容 (${textareaCode.length}字符):`);
  console.log(textareaCode);

  await page.waitForTimeout(30000);
  await browser.close();
})();
