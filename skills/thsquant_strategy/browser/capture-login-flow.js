#!/usr/bin/env node
/**
 * THSQuant 完整登录流程捕获
 * 打开登录页面，捕获所有认证相关的请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureFullLogin() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 完整登录流程捕获');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

  console.log('\n账号:', username);

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
  let reqId = 0;

  page.on('request', req => {
    const url = req.url();
    const id = reqId++;
    allRequests.push({
      id,
      url,
      method: req.method(),
      postData: req.postData(),
      headers: req.headers(),
      time: Date.now()
    });

    // 打印关键请求
    if (url.includes('login') || url.includes('auth') || url.includes('passport') ||
        url.includes('session') || url.includes('token') || url.includes('cookie')) {
      console.log(`\n[${id}] ${req.method()} ${url.split('?')[0]}`);
      if (req.postData()) {
        console.log(`    Body: ${req.postData().substring(0, 100)}`);
      }
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    const req = allRequests.find(r => r.url === url && !r.status);
    if (req) {
      req.status = resp.status();
      try {
        const body = await resp.text();
        req.response = body.substring(0, 1000);

        // 打印关键响应
        if (url.includes('login') || url.includes('auth') || url.includes('passport')) {
          console.log(`    Status: ${req.status}`);
          if (body.length < 300) {
            console.log(`    Response: ${body}`);
          } else {
            try {
              const json = JSON.parse(body);
              console.log(`    Response: ${JSON.stringify(json).substring(0, 150)}`);
            } catch (e) {
              console.log(`    Response: ${body.substring(0, 100)}...`);
            }
          }
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
    const loginBtn = await page.$('.header-login-btn, .login-btn, [class*="login"]');
    if (loginBtn) {
      await loginBtn.click();
      console.log('已点击登录按钮');
      await page.waitForTimeout(5000);
    }

    // 3. 检查登录iframe
    console.log('\n步骤3: 检查登录iframe...');
    const frames = page.frames();
    console.log(`发现 ${frames.length} 个frame`);

    let loginFrame = null;
    for (const frame of frames) {
      const frameUrl = frame.url();
      console.log(`  Frame: ${frameUrl}`);
      if (frameUrl.includes('passport') || frameUrl.includes('login')) {
        loginFrame = frame;
        console.log('  -> 找到登录frame!');
      }
    }

    // 4. 如果找到登录frame，填写表单
    if (loginFrame) {
      console.log('\n步骤4: 填写登录表单...');

      // 等待表单加载
      await loginFrame.waitForTimeout(2000);

      // 尝试各种选择器
      const selectors = {
        username: [
          'input[name="username"]',
          'input[name="account"]',
          'input[type="text"]',
          '#username',
          '#account',
          '.username-input',
          '.account-input'
        ],
        password: [
          'input[name="password"]',
          'input[type="password"]',
          '#password',
          '.password-input'
        ],
        submit: [
          'button[type="submit"]',
          'input[type="submit"]',
          '.login-btn',
          '.submit-btn',
          'button:has-text("登录")',
          'a:has-text("登录")'
        ]
      };

      let usernameInput = null;
      let passwordInput = null;
      let submitBtn = null;

      for (const sel of selectors.username) {
        try {
          usernameInput = await loginFrame.$(sel);
          if (usernameInput) {
            console.log(`  找到username: ${sel}`);
            break;
          }
        } catch (e) {}
      }

      for (const sel of selectors.password) {
        try {
          passwordInput = await loginFrame.$(sel);
          if (passwordInput) {
            console.log(`  找到password: ${sel}`);
            break;
          }
        } catch (e) {}
      }

      for (const sel of selectors.submit) {
        try {
          submitBtn = await loginFrame.$(sel);
          if (submitBtn) {
            console.log(`  找到submit: ${sel}`);
            break;
          }
        } catch (e) {}
      }

      if (usernameInput && passwordInput) {
        console.log('\n填写账号密码...');
        await usernameInput.fill(username);
        await loginFrame.waitForTimeout(500);
        await passwordInput.fill(password);
        await loginFrame.waitForTimeout(1000);

        if (submitBtn) {
          console.log('点击登录...');
          await submitBtn.click();
          await page.waitForTimeout(5000);
        }
      } else {
        console.log('未找到登录表单元素');
        console.log('请在浏览器中手动登录...');
      }
    } else {
      // 尝试主页面登录
      console.log('\n尝试在主页面查找登录表单...');

      const usernameInput = await page.$('input[name="username"], input[type="text"]');
      const passwordInput = await page.$('input[name="password"], input[type="password"]');

      if (usernameInput && passwordInput) {
        await usernameInput.fill(username);
        await page.waitForTimeout(500);
        await passwordInput.fill(password);
        await page.waitForTimeout(1000);

        const submitBtn = await page.$('button[type="submit"], .login-btn');
        if (submitBtn) {
          await submitBtn.click();
          await page.waitForTimeout(5000);
        }
      } else {
        console.log('请在浏览器中手动登录...');
      }
    }

    // 5. 等待登录完成
    console.log('\n步骤5: 等待登录完成...');
    console.log('请在浏览器中完成登录操作');
    console.log('登录成功后，等待30秒自动保存...');

    await page.waitForTimeout(30000);

    // 6. 检查登录状态
    console.log('\n步骤6: 检查登录状态...');

    const loginStatus = await page.evaluate(async () => {
      // 检查页面内容
      const body = document.body.innerHTML;
      const hasLogout = body.includes('退出') || body.includes('logout');
      const hasUserInfo = body.includes('HI') || body.includes('您好') || body.includes(username);

      // 检查localStorage
      const storageKeys = Object.keys(localStorage);

      // 调用API
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

      return { hasLogout, hasUserInfo, storageKeys, apiStatus };
    });

    console.log('登录状态:', {
      有退出按钮: loginStatus.hasLogout,
      有用户信息: loginStatus.hasUserInfo,
      API状态: loginStatus.apiStatus
    });

    // 7. 保存所有数据
    console.log('\n步骤7: 保存数据...');

    // 保存cookies
    const cookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies,
      timestamp: Date.now()
    }, null, 2));
    console.log(`Session已保存: ${cookies.length} cookies`);

    // 保存请求日志
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'login-flow-requests.json'),
      JSON.stringify(allRequests, null, 2));
    console.log(`请求日志: ${allRequests.length} 个请求`);

    // 8. 如果登录成功，测试API
    if (loginStatus.apiStatus && loginStatus.apiStatus.errorcode === 0) {
      console.log('\n✓ 登录成功! 测试API...');

      const apiTests = await page.evaluate(async () => {
        const results = {};
        const endpoints = [
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
            results[ep] = await resp.json();
          } catch (e) {
            results[ep] = { error: e.message };
          }
        }
        return results;
      });

      console.log('\nAPI测试结果:');
      Object.entries(apiTests).forEach(([ep, data]) => {
        console.log(`  ${ep}: errorcode=${data.errorcode}`);
        if (data.result) {
          console.log(`    结果: ${JSON.stringify(data.result).substring(0, 80)}`);
        }
      });
    }

    await browser.close();

    return { loginStatus, requests: allRequests };

  } catch (error) {
    console.error('\n错误:', error.message);

    // 保存已捕获的数据
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'login-flow-error.json'),
      JSON.stringify({ error: error.message, requests: allRequests }, null, 2));

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

captureFullLogin().then(result => {
  console.log('\n' + '='.repeat(70));
  console.log('✓ 完成');
  console.log('='.repeat(70));
  console.log('\n查看:');
  console.log('  - data/session.json');
  console.log('  - data/login-flow-requests.json');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});