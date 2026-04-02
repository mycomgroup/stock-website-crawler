#!/usr/bin/env node
/**
 * THSQuant 自动登录工具 v2
 * 正确处理密码登录流程
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoLoginV2() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 自动登录工具 v2');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

  console.log(`\n账号: ${username}`);

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  const page = await context.newPage();

  // 捕获请求
  const requests = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('/platform/') || url.includes('login') || url.includes('passport') || url.includes('upass')) {
      requests.push({
        url,
        method: req.method(),
        postData: req.postData(),
        time: Date.now()
      });
      console.log(`\n[请求] ${req.method()} ${url.split('?')[0]}`);
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/platform/') || url.includes('login') || url.includes('upass')) {
      try {
        const req = requests.find(r => r.url === url && !r.status);
        if (req) {
          req.status = resp.status();
          const text = await resp.text();
          req.response = text.substring(0, 300);
          console.log(`[响应] ${resp.status()} ${text.substring(0, 100)}`);
        }
      } catch (e) {}
    }
  });

  try {
    // 1. 打开平台
    console.log('\n步骤1: 打开平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 2. 点击登录按钮
    console.log('\n步骤2: 点击登录按钮...');
    const loginBtn = await page.$('a:has-text("登录"), .header-login-btn');
    if (loginBtn) {
      await loginBtn.click();
      console.log('已点击登录按钮');
      await page.waitForTimeout(3000);
    }

    // 3. 找到登录iframe
    console.log('\n步骤3: 查找登录iframe...');
    await page.waitForTimeout(2000);

    const frames = page.frames();
    console.log(`发现 ${frames.length} 个frame`);

    let loginFrame = null;
    for (const frame of frames) {
      try {
        const frameUrl = frame.url();
        console.log(`  ${frameUrl.substring(0, 60)}`);
        if (frameUrl.includes('upass') || frameUrl.includes('login')) {
          loginFrame = frame;
          console.log('  -> 登录iframe');
        }
      } catch (e) {}
    }

    if (!loginFrame) {
      throw new Error('未找到登录iframe');
    }

    // 4. 在iframe中操作
    console.log('\n步骤4: 在登录iframe中操作...');

    // 等待iframe加载完成
    await loginFrame.waitForTimeout(2000);

    // 截图当前状态
    const screenshotPath = path.join(OUTPUT_ROOT, `login-frame-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    console.log(`截图: ${screenshotPath}`);

    // 查找"密码登录"选项并点击
    console.log('\n查找并点击"密码登录"...');

    const passwordLoginSelectors = [
      'text=密码登录',
      'text=帐号密码登录',
      'text=账号密码登录',
      '//span[contains(text(), "密码登录")]',
      '//div[contains(text(), "密码登录")]',
      '//a[contains(text(), "密码")]',
      '.tab-item:has-text("密码")',
      '[class*="tab"]:has-text("密码")'
    ];

    let passwordTabClicked = false;
    for (const sel of passwordLoginSelectors) {
      try {
        let el;
        if (sel.startsWith('//')) {
          el = await loginFrame.locator(`xpath=${sel}`).first();
        } else {
          el = await loginFrame.$(sel);
        }

        if (el) {
          console.log(`  找到: ${sel}`);
          await el.click();
          console.log('  已点击密码登录选项');
          passwordTabClicked = true;
          await loginFrame.waitForTimeout(2000);
          break;
        }
      } catch (e) {
        // 继续尝试下一个选择器
      }
    }

    if (!passwordTabClicked) {
      console.log('  未找到密码登录选项，尝试直接查找输入框...');
    }

    // 再次截图
    const screenshotPath2 = path.join(OUTPUT_ROOT, `login-after-click-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath2 });
    console.log(`截图: ${screenshotPath2}`);

    // 5. 查找并填写账号密码
    console.log('\n步骤5: 填写账号密码...');

    // 等待输入框出现
    await loginFrame.waitForTimeout(1000);

    // 账号输入框选择器
    const usernameSelectors = [
      'input[name="username"]',
      'input[name="account"]',
      'input[placeholder*="账号"]',
      'input[placeholder*="用户名"]',
      'input[type="text"]',
      '#username',
      '#account'
    ];

    // 密码输入框选择器
    const passwordSelectors = [
      'input[name="password"]',
      'input[placeholder*="密码"]',
      'input[type="password"]',
      '#password'
    ];

    let usernameInput = null;
    let passwordInput = null;

    // 查找账号输入框
    for (const sel of usernameSelectors) {
      try {
        usernameInput = await loginFrame.$(sel);
        if (usernameInput) {
          console.log(`  找到账号输入框: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    // 查找密码输入框
    for (const sel of passwordSelectors) {
      try {
        passwordInput = await loginFrame.$(sel);
        if (passwordInput) {
          console.log(`  找到密码输入框: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    if (usernameInput && passwordInput) {
      console.log('\n填写登录信息...');

      // 填写账号
      await usernameInput.click();
      await loginFrame.waitForTimeout(300);
      await usernameInput.fill('');
      await usernameInput.fill(username);
      console.log(`  账号: ${username}`);
      await loginFrame.waitForTimeout(500);

      // 填写密码
      await passwordInput.click();
      await loginFrame.waitForTimeout(300);
      await passwordInput.fill('');
      await passwordInput.fill(password);
      console.log('  密码: ******');
      await loginFrame.waitForTimeout(500);

      // 截图填写后的状态
      const screenshotPath3 = path.join(OUTPUT_ROOT, `login-filled-${Date.now()}.png`);
      await page.screenshot({ path: screenshotPath3 });
      console.log(`截图: ${screenshotPath3}`);

      // 查找登录按钮
      console.log('\n查找登录按钮...');
      const submitSelectors = [
        'button[type="submit"]',
        'button:has-text("登录")',
        'button:has-text("登 录")',
        'input[type="submit"]',
        'a:has-text("登录")',
        '.login-btn',
        '.submit-btn',
        '[class*="login"]:has-text("登录")'
      ];

      let submitBtn = null;
      for (const sel of submitSelectors) {
        try {
          submitBtn = await loginFrame.$(sel);
          if (submitBtn) {
            console.log(`  找到登录按钮: ${sel}`);
            break;
          }
        } catch (e) {}
      }

      if (submitBtn) {
        console.log('\n点击登录按钮...');
        await submitBtn.click();
        console.log('已点击登录按钮');

        // 等待登录完成
        console.log('\n步骤6: 等待登录完成...');
        await page.waitForTimeout(5000);
      } else {
        console.log('\n未找到登录按钮，请手动点击登录');
      }

    } else {
      console.log('\n未找到账号或密码输入框');
      console.log('请在浏览器中手动登录...');
    }

    // 6. 检查登录状态
    console.log('\n步骤7: 检查登录状态...');
    await page.waitForTimeout(3000);

    const loginStatus = await page.evaluate(async () => {
      const body = document.body.innerHTML;
      const hasLogout = body.includes('退出');
      const hasUserInfo = body.includes('HI') || body.includes('您好');

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

      return { hasLogout, hasUserInfo, apiStatus };
    });

    console.log('\n登录状态:');
    console.log(`  有退出按钮: ${loginStatus.hasLogout}`);
    console.log(`  有用户信息: ${loginStatus.hasUserInfo}`);
    console.log(`  API状态: ${loginStatus.apiStatus?.errorcode}`);
    console.log(`  消息: ${loginStatus.apiStatus?.errormsg}`);

    // 7. 如果登录成功，测试API
    if (loginStatus.apiStatus?.errorcode === 0) {
      console.log('\n✓ 登录成功! 测试API...');

      const apiTests = await page.evaluate(async () => {
        const results = {};
        const endpoints = [
          '/platform/user/getauthdata',
          '/platform/strategy/list',
          '/platform/strategy/mylist',
          '/platform/backtest/list'
        ];

        for (const ep of endpoints) {
          try {
            const resp = await fetch(ep, {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: 'isajax=1'
            });
            const data = await resp.json();
            results[ep] = {
              errorcode: data.errorcode,
              hasResult: !!data.result,
              resultPreview: data.result ? JSON.stringify(data.result).substring(0, 150) : null
            };
          } catch (e) {
            results[ep] = { error: e.message };
          }
        }
        return results;
      });

      console.log('\nAPI测试结果:');
      Object.entries(apiTests).forEach(([ep, data]) => {
        if (data.errorcode === 0) {
          console.log(`  ✓ ${ep}: 成功`);
          if (data.resultPreview) {
            console.log(`    ${data.resultPreview}`);
          }
        } else {
          console.log(`  ✗ ${ep}: ${data.errorcode}`);
        }
      });

      fs.writeFileSync(path.join(OUTPUT_ROOT, 'api-tests-success.json'),
        JSON.stringify(apiTests, null, 2));
    }

    // 保存session
    const cookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies,
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    // 保存请求日志
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'login-v2-requests.json'),
      JSON.stringify(requests, null, 2));

    console.log('\n浏览器保持打开30秒...');
    await page.waitForTimeout(30000);

    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);

    try {
      fs.writeFileSync(SESSION_FILE, JSON.stringify({
        cookies: await context.cookies(),
        timestamp: Date.now()
      }, null, 2));
    } catch (e) {}

    // 截图错误状态
    try {
      await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-${Date.now()}.png`) });
    } catch (e) {}

    await browser.close();
    throw error;
  }
}

autoLoginV2().then(() => {
  console.log('\n' + '='.repeat(70));
  console.log('✓ 完成');
  console.log('='.repeat(70));
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});