#!/usr/bin/env node
/**
 * THSQuant 自动登录工具 v5 - 最终版
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoLoginV5() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 自动登录工具 v5');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

  console.log(`\n账号: ${username}`);

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    slowMo: 50,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  const page = await context.newPage();

  try {
    // 1. 打开平台并点击登录
    console.log('\n步骤1: 打开平台并点击登录...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.click('a:has-text("登录")');
    await page.waitForTimeout(3000);

    // 2. 获取登录iframe
    console.log('\n步骤2: 获取登录iframe...');
    const frameElement = await page.$('iframe[src*="upass"]');
    const loginFrame = await frameElement.contentFrame();
    await loginFrame.waitForTimeout(2000);

    // 3. 切换到密码登录
    console.log('\n步骤3: 切换到密码登录...');
    await loginFrame.evaluate(() => {
      const items = document.querySelectorAll('.nav-item, [class*="nav-item"]');
      for (const item of items) {
        if (item.textContent.includes('密码')) {
          item.click();
          return true;
        }
      }
      return false;
    });
    await loginFrame.waitForTimeout(2000);

    // 4. 填写账号密码
    console.log('\n步骤4: 填写账号密码...');
    await loginFrame.evaluate((creds) => {
      // 用户名
      const unameInput = document.querySelector('#uname, input[placeholder*="用户名"]');
      if (unameInput) {
        unameInput.value = creds.username;
        unameInput.dispatchEvent(new Event('input', { bubbles: true }));
      }

      // 密码
      const passwdInput = document.querySelector('#passwd, input[type="password"]');
      if (passwdInput) {
        passwdInput.value = creds.password;
        passwdInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }, { username, password });

    console.log('账号密码已填写');
    await loginFrame.waitForTimeout(1000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-v5-filled-${Date.now()}.png`) });

    // 5. 点击登录按钮
    console.log('\n步骤5: 点击登录按钮...');

    const clickResult = await loginFrame.evaluate(() => {
      // 尝试多种选择器
      const selectors = [
        '.login_btn',
        '[class*="login_btn"]',
        '[class*="login-btn"]',
        '.submit_btn',
        '[class*="submit"]',
        'button[type="submit"]'
      ];

      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            el.click();
            return { success: true, selector: sel, text: el.textContent };
          }
        }
      }

      // 查找所有可点击元素
      const clickables = document.querySelectorAll('[onclick], [role="button"], .btn, .button, a[href="#"]');
      for (const el of clickables) {
        const text = el.textContent.trim();
        if (text.includes('登录') || text.includes('登 录') || text === '登录') {
          el.click();
          return { success: true, selector: 'text-based', text };
        }
      }

      return { success: false };
    });

    console.log('点击结果:', clickResult);

    // 6. 等待登录完成
    console.log('\n步骤6: 等待登录完成...');
    await page.waitForTimeout(5000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-v5-after-login-${Date.now()}.png`) });

    // 7. 检查登录状态
    console.log('\n步骤7: 检查登录状态...');
    const loginStatus = await page.evaluate(async () => {
      let apiStatus = null;
      try {
        const resp = await fetch('/platform/user/getauthdata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1'
        });
        apiStatus = await resp.json();
      } catch (e) {
        apiStatus = { error: e.message };
      }
      return { apiStatus };
    });

    console.log('API状态:', loginStatus.apiStatus?.errorcode);
    console.log('消息:', loginStatus.apiStatus?.errormsg);

    // 8. 如果登录成功，测试API
    if (loginStatus.apiStatus?.errorcode === 0) {
      console.log('\n✓ 登录成功! 测试API...');

      const apiTests = await page.evaluate(async () => {
        const results = {};
        for (const ep of ['/platform/strategy/list', '/platform/strategy/mylist', '/platform/backtest/list']) {
          try {
            const resp = await fetch(ep, {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: 'isajax=1'
            });
            const data = await resp.json();
            results[ep] = { errorcode: data.errorcode, hasResult: !!data.result };
            if (data.result) {
              results[ep].preview = JSON.stringify(data.result).substring(0, 150);
            }
          } catch (e) {
            results[ep] = { error: e.message };
          }
        }
        return results;
      });

      console.log('\nAPI测试结果:');
      Object.entries(apiTests).forEach(([ep, data]) => {
        console.log(`  ${ep}: ${data.errorcode === 0 ? '✓ 成功' : '✗ 失败'}`);
        if (data.preview) console.log(`    ${data.preview}`);
      });

      fs.writeFileSync(path.join(OUTPUT_ROOT, 'api-tests-success.json'), JSON.stringify(apiTests, null, 2));
    }

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    console.log('\n浏览器保持打开30秒...');
    await page.waitForTimeout(30000);
    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-v5-${Date.now()}.png`) });
    fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2));
    await browser.close();
    throw error;
  }
}

autoLoginV5().then(() => console.log('\n✓ 完成')).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});