export default {
  id: 'chatgpt',
  name: 'ChatGPT',
  domain: 'chatgpt.com',
  loginUrl: 'https://chatgpt.com/auth/login',
  dashboardUrl: 'https://chatgpt.com/',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const resp = await fetch('https://chatgpt.com/backend-api/me', {
        headers: {
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
      });

      if (!resp.ok) return { success: false };
      const json = await resp.json();
      if (json.id && json.email) {
        return { success: true, user: json.email };
      }
      return { success: false };
    } catch (e) {
      return { success: false, message: e.message };
    }
  },

  async checkLoggedIn(page) {
    const url = page.url();
    if (url.includes('/auth/login') || url.includes('/signup')) return false;
    
    try {
      const chatInput = await page.$('[data-testid="chat-input"], textarea[placeholder*="Message"]');
      return !!chatInput;
    } catch (e) {
      return !url.includes('/auth');
    }
  },

  async automatedLogin(page, credentials) {
    const username = credentials.CHATGPT_USERNAME || credentials.OPENAI_EMAIL;
    const password = credentials.CHATGPT_PASSWORD || credentials.OPENAI_PASSWORD;
    
    if (!username || !password) throw new Error('未发现 ChatGPT 账号凭证');
    
    console.log('🔑 正在执行 ChatGPT 自动填表登录...');
    
    await page.waitForTimeout(3000);
    
    const loginBtn = await page.$('button:has-text("Log in"), button:has-text("登录")');
    if (loginBtn) {
      await loginBtn.click();
      console.log('   ✓ 点击登录按钮');
      await page.waitForTimeout(2000);
    }
    
    const emailInput = await page.$('input[type="email"], input[name="email"]');
    if (emailInput) {
      await emailInput.fill(username);
      console.log('   ✓ 已填写邮箱');
      await page.waitForTimeout(500);
      
      const continueBtn = await page.$('button:has-text("Continue"), button[type="submit"]');
      if (continueBtn) await continueBtn.click();
      await page.waitForTimeout(2000);
    }
    
    const passwordInput = await page.$('input[type="password"]');
    if (passwordInput) {
      await passwordInput.fill(password);
      console.log('   ✓ 已填写密码');
      await page.waitForTimeout(500);
      
      const submitBtn = await page.$('button:has-text("Continue"), button[type="submit"]');
      if (submitBtn) await submitBtn.click();
      console.log('   ✓ 点击提交');
    }
    
    await page.waitForTimeout(5000);
  }
};
