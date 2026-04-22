export default {
  id: 'thsquant',
  name: '同花顺量化 (thsquant)',
  domain: '.10jqka.com.cn',
  loginUrl: 'https://quant.10jqka.com.cn/view/study-index.html',
  dashboardUrl: 'https://quant.10jqka.com.cn/view/study-index.html',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    // 使用量化平台的检查登录接口
    const res = await fetch('https://quant.10jqka.com.cn/unified/check-login', {
      headers: {
        'Cookie': cookieHeader,
        'Accept': 'application/json'
      }
    });
    const data = await res.json().catch(() => ({}));
    if (data.code === 200 || data.code === 0) {
      return { success: true, user: data.data?.username || '已登录' };
    }
    // Fallback: fetch dashboard page and look for username pattern
    try {
      const dashRes = await fetch('https://quant.10jqka.com.cn/view/study-index.html', {
        headers: { 'Cookie': cookieHeader }
      });
      const text = await dashRes.text();
      const match = text.match(/username\s*[:=]\s*"([^"]+)"/i);
      if (match) {
        return { success: true, user: match[1] };
      }
    } catch (_) {}
    return { success: false, message: data.message || 'Cookie 失效' };
  },

  async checkLoggedIn(page) {
    // 1. 检查是否存在登录按钮 (优先通过 ID 检查)
    const isLoginBtnVisible = await page.evaluate(() => {
      const btn = document.querySelector('#header_signup, .login-btn-header');
      if (!btn) return false;
      const rect = btn.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0 && window.getComputedStyle(btn).visibility !== 'hidden';
    });
    
    if (isLoginBtnVisible) return false;

    // 2. 检查是否有已登录的标志
    const isLoggedIn = await page.evaluate(() => {
      // 同花顺量化登录后通常会有这些元素
      const userIndicators = document.querySelector('.user-info, .username-link, .head-img, .head_img, #header_user, .user-name');
      if (userIndicators) return true;
      
      const bodyText = document.body.innerText;
      // “退出登录”是比较稳健的登录标志
      if (bodyText.includes('退出登录') || bodyText.includes('个人中心')) return true;
      
      // 检查全局变量 (同花顺常用的)
      if (window.v_username || window.USER_NAME) return true;
      
      return false;
    });

    return isLoggedIn;
  },

  async automatedLogin(page, credentials) {
    const username = credentials.THSQUANT_USERNAME || credentials.THS_USER;
    const password = credentials.THSQUANT_PASSWORD || credentials.THS_PASS;
    
    if (!username || !password) throw new Error('未发现同花顺量化账号凭证 (THSQUANT_USERNAME/PASSWORD)');
    
    console.log('🔑 正在执行 THSQuant 自动填表登录...');
    
    // 1. 等待登录按钮并点击（如果表单没直接显示）
    const loginTrigger = await page.$('#header_signup, .login-btn-header');
    if (loginTrigger) {
      await loginTrigger.click();
      await page.waitForTimeout(1000);
    }

    // 2. 处理跨域 iframe
    const iframeElement = await page.waitForSelector('iframe[src*="upass.10jqka"]', { timeout: 30000 });
    const frame = await iframeElement.contentFrame();
    if (!frame) throw new Error('无法获取登录 iframe');

    // 3. 点击"密码登录"标签
    await frame.click('a:has-text("密码登录"), :has-text("密码登录")').catch(() => {});
    await page.waitForTimeout(500);

    // 4. 填表
    await frame.fill('input#username, input[name="username"]', username);
    await frame.fill('input#password, input[name="password"]', password);
    
    // 5. 点击登录
    const submitBtn = await frame.$('#loginBtn, button[type="submit"]');
    if (submitBtn) {
      await submitBtn.click();
    } else {
      await frame.keyboard.press('Enter');
    }
    
    // 等待登录成功后的调整
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  }
};
