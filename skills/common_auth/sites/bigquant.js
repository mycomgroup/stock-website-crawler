export default {
  id: 'bigquant',
  name: 'BigQuant',
  domain: '.bigquant.com',
  loginUrl: 'https://bigquant.com',
  dashboardUrl: 'https://bigquant.com/',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const resp = await fetch('https://bigquant.com/bigapis/auth/v1/users/me', {
        headers: {
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
      });

      if (!resp.ok) return { success: false, message: `HTTP ${resp.status}` };
      const json = await resp.json();
      if (json.code === 0 && json.data && (json.data.username || json.data.id)) {
        return { success: true, user: json.data.username || json.data.id };
      }
      return { success: false, message: json.message || '未登录' };
    } catch (e) {
      return { success: false, message: e.message };
    }
  },

  async checkLoggedIn(page) {
    try {
      const loginBtn = await page.$('button:has-text("登录")');
      const userAvatar = await page.$('[class*="avatar"], [class*="user"]');
      return !loginBtn || userAvatar;
    } catch (e) {
      const url = page.url();
      return !url.includes('/login');
    }
  },

  async automatedLogin(page, credentials) {
    const username = credentials.BIGQUANT_USERNAME || credentials.BIGQUANT_USER;
    const password = credentials.BIGQUANT_PASSWORD || credentials.BIGQUANT_PASS;
    
    if (!username || !password) throw new Error('未发现 BigQuant 账号凭证');
    
    console.log('🔑 正在执行 BigQuant 自动填表登录...');
    
    await page.waitForTimeout(3000);
    
    const loginBtn = page.locator('button:has-text("登录")');
    if (!(await loginBtn.count())) {
      throw new Error('未找到登录按钮');
    }
    await loginBtn.click();
    console.log('   ✓ 点击登录按钮打开模态框');
    await page.waitForTimeout(3000);
    
    const passwordTab = page.locator('text=密码登录');
    if (!(await passwordTab.count())) {
      throw new Error('未找到密码登录选项');
    }
    await passwordTab.click();
    console.log('   ✓ 切换到密码登录模式');
    await page.waitForTimeout(2000);
    
    const usernameInput = page.locator('input[placeholder="请输入用户名"]');
    const passwordInput = page.locator('input[placeholder="请输入登录密码"]');
    
    if (!(await usernameInput.count()) || !(await passwordInput.count())) {
      throw new Error('未找到用户名或密码输入框');
    }
    
    await usernameInput.click();
    await usernameInput.fill(username);
    console.log('   ✓ 已填写用户名');
    
    await page.waitForTimeout(5000);
    
    await passwordInput.click();
    await passwordInput.fill(password);
    console.log('   ✓ 已填写密码');
    
    await page.waitForTimeout(3000);
    
    const submitBtn = await page.$('.ant-modal-content button:has-text("登录")');
    if (submitBtn) {
      await submitBtn.click({ force: true });
      console.log('   ✓ 点击提交按钮');
    } else {
      await page.keyboard.press('Enter');
      console.log('   ✓ 按 Enter 提交');
    }
    
    await page.waitForTimeout(10000);
  }
};
