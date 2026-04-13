export default {
  id: '10jqka',
  name: '问财回测/同花顺',
  domain: '.10jqka.com.cn',
  loginUrl: 'https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest',
  dashboardUrl: 'https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    const res = await fetch('https://backtest.10jqka.com.cn/tradebacktest/yieldbacktest', {
      method: 'POST',
      headers: { 
        'Cookie': cookieHeader,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: '测试' })
    });
    const data = await res.json().catch(() => ({}));
    if (data.errorcode === -401) return { success: false, message: '未授权或 Cookie 已失效' };
    return { success: true, user: '已登录' };
  },

  async checkLoggedIn(page) {
    // 检查左上角是否有 "登录" 文本
    const loginLink = await page.$('a:has-text("登录")');
    return !loginLink;
  },

  async automatedLogin(page, credentials) {
    if (!credentials.username || !credentials.password) throw new Error('未发现同花顺账号凭证');
    
    console.log('🔑 正在执行 10jqka 自动填表登录...');
    
    // 点击登录触发弹窗 (如果没自动弹)
    const loginLink = await page.$('a:has-text("登录")');
    if (loginLink) await loginLink.click();
    
    const iframeElement = await page.waitForSelector('iframe[src*="upass.10jqka.com.cn"]', { timeout: 15000 });
    const frame = await iframeElement.contentFrame();
    
    await frame.click('a:has-text("密码登录")').catch(() => {});
    await frame.fill('input#uname', credentials.username);
    await frame.fill('input#passwd', credentials.password);
    await frame.click('#account_pannel .submit_btn');
    
    // 等待登录 Iframe 消失
    await page.waitForFunction(() => !document.querySelector('iframe[src*="upass.10jqka.com.cn"]'), { timeout: 30000 });
  }
};
