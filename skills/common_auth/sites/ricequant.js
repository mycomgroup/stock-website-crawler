export default {
  id: 'ricequant',
  name: '米筐',
  domain: '.ricequant.com',
  loginUrl: 'https://www.ricequant.com/login',
  dashboardUrl: 'https://www.ricequant.com/algorithms',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const resp = await fetch('https://www.ricequant.com/api/user/isLogin.do', {
        method: 'POST',
        headers: {
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (!resp.ok) return false;
      const json = await resp.json();
      if (json.code === 0 && (json.userId || json.user_id)) {
        return { success: true, user: json.fullname || json.username || json.userId };
      }
      return { success: false, message: json.message || '未登录' };
    } catch (e) {
      return { success: false, message: e.message };
    }
  },

  async checkLoggedIn(page) {
    const url = page.url();
    if (url.includes('/login')) return false;
    
    try {
      const loginBtn = await page.$('button:has-text("登录")');
      const userInfo = await page.$('.user-info, .user-avatar, [class*="user"]');
      return !loginBtn || userInfo;
    } catch (e) {
      return !url.includes('/login');
    }
  },

  async automatedLogin(page, credentials) {
    const username = credentials.RICEQUANT_USERNAME || credentials.RICEQUANT_USER;
    const password = credentials.RICEQUANT_PASSWORD || credentials.RICEQUANT_PASS;
    
    if (!username || !password) throw new Error('未发现米筐账号凭证');
    
    console.log('🔑 正在执行 RiceQuant 自动填表登录...');
    
    await page.waitForTimeout(2000);
    
    const loginBtn = await page.$('button:has-text("登录")');
    if (loginBtn) {
      await loginBtn.click();
      console.log('   ✓ 点击登录按钮打开模态框');
      await page.waitForTimeout(2000);
    }
    
    await page.click('text=密码登录');
    console.log('   ✓ 切换到密码登录模式');
    await page.waitForTimeout(1000);
    
    const usernameInput = page.locator('input[placeholder="国内手机号或邮箱"]');
    const passwordInput = page.locator('input[type="password"]');
    
    if (!(await usernameInput.count()) || !(await passwordInput.count())) {
      throw new Error('未找到用户名或密码输入框');
    }
    
    await usernameInput.click();
    await page.waitForTimeout(100);
    await usernameInput.fill(username);
    console.log('   ✓ 已填写用户名');
    
    await page.waitForTimeout(500);
    
    await passwordInput.click();
    await page.waitForTimeout(100);
    await passwordInput.fill(password);
    console.log('   ✓ 已填写密码');
    
    await page.waitForTimeout(500);
    
    await page.click('button.btn--submit:has-text("登录")');
    console.log('   ✓ 点击提交按钮');
    
    await page.waitForTimeout(3000);
  }
};
