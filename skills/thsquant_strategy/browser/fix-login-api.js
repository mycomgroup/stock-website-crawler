#!/usr/bin/env node
/**
 * THSQuant 登录修复工具
 * 使用ths_iframe_login正确登录并获取有效session
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function fixLoginAndTestAPIs() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 登录修复与API测试');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

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

  // 捕获所有请求
  const allRequests = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('/platform/') || url.includes('login') || url.includes('auth')) {
      allRequests.push({
        url,
        method: req.method(),
        postData: req.postData(),
        time: Date.now()
      });
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/platform/') || url.includes('login') || url.includes('auth')) {
      try {
        const body = await resp.text();
        const req = allRequests.find(r => r.url === url && !r.status);
        if (req) {
          req.status = resp.status();
          req.response = body.substring(0, 500);
        }
      } catch (e) {}
    }
  });

  try {
    // 1. 打开平台
    console.log('\n步骤1: 打开平台首页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 2. 检查ths_iframe_login
    console.log('\n步骤2: 检查登录组件...');
    const loginInfo = await page.evaluate(() => {
      const info = {};

      if (window.ths_iframe_login) {
        info.hasLoginComponent = true;
        info.loginMethods = Object.keys(window.ths_iframe_login);

        // 尝试获取登录URL
        if (window.ths_iframe_login.getLoginUrl) {
          try {
            info.loginUrl = window.ths_iframe_login.getLoginUrl();
          } catch (e) {}
        }
      }

      // 检查登录按钮
      const loginBtn = document.querySelector('.header-login-btn, .login-btn, [class*="login"]');
      if (loginBtn) {
        info.loginBtnClass = loginBtn.className;
        info.loginBtnText = loginBtn.textContent;
      }

      return info;
    });

    console.log('登录组件:', loginInfo);

    // 3. 点击登录按钮
    console.log('\n步骤3: 触发登录...');

    // 方法1: 通过ths_iframe_login
    if (loginInfo.hasLoginComponent) {
      console.log('使用ths_iframe_login组件...');
      await page.evaluate(() => {
        if (window.ths_iframe_login && window.ths_iframe_login.show) {
          window.ths_iframe_login.show();
        }
      });
      await page.waitForTimeout(2000);
    }

    // 方法2: 点击登录按钮
    const loginBtn = await page.$('.header-login-btn, .login-btn, [class*="login"]');
    if (loginBtn) {
      console.log('点击登录按钮...');
      await loginBtn.click();
      await page.waitForTimeout(3000);
    }

    // 4. 等待登录弹窗
    console.log('\n步骤4: 等待登录界面...');
    await page.waitForTimeout(3000);

    // 检查是否有iframe登录框
    const frames = page.frames();
    console.log(`当前frames: ${frames.length}`);

    for (const frame of frames) {
      try {
        const frameUrl = frame.url();
        console.log(`  Frame: ${frameUrl}`);

        // 在iframe中查找登录表单
        if (frameUrl.includes('login') || frameUrl.includes('passport')) {
          console.log('\n找到登录iframe!');

          // 尝试填写表单
          const usernameInput = await frame.$('input[name="username"], input[type="text"], #username');
          const passwordInput = await frame.$('input[name="password"], input[type="password"], #password');
          const submitBtn = await frame.$('button[type="submit"], input[type="submit"], .login-btn');

          if (usernameInput && passwordInput) {
            console.log('填写登录表单...');
            await usernameInput.fill(username);
            await passwordInput.fill(password);
            await page.waitForTimeout(1000);

            if (submitBtn) {
              console.log('点击登录...');
              await submitBtn.click();
              await page.waitForTimeout(5000);
            }
          }
        }
      } catch (e) {
        console.log(`  Frame error: ${e.message}`);
      }
    }

    // 5. 检查登录状态
    console.log('\n步骤5: 检查登录状态...');
    await page.waitForTimeout(3000);

    const loginStatus = await page.evaluate(async () => {
      // 检查页面内容
      const body = document.body.innerHTML;
      const hasLogoutBtn = body.includes('退出') || body.includes('logout');
      const hasUserInfo = body.includes('HI') || body.includes('您好');

      // 调用API检查
      let apiCheck = null;
      try {
        const resp = await fetch('/platform/user/getauthdata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1'
        });
        apiCheck = await resp.json();
      } catch (e) {
        apiCheck = { error: e.message };
      }

      return {
        hasLogoutBtn,
        hasUserInfo,
        apiCheck
      };
    });

    console.log('登录状态:', {
      有退出按钮: loginStatus.hasLogoutBtn,
      有用户信息: loginStatus.hasUserInfo,
      API检查: loginStatus.apiCheck
    });

    // 6. 如果登录成功，测试API
    if (loginStatus.apiCheck && loginStatus.apiCheck.errorcode === 0) {
      console.log('\n✓ 登录成功! 测试API...');

      const apiResults = await page.evaluate(async () => {
        const results = {};

        const endpoints = [
          '/platform/strategy/list',
          '/platform/strategy/mylist',
          '/platform/backtest/list',
          '/platform/research/strategylist',
          '/platform/simuaccount/getyybidlist',
          '/platform/simupaper/queryall/'
        ];

        for (const endpoint of endpoints) {
          try {
            const resp = await fetch(endpoint, {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: 'isajax=1'
            });
            const data = await resp.json();
            results[endpoint] = {
              status: resp.status,
              errorcode: data.errorcode,
              hasResult: !!data.result,
              resultType: typeof data.result,
              resultPreview: JSON.stringify(data.result).substring(0, 200)
            };
          } catch (e) {
            results[endpoint] = { error: e.message };
          }
        }

        return results;
      });

      console.log('\n' + '='.repeat(70));
      console.log('API测试结果:');
      console.log('='.repeat(70));

      Object.entries(apiResults).forEach(([endpoint, result]) => {
        console.log(`\n${endpoint}:`);
        if (result.error) {
          console.log(`  Error: ${result.error}`);
        } else {
          console.log(`  Status: ${result.status}`);
          console.log(`  Errorcode: ${result.errorcode}`);
          console.log(`  Has Result: ${result.hasResult}`);
          if (result.resultPreview) {
            console.log(`  Preview: ${result.resultPreview}`);
          }
        }
      });

      // 保存API结果
      fs.writeFileSync(path.join(OUTPUT_ROOT, 'api-test-results.json'),
        JSON.stringify(apiResults, null, 2));

    } else {
      console.log('\n⚠ 未能自动登录');
      console.log('请在浏览器中手动登录，登录后按回车继续...');

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

      console.log('重新检查:', recheckStatus);
    }

    // 保存session
    const cookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies,
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    // 保存请求日志
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'login-requests.json'),
      JSON.stringify(allRequests, null, 2));

    console.log('\n浏览器保持打开30秒...');
    await page.waitForTimeout(30000);

    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);

    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    await browser.close();
    throw error;
  }
}

fixLoginAndTestAPIs().then(() => {
  console.log('\n✓ 完成');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});