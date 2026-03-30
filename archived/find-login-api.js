import { chromium } from 'playwright';

async function findLoginAPI() {
  console.log('=== Finding RiceQuant Login API ===\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 拦截所有请求
  const requests = [];
  page.on('request', request => {
    requests.push({
      method: request.method(),
      url: request.url(),
      headers: request.headers(),
      postData: request.postData()
    });
  });
  
  page.on('response', response => {
    const url = response.url();
    if (url.includes('/api/') || url.includes('/auth/')) {
      console.log(`Response: ${response.status()} ${url}`);
    }
  });
  
  try {
    console.log('1. Visiting login page...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);
    
    // 列出所有捕获的请求
    console.log('\n2. All API requests captured:');
    const apiRequests = requests.filter(r => r.url.includes('ricequant.com'));
    apiRequests.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req.method} ${req.url}`);
    });
    
    // 查找登录按钮
    console.log('\n3. Finding login button...');
    const loginButtons = await page.$$('button:has-text("登录")');
    console.log(`   Found ${loginButtons.length} login buttons`);
    
    if (loginButtons.length > 0) {
      // 点击登录按钮
      console.log('\n4. Clicking login button...');
      await loginButtons[0].click();
      await page.waitForTimeout(3000);
      
      // 检查是否出现了登录模态框
      console.log('\n5. Looking for login form...');
      const inputs = await page.$$('input');
      console.log(`   Found ${inputs.length} inputs`);
      
      // 列出所有输入框
      for (let i = 0; i < inputs.length; i++) {
        const type = await inputs[i].getAttribute('type');
        const name = await inputs[i].getAttribute('name');
        const placeholder = await inputs[i].getAttribute('placeholder');
        console.log(`   Input ${i + 1}: type=${type}, name=${name}, placeholder=${placeholder}`);
      }
      
      // 截图以便查看
      await page.screenshot({ path: 'login-modal.png', fullPage: true });
      console.log('\n   ✓ Screenshot saved to login-modal.png');
    }
    
    // 检查新捕获的请求
    console.log('\n6. New API requests after click:');
    const newRequests = requests.filter(r => 
      r.url.includes('ricequant.com') && 
      !r.url.includes('.js') && 
      !r.url.includes('.css') &&
      !r.url.includes('.png') &&
      !r.url.includes('.jpg') &&
      !r.url.includes('isLogin.do')
    );
    
    newRequests.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req.method} ${req.url}`);
      if (req.postData) {
        console.log(`     PostData: ${req.postData.substring(0, 200)}`);
      }
    });
    
    // 尝试模拟登录请求
    console.log('\n7. Trying common login endpoints...');
    const testEndpoints = [
      '/api/v1/auth/login',
      '/api/v2/auth/login',
      '/api/auth/login',
      '/api/user/login',
      '/api/user/login.do',
      '/auth/login',
      '/login',
    ];
    
    for (const endpoint of testEndpoints) {
      try {
        const resp = await page.evaluate(async (ep) => {
          const url = ep.startsWith('http') ? ep : `https://www.ricequant.com${ep}`;
          try {
            const response = await fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify({
                username: 'test',
                password: 'test'
              })
            });
            return {
              url: url,
              status: response.status,
              contentType: response.headers.get('content-type'),
              text: (await response.text()).substring(0, 200)
            };
          } catch (e) {
            return {
              url: url,
              error: e.message
            };
          }
        }, endpoint);
        
        console.log(`  ${resp.url}: ${resp.status || 'error'} (${resp.contentType || ''})`);
        if (resp.text && resp.text.includes('json')) {
          console.log(`    Response: ${resp.text}`);
        }
      } catch (e) {}
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

findLoginAPI();
