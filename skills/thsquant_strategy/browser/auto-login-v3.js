#!/usr/bin/env node
/**
 * THSQuant 自动登录工具 v3
 * 使用evaluate直接操作DOM
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoLoginV3() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 自动登录工具 v3');
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

  try {
    // 1. 打开平台
    console.log('\n步骤1: 打开平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 2. 点击登录按钮
    console.log('\n步骤2: 点击登录按钮...');
    await page.click('a:has-text("登录")');
    console.log('已点击登录按钮');
    await page.waitForTimeout(3000);

    // 3. 找到登录iframe
    console.log('\n步骤3: 查找登录iframe...');
    const frameElement = await page.$('iframe[src*="upass"]');
    if (!frameElement) {
      throw new Error('未找到登录iframe');
    }

    const loginFrame = await frameElement.contentFrame();
    console.log('找到登录iframe');

    // 等待iframe加载
    await loginFrame.waitForTimeout(2000);

    // 4. 在iframe中执行登录操作
    console.log('\n步骤4: 执行登录操作...');

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-step4-${Date.now()}.png`) });

    // 使用evaluate直接操作DOM
    const loginResult = await loginFrame.evaluate((creds) => {
      const { username, password } = creds;
      const result = { steps: [] };

      // 步骤1: 查找并点击"密码登录"
      const passwordTabs = document.querySelectorAll('.tab-item, [class*="tab"]');
      result.steps.push(`找到 ${passwordTabs.length} 个tab元素`);

      for (const tab of passwordTabs) {
        if (tab.textContent.includes('密码')) {
          tab.click();
          result.steps.push('点击了密码登录tab');
          break;
        }
      }

      // 查找所有可点击的"密码登录"元素
      const allElements = document.querySelectorAll('*');
      for (const el of allElements) {
        if (el.textContent === '密码登录' || el.textContent === '帐号密码登录') {
          el.click();
          result.steps.push(`点击了: ${el.textContent}`);
          break;
        }
      }

      return result;
    }, { username, password });

    console.log('步骤结果:', loginResult.steps);

    // 等待切换到密码登录界面
    await loginFrame.waitForTimeout(2000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-after-tab-${Date.now()}.png`) });

    // 5. 填写账号密码
    console.log('\n步骤5: 填写账号密码...');

    const fillResult = await loginFrame.evaluate((creds) => {
      const { username, password } = creds;
      const result = { success: false, steps: [] };

      // 查找所有input元素
      const inputs = document.querySelectorAll('input');
      result.steps.push(`找到 ${inputs.length} 个input元素`);

      let usernameInput = null;
      let passwordInput = null;

      for (const input of inputs) {
        const type = input.type;
        const name = input.name;
        const placeholder = input.placeholder;

        result.steps.push(`input: type=${type}, name=${name}, placeholder=${placeholder}`);

        if (type === 'text' || type === 'tel') {
          usernameInput = input;
        }
        if (type === 'password') {
          passwordInput = input;
        }
      }

      if (usernameInput && passwordInput) {
        // 填写账号
        usernameInput.value = '';
        usernameInput.focus();
        usernameInput.value = username;
        usernameInput.dispatchEvent(new Event('input', { bubbles: true }));
        usernameInput.dispatchEvent(new Event('change', { bubbles: true }));
        result.steps.push(`账号已填写: ${username}`);

        // 填写密码
        passwordInput.value = '';
        passwordInput.focus();
        passwordInput.value = password;
        passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
        passwordInput.dispatchEvent(new Event('change', { bubbles: true }));
        result.steps.push('密码已填写');

        result.success = true;
        result.usernameInput = usernameInput.name || usernameInput.id;
        result.passwordInput = passwordInput.name || passwordInput.id;
      }

      return result;
    }, { username, password });

    console.log('填写结果:', fillResult.steps);
    console.log('成功:', fillResult.success);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-filled-${Date.now()}.png`) });

    // 6. 点击登录按钮
    console.log('\n步骤6: 点击登录按钮...');

    await loginFrame.waitForTimeout(1000);

    const clickResult = await loginFrame.evaluate(() => {
      const result = { success: false, steps: [] };

      // 查找登录按钮
      const buttons = document.querySelectorAll('button, input[type="submit"], a.btn');
      result.steps.push(`找到 ${buttons.length} 个按钮`);

      for (const btn of buttons) {
        const text = btn.textContent || btn.value || '';
        result.steps.push(`按钮: ${text.substring(0, 20)}`);

        if (text.includes('登录') || text.includes('登 录')) {
          btn.click();
          result.success = true;
          result.steps.push('点击了登录按钮');
          break;
        }
      }

      // 如果没找到，尝试其他方式
      if (!result.success) {
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
          submitBtn.click();
          result.success = true;
          result.steps.push('点击了submit按钮');
        }
      }

      return result;
    });

    console.log('点击结果:', clickResult.steps);

    // 7. 等待登录完成
    console.log('\n步骤7: 等待登录完成...');
    await page.waitForTimeout(5000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-after-submit-${Date.now()}.png`) });

    // 8. 检查登录状态
    console.log('\n步骤8: 检查登录状态...');

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

    // 9. 如果登录成功，测试API
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
              resultType: data.result ? (Array.isArray(data.result) ? 'array' : typeof data.result) : null,
              resultPreview: data.result ? JSON.stringify(data.result).substring(0, 200) : null
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
          console.log(`  ✓ ${ep}: 成功 (${data.resultType})`);
          if (data.resultPreview) {
            console.log(`    ${data.resultPreview}`);
          }
        } else {
          console.log(`  ✗ ${ep}: errorcode=${data.errorcode}`);
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

    console.log('\n浏览器保持打开60秒，可以手动检查...');
    await page.waitForTimeout(60000);

    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);

    try {
      await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-${Date.now()}.png`) });
    } catch (e) {}

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

autoLoginV3().then(() => {
  console.log('\n✓ 完成');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});