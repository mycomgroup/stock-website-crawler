const { chromium } = require('playwright');

const TEST_URL = 'https://www.lixinger.com/open/api/doc?api-key=cn/company/measures';
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';

async function doLogin(page) {
  console.log('尝试登录...');
  await page.waitForTimeout(2000);
  const pwdInput = page.locator('input[type="password"]').first();
  if (await pwdInput.count() > 0) {
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
    await pwdInput.fill(PASSWORD);
    const btn = page.locator('button:has-text("登录"), button[type="submit"]').first();
    if (await btn.count() > 0) {
      await btn.click();
      await page.waitForTimeout(4000);
    }
  }
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

  console.log('页面已加载，开始分析...\n');

  const result = await page.evaluate(() => {
    const info = {
      buttons: [],
      textareas: [],
      codeBlocks: [],
      apiTrySection: null
    };
    
    // 查找所有按钮
    document.querySelectorAll('button, a').forEach((el, i) => {
      const text = el.textContent.trim();
      if (text.includes('获取') || text.includes('试用') || text.includes('执行')) {
        info.buttons.push({
          index: i,
          text: text,
          tag: el.tagName,
          className: el.className
        });
      }
    });
    
    // 查找所有textarea
    document.querySelectorAll('textarea').forEach((el, i) => {
      const value = (el.value || '').trim();
      info.textareas.push({
        index: i,
        className: el.className,
        hasValue: value.length > 0,
        valuePreview: value.substring(0, 200)
      });
    });
    
    // 查找所有代码块
    document.querySelectorAll('pre, code').forEach((el, i) => {
      const text = (el.textContent || '').trim();
      if (text.includes('{') && text.length > 10) {
        info.codeBlocks.push({
          index: i,
          tag: el.tagName,
          className: el.className,
          preview: text.substring(0, 200)
        });
      }
    });
    
    // 查找API试用区域
    const sections = Array.from(document.querySelectorAll('h2, h3, div, section'));
    const apiSection = sections.find(el => el.textContent && el.textContent.includes('API试用'));
    if (apiSection) {
      info.apiTrySection = {
        tag: apiSection.tagName,
        className: apiSection.className,
        html: apiSection.outerHTML.substring(0, 500)
      };
    }
    
    return info;
  });

  console.log('分析结果:');
  console.log(JSON.stringify(result, null, 2));
  
  await page.screenshot({ path: 'debug-measures.png', fullPage: true });
  console.log('\n已保存截图: debug-measures.png');
  
  console.log('\n等待30秒后关闭...');
  await page.waitForTimeout(30000);
  
  await browser.close();
})();
