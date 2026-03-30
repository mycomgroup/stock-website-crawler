import { chromium } from 'playwright';

async function exploreAPI() {
  console.log('=== Exploring RiceQuant API ===\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 拦截所有网络请求
  const requests = [];
  page.on('request', request => {
    const url = request.url();
    if (url.includes('ricequant.com') && (url.includes('/api/') || url.includes('/auth/'))) {
      requests.push({
        method: request.method(),
        url: url,
        headers: request.headers(),
        postData: request.postData()
      });
    }
  });
  
  try {
    console.log('Visiting ricequant.com to find API endpoints...');
    await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    console.log('\nCaptured API requests:');
    if (requests.length === 0) {
      console.log('  No API requests captured on homepage');
    } else {
      requests.forEach((req, i) => {
        console.log(`  ${i + 1}. ${req.method} ${req.url}`);
      });
    }
    
    // 尝试访问登录页面
    console.log('\nVisiting login page...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    // 获取页面信息
    const title = await page.title();
    console.log(`Page title: ${title}`);
    
    // 查找表单
    const forms = await page.$$('form');
    console.log(`\nFound ${forms.length} forms`);
    
    for (let i = 0; i < forms.length; i++) {
      const action = await forms[i].getAttribute('action');
      const method = await forms[i].getAttribute('method');
      console.log(`  Form ${i + 1}: ${method || 'GET'} ${action || 'no action'}`);
      
      // 查找输入字段
      const inputs = await forms[i].$$('input');
      for (const input of inputs) {
        const type = await input.getAttribute('type');
        const name = await input.getAttribute('name');
        const placeholder = await input.getAttribute('placeholder');
        console.log(`    - ${name || 'unnamed'} (${type || 'text'}): ${placeholder || ''}`);
      }
    }
    
    // 检查是否有登录按钮
    const buttons = await page.$$('button');
    console.log(`\nFound ${buttons.length} buttons:`);
    for (const btn of buttons) {
      const text = await btn.textContent();
      const type = await btn.getAttribute('type');
      console.log(`  - ${type || 'button'}: "${text?.trim()}"`);
    }
    
    console.log('\nCaptured API requests after login page:');
    const loginRequests = requests.filter(r => r.url.includes('login') || r.url.includes('auth'));
    if (loginRequests.length === 0) {
      console.log('  No login-related API requests');
    } else {
      loginRequests.forEach((req, i) => {
        console.log(`  ${i + 1}. ${req.method} ${req.url}`);
      });
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

exploreAPI();
