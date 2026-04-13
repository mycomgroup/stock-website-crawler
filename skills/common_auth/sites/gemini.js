export default {
  id: 'gemini',
  name: 'Gemini',
  domain: '.google.com',
  loginUrl: 'https://gemini.google.com/',
  dashboardUrl: 'https://gemini.google.com/app',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const resp = await fetch('https://gemini.google.com/api/user/info', {
        headers: {
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
      });

      if (!resp.ok) return false;
      const json = await resp.json();
      return json && (json.email || json.id || json.user_id);
    } catch (e) {
      try {
        const homeResp = await fetch('https://gemini.google.com/', { headers: { 'Cookie': cookieHeader } });
        const html = await homeResp.text();
        return html.includes('signed-in') || html.includes('Gemini');
      } catch {
        return false;
      }
    }
  },

  async checkLoggedIn(page) {
    try {
      const chatInput = await page.$('textarea[placeholder*="Enter"], textarea, .chat-input');
      const signInBtn = await page.$('button:has-text("Sign in"), a:has-text("Sign in")');
      return !!chatInput && !signInBtn;
    } catch (e) {
      const url = page.url();
      return !url.includes('/signin') && !url.includes('/accounts.google.com');
    }
  },

  async automatedLogin(page, credentials) {
    const username = credentials.GEMINI_USERNAME || credentials.GOOGLE_EMAIL;
    const password = credentials.GEMINI_PASSWORD || credentials.GOOGLE_PASSWORD;
    
    if (!username || !password) throw new Error('未发现 Google/Gemini 账号凭证');
    
    console.log('🔑 正在执行 Gemini 自动填表登录...');
    
    await page.waitForTimeout(3000);
    
    const signInBtn = await page.$('button:has-text("Sign in"), a:has-text("Sign in")');
    if (signInBtn) {
      await signInBtn.click();
      console.log('   ✓ 点击登录按钮');
      await page.waitForTimeout(3000);
    }
    
    const emailInput = await page.$('input[type="email"], input[name="email"]');
    if (emailInput) {
      await emailInput.fill(username);
      console.log('   ✓ 已填写邮箱');
      await page.waitForTimeout(500);
      
      const nextBtn = await page.$('button:has-text("Next"), button[type="submit"]');
      if (nextBtn) await nextBtn.click();
      await page.waitForTimeout(3000);
    }
    
    const passwordInput = await page.$('input[type="password"]');
    if (passwordInput) {
      await passwordInput.fill(password);
      console.log('   ✓ 已填写密码');
      await page.waitForTimeout(500);
      
      const nextBtn = await page.$('button:has-text("Next"), button[type="submit"]');
      if (nextBtn) await nextBtn.click();
      console.log('   ✓ 点击提交');
    }
    
    await page.waitForTimeout(5000);
  }
};
