export default {
  id: 'guorn',
  name: '果仁网',
  domain: '.guorn.com',
  loginUrl: 'https://guorn.com/user/login',
  dashboardUrl: 'https://guorn.com/user/profile',
  
  async verifySession(cookies) {
    const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    try {
      const res = await fetch('https://guorn.com/user/profile', {
        headers: { 
          'Cookie': cookieHeader,
          'Accept': 'application/json',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
      });
      if (res.status === 401) return { success: false, message: 'Cookie 已过期' };
      const json = await res.json().catch(() => ({}));
      
      if (json.status === 'ok' && json.data && json.data.username) {
        return { success: true, user: json.data.username };
      }
      return { success: false, message: '无法识别用户信息' };
    } catch (e) {
      return { success: false, message: `网络错误: ${e.message}` };
    }
  },

  async checkLoggedIn(page) {
    const url = page.url();
    return !url.includes('/user/login');
  },

  async automatedLogin(page, credentials) {
    const username = credentials.GUORN_USERNAME || credentials.GUORN_USER;
    const password = credentials.GUORN_PASSWORD || credentials.GUORN_PASS;
    
    if (!username || !password) throw new Error('未发现果仁网账号凭证');
    
    console.log('🔑 正在执行 Guorn 自动填表登录...');
    
    await page.waitForTimeout(2000);
    
    try {
      const passwordTabs = await page.locator('a, div, span, button').filter({ hasText: '密码登录' }).all();
      for (const tab of passwordTabs) {
        if (await tab.isVisible({ timeout: 1000 }).catch(() => false)) {
          console.log('  切换到密码登录...');
          await tab.click();
          await page.waitForTimeout(1500);
          break;
        }
      }
    } catch (e) {
      console.log('  未找到密码登录标签，尝试直接登录...');
    }

    const phoneSelectors = [
      '#login-Id',
      'input[name="account"]',
      'input[placeholder*="手机"]',
      'input[placeholder*="账号"]',
      'input[type="text"]:visible'
    ];
    
    let filled = false;
    for (const sel of phoneSelectors) {
      const input = page.locator(sel).first();
      if (await input.isVisible({ timeout: 2000 }).catch(() => false)) {
        console.log(`  找到用户名输入框: ${sel}`);
        await input.fill(username);
        filled = true;
        break;
      }
    }
    if (!filled) throw new Error('无法找到用户名输入框');

    const passwordSelectors = [
      '#login-password',
      'input[type="password"]:visible'
    ];
    
    filled = false;
    for (const sel of passwordSelectors) {
      const input = page.locator(sel).first();
      if (await input.isVisible({ timeout: 2000 }).catch(() => false)) {
        console.log(`  找到密码输入框: ${sel}`);
        await input.fill(password);
        filled = true;
        break;
      }
    }
    if (!filled) throw new Error('无法找到密码输入框');

    const loginSelectors = [
      '#sign-in',
      'button[type="submit"]:has-text("登录")',
      'button:visible:has-text("登录")',
      'input[type="submit"]:visible'
    ];
    
    let clicked = false;
    for (const sel of loginSelectors) {
      const btn = page.locator(sel).first();
      if (await btn.isVisible({ timeout: 2000 }).catch(() => false)) {
        console.log(`  找到登录按钮: ${sel}`);
        await btn.click();
        clicked = true;
        break;
      }
    }
    if (!clicked) throw new Error('无法找到登录按钮');

    await page.waitForTimeout(5000);
    
    const isLoggedIn = !page.url().includes('/user/login');
    if (!isLoggedIn) {
      throw new Error('登录失败，请检查用户名密码或网络连接');
    }
    
    console.log('  登录成功');
    return { success: true };
  }
};
