import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { SESSION_FILE, DATA_DIR } from '../paths.js';
import { saveSession } from './session-manager.js';

const START_URL = 'https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest';

export async function login() {
  const username = process.env.THSQUANT_USERNAME;
  const password = process.env.THSQUANT_PASSWORD;

  if (!username || !password) {
    console.error('❌ 错误: .env 文件中未配置 THSQUANT_USERNAME 或 THSQUANT_PASSWORD');
    process.exit(1);
  }

  console.log('🚀 启动浏览器执行自动登录...');
  
  const browser = await chromium.launch({
    headless: process.env.PLAYWRIGHT_HEADLESS !== 'false',
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  
  const page = await context.newPage();
  
  try {
    console.log(`正在打开: ${START_URL}`);
    await page.goto(START_URL, { waitUntil: 'networkidle', timeout: 60000 });
    
    // 检查是否已经登录 (检测左上角是否有 "登录" 字样)
    const loginLink = await page.$('a:has-text("登录")');
    if (!loginLink) {
      console.log('✅ 检测到已处于登录状态。');
    } else {
      console.log('🔑 未登录，正在触发登录弹窗...');
      await loginLink.click();
      
      // 等待登录 Iframe 加载
      console.log('⏳ 等待登录 Iframe...');
      const iframeElement = await page.waitForSelector('iframe[src*="upass.10jqka.com.cn"]', { timeout: 15000 });
      const frame = await iframeElement.contentFrame();
      
      if (!frame) throw new Error('无法访问登录 Iframe');

      // 1. 切换到“密码登录”标签
      console.log('👉 切换到密码登录...');
      await frame.click('a:has-text("密码登录")').catch(() => {});
      
      // 2. 填写账号密码
      console.log('✍️ 正在填写凭据...');
      await frame.fill('input#uname', username);
      await frame.fill('input#passwd', password);
      
      // 3. 点击登录
      console.log('👆 点击登录按钮...');
      await frame.click('#account_pannel .submit_btn');
      
      // 等待登录成功跳转 (检测页面是否刷新或弹窗消失)
      console.log('⏳ 等待认证结果...');
      await page.waitForFunction(() => !document.querySelector('iframe[src*="upass.10jqka.com.cn"]'), { timeout: 30000 });
      
      // 额外等待一下让 Cookie 同步
      await page.waitForTimeout(3000);
    }

    const cookies = await context.cookies();
    saveSession(cookies, page.url());
    
    console.log(`\n✅ 登录成功！Session 已更新。`);
    console.log(`📊 捕获到 ${cookies.length} 个 Cookie。`);
    return cookies;
    
  } catch (error) {
    console.error(`\n❌ 自动登录失败: ${error.message}`);
    // 如果失败了，建议用户检查一下是否有验证码弹出
    console.log('提示: 如果遇到滑块验证码，请尝试手动运行一次 npm run login。');
    throw error;
  } finally {
    await browser.close();
  }
}

// Allow running as script
if (process.argv[1] === import.meta.url || process.argv[1]?.endsWith('automated-login.js')) {
  login().catch(e => {
    console.error(e);
    process.exit(1);
  });
}
