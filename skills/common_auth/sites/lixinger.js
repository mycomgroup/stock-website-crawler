export default {
  id: 'lixinger',
  name: '理杏仁',
  domain: '.lixinger.com',
  loginUrl: 'https://www.lixinger.com/login',
  dashboardUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/cn',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const resp = await fetch('https://www.lixinger.com/api/company/screener/dates', {
        method: 'POST',
        headers: {
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ areaCode: 'cn' })
      });

      if (!resp.ok) return { success: false, message: `HTTP ${resp.status}` };
      const json = await resp.json();
      if (json && json.priceMetricsDate) {
        return { success: true, user: '理杏仁用户' };
      }
      return { success: false, message: '未返回有效数据' };
    } catch (e) {
      return { success: false, message: e.message };
    }
  },

  async checkLoggedIn(page) {
    const url = page.url();
    return !url.includes('/login');
  },

  async automatedLogin(page, credentials) {
    const username = credentials.LIXINGER_USERNAME || credentials.LIXINGER_USER;
    const password = credentials.LIXINGER_PASSWORD || credentials.LIXINGER_PASS;
    
    if (!username || !password) throw new Error('未发现理杏仁账号凭证');
    
    console.log('🔑 正在执行 Lixinger 自动填表登录...');
    
    await page.waitForTimeout(2000);
    
    const usernameInput = await page.$('input[name="username"], input[type="text"], input[placeholder*="用户名"]');
    const passwordInput = await page.$('input[type="password"]');
    
    if (!usernameInput || !passwordInput) {
      throw new Error('未找到用户名或密码输入框');
    }
    
    await usernameInput.click();
    await usernameInput.fill(username);
    console.log('   ✓ 已填写用户名');
    
    await passwordInput.click();
    await passwordInput.fill(password);
    console.log('   ✓ 已填写密码');
    
    await page.waitForTimeout(500);
    
    const submitBtn = await page.$('button[type="submit"], button:has-text("登录")');
    if (submitBtn) {
      await submitBtn.click();
      console.log('   ✓ 点击提交按钮');
    } else {
      await page.keyboard.press('Enter');
      console.log('   ✓ 按 Enter 提交');
    }
    
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);
  }
};
