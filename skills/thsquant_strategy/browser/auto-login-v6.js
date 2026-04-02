#!/usr/bin/env node
/**
 * THSQuant 自动登录工具 v6 - 处理验证码
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoLoginV6() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 自动登录工具 v6 - 处理验证码');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

  console.log(`\n账号: ${username}`);
  console.log('注意: 登录可能需要手动完成验证码');

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
      const unameInput = document.querySelector('#uname, input[placeholder*="用户名"]');
      if (unameInput) {
        unameInput.value = creds.username;
        unameInput.dispatchEvent(new Event('input', { bubbles: true }));
      }

      const passwdInput = document.querySelector('#passwd, input[type="password"]');
      if (passwdInput) {
        passwdInput.value = creds.password;
        passwdInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }, { username, password });

    console.log('账号密码已填写');
    await loginFrame.waitForTimeout(1000);

    // 5. 点击登录按钮
    console.log('\n步骤5: 点击登录按钮...');
    await loginFrame.evaluate(() => {
      const btn = document.querySelector('.submit_btn');
      if (btn) btn.click();
    });

    console.log('已点击登录按钮');
    await page.waitForTimeout(3000);

    // 6. 检查是否有验证码弹窗
    console.log('\n步骤6: 检查验证码...');

    const verifyCheck = await loginFrame.evaluate(() => {
      const result = { hasVerify: false, type: null };

      // 检查滑块验证码
      const slider = document.querySelector('[class*="slide"], [class*="slider"], .verify-slide');
      if (slider) {
        result.hasVerify = true;
        result.type = 'slider';
      }

      // 检查图片验证码
      const imgVerify = document.querySelector('[class*="verify-img"], .captcha-img, img[src*="captcha"]');
      if (imgVerify) {
        result.hasVerify = true;
        result.type = 'image';
      }

      // 检查错误提示
      const errorEl = document.querySelector('[class*="error"], .error-msg, .msg');
      if (errorEl && errorEl.textContent) {
        result.error = errorEl.textContent;
      }

      return result;
    });

    if (verifyCheck.hasVerify) {
      console.log(`\n⚠ 检测到验证码: ${verifyCheck.type}`);
      console.log('请在浏览器中手动完成验证码...');
    } else if (verifyCheck.error) {
      console.log(`\n登录错误: ${verifyCheck.error}`);
    }

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-v6-verify-${Date.now()}.png`) });

    // 7. 等待用户完成验证码
    console.log('\n步骤7: 等待登录完成 (请在30秒内完成验证码)...');

    // 轮询检查登录状态
    let loginSuccess = false;
    for (let i = 0; i < 30; i++) {
      await page.waitForTimeout(1000);

      const status = await page.evaluate(async () => {
        try {
          const resp = await fetch('/platform/user/getauthdata', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'isajax=1'
          });
          const data = await resp.json();
          return data.errorcode;
        } catch (e) {
          return -1;
        }
      });

      if (status === 0) {
        loginSuccess = true;
        console.log(`\n✓ 登录成功! (${i + 1}秒)`);
        break;
      }

      process.stdout.write(`\r等待登录... ${i + 1}/30秒`);
    }

    // 8. 如果登录成功，测试API
    if (loginSuccess) {
      console.log('\n\n步骤8: 测试API...');

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
              preview: data.result ? JSON.stringify(data.result).substring(0, 200) : null
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
          if (data.preview) console.log(`    ${data.preview}`);
        } else {
          console.log(`  ✗ ${ep}: errorcode=${data.errorcode}`);
        }
      });

      fs.writeFileSync(path.join(OUTPUT_ROOT, 'api-tests-success.json'), JSON.stringify(apiTests, null, 2));
    } else {
      console.log('\n\n⚠ 登录未成功，可能需要手动完成验证码');
    }

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));
    console.log('\n✓ Session已保存');

    console.log('\n浏览器保持打开60秒，可以手动操作...');
    await page.waitForTimeout(60000);

    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-v6-${Date.now()}.png`) });
    fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2));
    await browser.close();
    throw error;
  }
}

autoLoginV6().then(() => console.log('\n✓ 完成')).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});