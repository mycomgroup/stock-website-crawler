#!/usr/bin/env node
/**
 * THSQuant 自动登录工具 v4
 * 更完善的密码登录切换
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function autoLoginV4() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 自动登录工具 v4');
  console.log('='.repeat(70));

  const username = process.env.THSQUANT_USERNAME || 'mx_kj1ku00qp';
  const password = process.env.THSQUANT_PASSWORD || 'f09173228552';

  console.log(`\n账号: ${username}`);

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,  // 慢速执行，便于观察
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
    await page.waitForTimeout(2000);

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
    await loginFrame.waitForTimeout(2000);

    // 4. 分析并操作登录界面
    console.log('\n步骤4: 分析登录界面...');

    // 先获取完整的页面结构
    const pageStructure = await loginFrame.evaluate(() => {
      const info = {
        tabs: [],
        inputs: [],
        buttons: [],
        forms: []
      };

      // 查找所有tab
      document.querySelectorAll('[class*="tab"], .tab-item, [role="tab"]').forEach(el => {
        info.tabs.push({
          text: el.textContent.trim(),
          className: el.className,
          active: el.classList.contains('active') || el.className.includes('active')
        });
      });

      // 查找所有input
      document.querySelectorAll('input').forEach(el => {
        info.inputs.push({
          type: el.type,
          name: el.name,
          placeholder: el.placeholder,
          visible: el.offsetParent !== null,
          display: window.getComputedStyle(el).display
        });
      });

      // 查找所有按钮
      document.querySelectorAll('button, [role="button"], .btn, input[type="submit"]').forEach(el => {
        info.buttons.push({
          text: (el.textContent || el.value || '').trim().substring(0, 30),
          className: el.className,
          type: el.type || 'button',
          visible: el.offsetParent !== null
        });
      });

      // 查找表单
      document.querySelectorAll('form').forEach(el => {
        info.forms.push({
          id: el.id,
          className: el.className,
          action: el.action
        });
      });

      return info;
    });

    console.log('\n页面结构分析:');
    console.log('Tabs:', pageStructure.tabs);
    console.log('可见Inputs:', pageStructure.inputs.filter(i => i.visible));
    console.log('可见Buttons:', pageStructure.buttons.filter(b => b.visible));
    console.log('Forms:', pageStructure.forms);

    // 5. 点击密码登录tab
    console.log('\n步骤5: 切换到密码登录...');

    const switchResult = await loginFrame.evaluate(() => {
      const result = { found: false, clicked: false };

      // 查找所有包含"密码"文字的元素
      const allElements = document.querySelectorAll('*');
      for (const el of allElements) {
        const text = el.textContent.trim();
        if (text === '密码登录' || text === '帐号密码登录' || text === '账号密码登录') {
          result.found = true;
          result.element = el.tagName;
          result.className = el.className;

          // 点击
          el.click();
          result.clicked = true;
          break;
        }
      }

      return result;
    });

    console.log('切换结果:', switchResult);

    // 等待界面切换动画
    console.log('\n等待界面切换...');
    await loginFrame.waitForTimeout(2000);

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-v4-after-switch-${Date.now()}.png`) });

    // 6. 再次分析界面，找到密码登录的输入框
    console.log('\n步骤6: 查找密码登录输入框...');

    const inputInfo = await loginFrame.evaluate(() => {
      const info = { inputs: [] };

      // 查找所有可见的输入框
      document.querySelectorAll('input').forEach(el => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);

        info.inputs.push({
          type: el.type,
          name: el.name,
          placeholder: el.placeholder,
          id: el.id,
          visible: rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden',
          x: rect.x,
          y: rect.y,
          width: rect.width,
          height: rect.height
        });
      });

      return info;
    });

    console.log('输入框信息:', inputInfo.inputs);

    // 7. 填写账号密码
    console.log('\n步骤7: 填写账号密码...');

    const fillResult = await loginFrame.evaluate((creds) => {
      const { username, password } = creds;
      const result = { success: false, steps: [] };

      // 找到可见的text/tel输入框作为账号
      const inputs = Array.from(document.querySelectorAll('input'));
      const visibleInputs = inputs.filter(el => {
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
      });

      result.steps.push(`可见输入框数量: ${visibleInputs.length}`);

      // 查找用户名输入框
      const usernameInput = visibleInputs.find(el =>
        el.type === 'text' &&
        (el.placeholder?.includes('用户名') || el.placeholder?.includes('账号') || el.placeholder?.includes('手机'))
      ) || visibleInputs.find(el => el.type === 'text');

      // 查找密码输入框
      const passwordInput = visibleInputs.find(el => el.type === 'password');

      if (usernameInput) {
        result.steps.push(`找到用户名输入框: placeholder=${usernameInput.placeholder}`);

        // 模拟用户输入
        usernameInput.focus();
        usernameInput.click();
        usernameInput.value = username;

        // 触发事件
        ['focus', 'input', 'change', 'blur'].forEach(eventType => {
          usernameInput.dispatchEvent(new Event(eventType, { bubbles: true }));
        });

        result.steps.push(`已填写用户名: ${username}`);
      }

      if (passwordInput) {
        result.steps.push(`找到密码输入框: placeholder=${passwordInput.placeholder}`);

        passwordInput.focus();
        passwordInput.click();
        passwordInput.value = password;

        ['focus', 'input', 'change', 'blur'].forEach(eventType => {
          passwordInput.dispatchEvent(new Event(eventType, { bubbles: true }));
        });

        result.steps.push('已填写密码');
      }

      result.success = !!(usernameInput && passwordInput);
      return result;
    }, { username, password });

    console.log('填写结果:', fillResult.steps);

    // 截图填写后状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-v4-filled-${Date.now()}.png`) });

    // 8. 查找并点击登录按钮
    console.log('\n步骤8: 查找登录按钮...');

    await loginFrame.waitForTimeout(1000);

    // 分析当前按钮
    const buttonInfo = await loginFrame.evaluate(() => {
      const buttons = [];

      document.querySelectorAll('button, input[type="submit"], input[type="button"], .btn, [role="button"]').forEach(el => {
        const rect = el.getBoundingClientRect();
        const text = (el.textContent || el.value || '').trim();

        buttons.push({
          tag: el.tagName,
          text: text.substring(0, 30),
          type: el.type,
          visible: rect.width > 0 && rect.height > 0,
          className: el.className.substring(0, 50),
          x: rect.x,
          y: rect.y
        });
      });

      return buttons;
    });

    console.log('按钮列表:');
    buttonInfo.filter(b => b.visible).forEach(b => {
      console.log(`  ${b.tag}: "${b.text}" (${b.className})`);
    });

    // 点击登录按钮
    const clickResult = await loginFrame.evaluate(() => {
      const result = { success: false, clicked: null };

      // 查找包含"登录"文字的按钮
      const allButtons = document.querySelectorAll('button, input[type="submit"], .btn, [role="button"]');

      for (const btn of allButtons) {
        const text = (btn.textContent || btn.value || '').trim();

        // 排除"获取验证码"等按钮
        if ((text.includes('登录') || text.includes('登 录')) && !text.includes('验证码')) {
          btn.click();
          result.success = true;
          result.clicked = text;
          break;
        }
      }

      // 如果没找到特定的登录按钮，尝试点击第一个可见的submit按钮
      if (!result.success) {
        const submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn) {
          submitBtn.click();
          result.success = true;
          result.clicked = 'submit button';
        }
      }

      return result;
    });

    console.log('点击结果:', clickResult);

    // 9. 等待登录完成
    console.log('\n步骤9: 等待登录完成...');
    await page.waitForTimeout(5000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `login-v4-after-submit-${Date.now()}.png`) });

    // 10. 检查登录状态
    console.log('\n步骤10: 检查登录状态...');

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

    // 11. 如果登录成功，测试API
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

    console.log('\n浏览器保持打开60秒...');
    await page.waitForTimeout(60000);

    await browser.close();

  } catch (error) {
    console.error('\n错误:', error.message);

    try {
      await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-v4-${Date.now()}.png`) });
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

autoLoginV4().then(() => {
  console.log('\n✓ 完成');
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});