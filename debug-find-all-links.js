const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LINKS_FILE = path.join(__dirname, 'links.txt');
const ACCOUNT = '13311390323';
const PASSWORD = '3228552';

async function doLogin(page) {
  console.log('尝试登录...');
  await page.waitForTimeout(2000);
  
  // 查找密码输入框
  const pwdInput = page.locator('input[type="password"]').first();
  if (await pwdInput.count() > 0) {
    // 查找手机号输入框
    const phoneSelectors = ['input[placeholder*="手机"]', 'input[placeholder*="账号"]', 'input[type="tel"]', 'input[name="phone"]'];
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
    
    // 查找登录按钮
    const btn = page.locator('button:has-text("登录"), button[type="submit"]').first();
    if (await btn.count() > 0) {
      await btn.click();
      await page.waitForTimeout(4000);
      console.log('登录完成');
    }
  }
}

// 读取已有的URL列表
function readExistingUrls() {
  if (fs.existsSync(LINKS_FILE)) {
    const content = fs.readFileSync(LINKS_FILE, 'utf8');
    return content.split('\n').filter(line => line.trim()).map(line => line.trim());
  }
  return [];
}

// 保存URL列表（排序后）
function saveUrls(urls) {
  const uniqueUrls = [...new Set(urls)]; // 去重
  uniqueUrls.sort(); // 排序
  fs.writeFileSync(LINKS_FILE, uniqueUrls.join('\n') + '\n', 'utf8');
  return uniqueUrls;
}

// 从页面提取所有API文档链接
async function extractApiLinks(page) {
  return await page.evaluate(() => {
    const links = new Set();
    
    // 查找所有包含 api-key 的链接
    document.querySelectorAll('a[href*="api-key="]').forEach((a) => {
      const href = a.getAttribute('href');
      if (href) {
        try {
          let url = href.startsWith('http') ? href : new URL(href, window.location.origin).href;
          // 只保留 doc?api-key= 格式的链接
          if (url.includes('/open/api/doc') && url.includes('api-key=')) {
            links.add(url);
          }
        } catch (_) {}
      }
    });
    
    return Array.from(links);
  });
}

(async () => {
  const browser = await chromium.launch({ headless: false, channel: 'chrome' });
  const context = await browser.newContext();
  const page = await context.newPage();

  // 读取现有URL
  let existingUrls = readExistingUrls();
  console.log(`已有 ${existingUrls.length} 个URL\n`);

  // 如果没有URL，添加一些起始URL
  if (existingUrls.length === 0) {
    existingUrls = [
      'https://www.lixinger.com/open/api/doc',
      'https://www.lixinger.com/open/api/my-apis',
    ];
    console.log('添加起始URL');
  }

  const newUrls = new Set();
  const visitedPages = new Set();

  // 遍历所有URL
  for (const url of existingUrls) {
    if (visitedPages.has(url)) continue;
    visitedPages.add(url);

    console.log(`访问: ${url}`);
    
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);

      // 检查是否需要登录
      if (page.url().includes('login') || (await page.locator('input[type="password"]').count()) > 0) {
        await doLogin(page);
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(2000);
      }

      // 展开所有可能的折叠内容
      await page.evaluate(() => {
        // 展开details
        document.querySelectorAll('details').forEach(d => d.open = true);
        
        // 点击展开按钮
        document.querySelectorAll('button, a, span, div').forEach((el) => {
          const text = (el.textContent || '').trim();
          const className = el.className || '';
          if (text.includes('展开') || text.includes('▶') || 
              className.includes('expand') || className.includes('collapse')) {
            try {
              el.click();
            } catch (_) {}
          }
        });
      });

      await page.waitForTimeout(1500);

      // 提取API链接
      const links = await extractApiLinks(page);
      
      if (links.length > 0) {
        console.log(`  找到 ${links.length} 个API链接`);
        links.forEach(link => {
          if (!existingUrls.includes(link)) {
            newUrls.add(link);
            console.log(`  + ${link}`);
          }
        });
      } else {
        console.log(`  未找到新链接`);
      }

    } catch (e) {
      console.error(`  错误: ${e.message}`);
    }

    await page.waitForTimeout(500);
  }

  // 合并并保存
  const allUrls = [...existingUrls, ...Array.from(newUrls)];
  const savedUrls = saveUrls(allUrls);
  
  console.log(`\n总计: ${savedUrls.length} 个URL`);
  console.log(`新增: ${newUrls.size} 个URL`);
  console.log(`已保存到: ${LINKS_FILE}`);

  await browser.close();
})();
