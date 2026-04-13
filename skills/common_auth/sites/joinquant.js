export default {
  id: 'joinquant',
  name: '聚宽',
  domain: '.joinquant.com',
  loginUrl: 'https://www.joinquant.com/user/login',
  dashboardUrl: 'https://www.joinquant.com/algorithm/index/list',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const resp = await fetch('https://www.joinquant.com/algorithm/index/list', {
        headers: {
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
          'Referer': 'https://www.joinquant.com/',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
      });

      if (!resp.ok) return { success: false, message: `HTTP ${resp.status}` };
      const html = await resp.text();
      
      if (html.includes('登录') && !html.includes('策略列表') && !html.includes('算法回测')) {
        return { success: false, message: '页面判定为未登录状态' };
      }

      if (html.includes('退出') || html.includes('logout') || html.includes('algorithmId')) {
         return { success: true, user: 'JoinQuant User' };
      }
      
      return { success: false, message: '无法识别登录特征' };
    } catch (e) {
      return { success: false, message: e.message };
    }
  },

  async checkLoggedIn(page) {
    const url = page.url();
    return !url.includes('/user/login');
  },

  async automatedLogin(page, credentials) {
    const username = credentials.JOINQUANT_USERNAME || credentials.JOINQUANT_USER;
    const password = credentials.JOINQUANT_PASSWORD || credentials.JOINQUANT_PASS;
    
    if (!username || !password) throw new Error('未发现聚宽账号凭证');
    
    console.log('🔑 正在执行 JoinQuant 自动填表登录...');
    
    await page.waitForTimeout(2000);
    
    await page.locator('text=密码登录').click();
    console.log('   ✓ 点击密码登录标签');
    await page.waitForTimeout(500);
    
    const usernameInput = page.locator('input[name="username"]');
    const passwordInput = page.locator('input[name="pwd"]');
    
    if (!(await usernameInput.count()) || !(await passwordInput.count())) {
      throw new Error('未找到用户名或密码输入框');
    }
    
    await usernameInput.fill('');
    await usernameInput.fill(username);
    console.log('   ✓ 已填写用户名');
    
    await passwordInput.fill('');
    await passwordInput.fill(password);
    console.log('   ✓ 已填写密码');
    
    await page.locator('input[type="checkbox"]').check({ force: true });
    console.log('   ✓ 已勾选同意协议');
    
    await page.waitForTimeout(300);
    
    const submitBtn = page.locator('button.btnPwdSubmit');
    if (await submitBtn.count()) {
      await submitBtn.click({ force: true });
      console.log('   ✓ 点击提交按钮');
    } else {
      await passwordInput.press('Enter');
      console.log('   ✓ 按 Enter 提交');
    }
    
    await Promise.race([
      page.waitForURL(url => !url.includes('/user/login/'), { timeout: 15000 }).catch(() => null),
      page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => null),
      page.waitForTimeout(5000)
    ]);
    
    await page.waitForTimeout(2000);
  }
};
