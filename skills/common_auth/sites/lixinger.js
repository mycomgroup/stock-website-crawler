export default {
  id: 'lixinger',
  name: '理杏仁',
  domain: '.lixinger.com',
  loginUrl: 'https://www.lixinger.com/login',
  dashboardUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/cn',
  loginApi: 'https://www.lixinger.com/api/account/sign-in/by-account',
  
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
    return !url.includes('/login') && !url.includes('/user/login');
  },

  buildCookieFromHeader(setCookies) {
    if (!setCookies || setCookies.length === 0) return null;
    
    const cookieStr = setCookies
      .map(c => c.split(';')[0].trim())
      .filter(Boolean)
      .join('; ');
    
    if (!cookieStr) return null;
    
    return cookieStr.split(';')
      .map(item => item.trim())
      .filter(Boolean)
      .map(item => {
        const [name, ...rest] = item.split('=');
        return {
          name,
          value: rest.join('='),
          domain: '.lixinger.com',
          path: '/',
          secure: true,
          sameSite: 'Lax'
        };
      });
  },

  async apiLogin(credentials) {
    const username = credentials.LIXINGER_USERNAME || credentials.LIXINGER_USER;
    const password = credentials.LIXINGER_PASSWORD || credentials.LIXINGER_PASS;
    
    if (!username || !password) throw new Error('未发现理杏仁账号凭证');
    
    console.log('🔑 正在执行 Lixinger API 登录...');
    
    const response = await fetch(this.loginApi, {
      method: 'POST',
      headers: {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/json;charset=UTF-8',
        'referer': 'https://www.lixinger.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
      },
      body: JSON.stringify({ accountName: username, password })
    });

    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`API 登录失败 ${response.status}: ${text.slice(0, 500)}`);
    }

    const setCookies = response.headers.getSetCookie ? response.headers.getSetCookie() : [];
    const cookies = this.buildCookieFromHeader(setCookies);
    
    if (!cookies || cookies.length === 0) {
      throw new Error('API 登录成功但未返回 Cookie');
    }
    
    console.log('  ✓ API 登录成功，获取到 Cookie');
    return cookies;
  },

  async automatedLogin(page, credentials) {
    if (!page) {
      return await this.apiLogin(credentials);
    }
    
    const username = credentials.LIXINGER_USERNAME || credentials.LIXINGER_USER;
    const password = credentials.LIXINGER_PASSWORD || credentials.LIXINGER_PASS;
    
    if (!username || !password) throw new Error('未发现理杏仁账号凭证');
    
    console.log('🔑 正在执行 Lixinger 浏览器填表登录...');
    
    await page.waitForTimeout(2000);
    
    try {
      const passwordTabs = await page.locator('a, div, span, button, li')
        .filter({ hasText: /密码登录|账号登录|普通登录/ }).all();
      for (const tab of passwordTabs) {
        if (await tab.isVisible({ timeout: 5000 }).catch(() => false)) {
          console.log('  ✓ 切换到密码登录');
          await tab.click();
          await page.waitForTimeout(1500);
          break;
        }
      }
    } catch (e) {
      console.log('  未找到密码登录标签，尝试直接登录...');
    }

    const usernameSelectors = [
      'input[name="username"]',
      'input[name="account"]',
      'input[name="phone"]',
      'input[placeholder*="用户名"]',
      'input[placeholder*="账号"]',
      'input[placeholder*="手机"]',
      'input[placeholder*="邮箱"]',
      'input[type="text"]:visible'
    ];
    
    let filled = false;
    for (const sel of usernameSelectors) {
      const input = page.locator(sel).first();
      if (await input.isVisible({ timeout: 30000 }).catch(() => false)) {
        console.log(`  ✓ 找到用户名输入框: ${sel}`);
        await input.fill(username);
        filled = true;
        break;
      }
    }
    if (!filled) throw new Error('无法找到用户名输入框');

    const passwordSelectors = [
      'input[name="password"]',
      'input[name="pwd"]',
      'input[placeholder*="密码"]',
      'input[type="password"]:visible'
    ];
    
    filled = false;
    for (const sel of passwordSelectors) {
      const input = page.locator(sel).first();
      if (await input.isVisible({ timeout: 30000 }).catch(() => false)) {
        console.log(`  ✓ 找到密码输入框: ${sel}`);
        await input.fill(password);
        filled = true;
        break;
      }
    }
    if (!filled) throw new Error('无法找到密码输入框');

    const loginSelectors = [
      'button[type="submit"]',
      'button.btn-login',
      'button:has-text("登录")',
      'button:visible:has-text("登")',
      'input[type="submit"]',
      'a:has-text("登录")'
    ];
    
    let clicked = false;
    for (const sel of loginSelectors) {
      const btn = page.locator(sel).first();
      if (await btn.isVisible({ timeout: 10000 }).catch(() => false)) {
        console.log(`  ✓ 找到登录按钮: ${sel}`);
        await btn.click();
        clicked = true;
        break;
      }
    }
    if (!clicked) {
      await page.keyboard.press('Enter');
      console.log('  ✓ 按 Enter 提交');
    }

    await Promise.race([
      page.waitForURL(url => !url.includes('/login'), { timeout: 15000 }).catch(() => null),
      page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => null),
      page.waitForTimeout(8000)
    ]);
    
    await page.waitForTimeout(2000);
    
    const isLoggedIn = await this.checkLoggedIn(page);
    if (!isLoggedIn) {
      throw new Error('浏览器登录失败，请检查用户名密码或网络连接');
    }
    
    console.log('  ✓ 浏览器登录成功');
    return { success: true };
  }
};