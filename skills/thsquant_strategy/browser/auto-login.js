#!/usr/bin/env node
/**
 * THSQuant 自动登录工具
 * 切换到密码登录方式并自动输入账号密码
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoLogin() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 自动登录工具');
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
    if (url.includes('/platform/') || url.includes('login') || url.includes('passport')) {
      requests.push({
        url,
        method: req.method(),
        postData: req.postData(),
        time: Date.now()
      });
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/platform/') || url.includes('login')) {
      try {
        const req = requests.find(r => r.url === url && !r.status);
        if (req) {
          req.status = resp.status();
          req.response = await resp.text();
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

    // 尝试多种登录按钮选择器
    const loginSelectors = [
      '.header-login-btn',
      '.login-btn',
      '[class*="login"]',
      'a:has-text("登录")',
      'button:has-text("登录")'
    ];

    let loginBtn = null;
    for (const sel of loginSelectors) {
      try {
        loginBtn = await page.$(sel);
        if (loginBtn) {
          console.log(`  找到登录按钮: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    if (loginBtn) {
      await loginBtn.click();
      console.log('  已点击登录按钮');
      await page.waitForTimeout(3000);
    } else {
      console.log('  未找到登录按钮，尝试通过JS触发');
      await page.evaluate(() => {
        if (window.ths_iframe_login && window.ths_iframe_login.show) {
          window.ths_iframe_login.show();
        }
      });
      await page.waitForTimeout(3000);
    }

    // 3. 查找登录iframe或弹窗
    console.log('\n步骤3: 查找登录界面...');

    // 等待登录弹窗出现
    await page.waitForTimeout(2000);

    // 检查所有frames
    const frames = page.frames();
    console.log(`  发现 ${frames.length} 个frame`);

    let loginFrame = null;
    for (const frame of frames) {
      try {
        const frameUrl = frame.url();
        console.log(`    Frame: ${frameUrl.substring(0, 60)}`);

        // 检查是否是登录相关frame
        if (frameUrl.includes('passport') || frameUrl.includes('login') ||
            frameUrl.includes('upass') || frameUrl.includes('auth')) {
          loginFrame = frame;
          console.log('    -> 可能是登录frame');
        }
      } catch (e) {}
    }

    // 4. 在登录界面中操作
    console.log('\n步骤4: 在登录界面中操作...');

    // 首先尝试在主页面找登录元素
    let foundInMain = false;

    // 检查是否有"密码登录"选项
    console.log('\n  查找"密码登录"选项...');

    const passwordLoginSelectors = [
      'text=密码登录',
      'text=帐号密码登录',
      'text=账号密码登录',
      '[class*="password"]',
      '[class*="pwd"]',
      'a:has-text("密码")',
      'span:has-text("密码")',
      'div:has-text("密码登录")'
    ];

    // 先在主页面找
    for (const sel of passwordLoginSelectors) {
      try {
        const el = await page.$(sel);
        if (el) {
          console.log(`  主页面找到: ${sel}`);
          await el.click();
          await page.waitForTimeout(1000);
          foundInMain = true;
          break;
        }
      } catch (e) {}
    }

    // 如果主页面没找到，在iframe中找
    if (!foundInMain && loginFrame) {
      console.log('  在iframe中查找...');
      for (const sel of passwordLoginSelectors) {
        try {
          const el = await loginFrame.$(sel);
          if (el) {
            console.log(`  iframe中找到: ${sel}`);
            await el.click();
            await loginFrame.waitForTimeout(1000);
            foundInMain = true;
            break;
          }
        } catch (e) {}
      }
    }

    // 检查所有frame中是否有登录表单
    for (const frame of frames) {
      if (foundInMain) break;

      try {
        const frameUrl = frame.url();
        if (frameUrl === 'about:blank') continue;

        console.log(`\n  检查frame: ${frameUrl.substring(0, 50)}`);

        // 查找密码登录选项
        for (const sel of passwordLoginSelectors) {
          try {
            const el = await frame.$(sel);
            if (el) {
              console.log(`    找到密码登录: ${sel}`);
              await el.click();
              await frame.waitForTimeout(1000);
              foundInMain = true;
              break;
            }
          } catch (e) {}
        }

        // 查找账号密码输入框
        if (!foundInMain) {
          const usernameInput = await frame.$('input[type="text"], input[name="username"], input[name="account"], #username');
          const passwordInput = await frame.$('input[type="password"], input[name="password"], #password');

          if (usernameInput && passwordInput) {
            console.log('    找到账号密码输入框!');

            // 填写账号
            await usernameInput.click();
            await frame.waitForTimeout(300);
            await usernameInput.fill(username);
            console.log(`    已输入账号: ${username}`);
            await frame.waitForTimeout(500);

            // 填写密码
            await passwordInput.click();
            await frame.waitForTimeout(300);
            await passwordInput.fill(password);
            console.log('    已输入密码');
            await frame.waitForTimeout(500);

            // 查找登录按钮
            const submitSelectors = [
              'button[type="submit"]',
              'input[type="submit"]',
              'button:has-text("登录")',
              'a:has-text("登录")',
              '[class*="submit"]',
              '[class*="login-btn"]'
            ];

            for (const sel of submitSelectors) {
              try {
                const submitBtn = await frame.$(sel);
                if (submitBtn) {
                  console.log(`    找到登录按钮: ${sel}`);
                  await submitBtn.click();
                  console.log('    已点击登录按钮');
                  break;
                }
              } catch (e) {}
            }

            foundInMain = true;
            break;
          }
        }
      } catch (e) {
        console.log(`    错误: ${e.message}`);
      }
    }

    // 如果还是没找到，在主页面再试一次
    if (!foundInMain) {
      console.log('\n  在主页面查找登录表单...');

      const usernameInput = await page.$('input[type="text"]:visible, input[name="username"]:visible, input[name="account"]:visible');
      const passwordInput = await page.$('input[type="password"]:visible');

      if (usernameInput && passwordInput) {
        await usernameInput.fill(username);
        await page.waitForTimeout(300);
        await passwordInput.fill(password);
        await page.waitForTimeout(500);

        const submitBtn = await page.$('button[type="submit"]:visible, button:has-text("登录"):visible');
        if (submitBtn) {
          await submitBtn.click();
          console.log('  已在主页面完成登录');
        }
      }
    }

    // 5. 等待登录完成
    console.log('\n步骤5: 等待登录完成...');
    await page.waitForTimeout(5000);

    // 6. 检查登录状态
    console.log('\n步骤6: 检查登录状态...');

    const loginStatus = await page.evaluate(async () => {
      const body = document.body.innerHTML;
      const hasLogout = body.includes('退出') || body.includes('logout');
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

    console.log('登录状态:', {
      有退出按钮: loginStatus.hasLogout,
      有用户信息: loginStatus.hasUserInfo,
      API状态: loginStatus.apiStatus?.errorcode,
      消息: loginStatus.apiStatus?.errormsg
    });

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
              resultPreview: data.result ? JSON.stringify(data.result).substring(0, 100) : null
            };
          } catch (e) {
            results[ep] = { error: e.message };
          }
        }
        return results;
      });

      console.log('\nAPI测试结果:');
      Object.entries(apiTests).forEach(([ep, data]) => {
        console.log(`  ${ep}:`);
        console.log(`    errorcode: ${data.errorcode}`);
        if (data.hasResult) {
          console.log(`    有结果: ${data.resultPreview}`);
        }
      });

      // 保存API测试结果
      fs.writeFileSync(path.join(OUTPUT_ROOT, 'api-tests-after-login.json'),
        JSON.stringify(apiTests, null, 2));
    } else {
      console.log('\n⚠ 未能完成自动登录');
      console.log('请在浏览器中手动完成登录，然后按回车继续...');

      // 等待用户操作
      await new Promise(resolve => {
        process.stdin.once('data', resolve);
      });

      // 重新检查
      const recheckStatus = await page.evaluate(async () => {
        try {
          const resp = await fetch('/platform/user/getauthdata', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'isajax=1'
          });
          return await resp.json();
        } catch (e) {
          return { error: e.message };
        }
      });

      console.log('\n重新检查登录状态:', recheckStatus);
    }

    // 保存session
    const cookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies,
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    // 保存请求日志
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'login-attempt-requests.json'),
      JSON.stringify(requests, null, 2));

    console.log('\n浏览器保持打开，可以查看状态...');
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

    await browser.close();
    throw error;
  }
}

autoLogin().then(() => {
  console.log('\n✓ 完成');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});