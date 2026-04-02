#!/usr/bin/env node
/**
 * THSQuant 策略提交工具 v2
 * 改进的页面导航和编辑器检测
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function submitStrategy(strategyFile, config = {}) {
  const strategyPath = path.resolve(strategyFile);
  const code = fs.readFileSync(strategyPath, 'utf8');
  const name = config.name || path.basename(strategyPath, '.py');

  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 策略提交工具 v2');
  console.log('='.repeat(70));
  console.log(`\n策略: ${name} (${code.split('\n').length} 行)`);

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 捕获所有请求
  page.on('request', req => {
    const url = req.url();
    if (url.includes('/platform/')) {
      console.log(`[API] ${req.method()} ${url.split('?')[0]}`);
    }
  });

  try {
    // 1. 打开主页面
    console.log('\n步骤1: 打开平台首页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(5000);

    // 检查登录状态
    const loginCheck = await page.evaluate(async () => {
      try {
        const resp = await fetch('/platform/user/getauthdata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1'
        });
        return await resp.json();
      } catch (e) {
        return { errorcode: -1 };
      }
    });

    if (loginCheck.errorcode !== 0) {
      console.log('未登录，请先运行: node browser/auto-login-v6.js');
      await browser.close();
      return { success: false, reason: 'not_logged_in' };
    }
    console.log('✓ 已登录');

    // 2. 导航到策略列表
    console.log('\n步骤2: 导航到策略研究...');
    await page.click('a:has-text("策略研究"), [href*="strategy"]');
    await page.waitForTimeout(3000);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, `v2-step2-${Date.now()}.png`) });

    // 3. 查找并点击新建按钮
    console.log('\n步骤3: 点击新建策略...');

    // 等待页面加载
    await page.waitForTimeout(2000);

    // 查找新建按钮
    const newBtn = await page.$('button:has-text("新建"), .new-btn, [class*="create"]');
    if (newBtn) {
      await newBtn.click();
      console.log('点击了新建按钮');
    } else {
      // 直接导航
      await page.goto('https://quant.10jqka.com.cn/platform/study/html/editor.html');
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `v2-step3-${Date.now()}.png`) });

    // 4. 检查页面结构
    console.log('\n步骤4: 分析页面结构...');

    const pageInfo = await page.evaluate(() => {
      const info = {
        url: window.location.href,
        title: document.title,
        iframes: [],
        editors: []
      };

      // 检查iframe
      document.querySelectorAll('iframe').forEach(iframe => {
        info.iframes.push({
          src: iframe.src,
          id: iframe.id
        });
      });

      // 检查编辑器
      if (window.monaco) info.editors.push('monaco');
      if (window.CodeMirror) info.editors.push('codemirror');
      if (document.querySelector('textarea')) info.editors.push('textarea');

      return info;
    });

    console.log('页面信息:', pageInfo);

    // 5. 如果有iframe，切换到编辑器iframe
    console.log('\n步骤5: 查找编辑器...');

    let editorFrame = page;
    for (const iframe of pageInfo.iframes) {
      if (iframe.src.includes('editor') || iframe.src.includes('study')) {
        const frameEl = await page.$(`iframe[src*="${iframe.src.split('?')[0]}"]`);
        if (frameEl) {
          editorFrame = await frameEl.contentFrame();
          console.log(`找到编辑器iframe: ${iframe.src}`);
          break;
        }
      }
    }

    // 6. 输入策略代码
    console.log('\n步骤6: 输入策略代码...');

    const codeResult = await editorFrame.evaluate((strategyCode) => {
      // Monaco
      if (window.monaco && window.monaco.editor) {
        const editors = window.monaco.editor.getEditors();
        if (editors.length > 0) {
          editors[0].setValue(strategyCode);
          return { success: true, method: 'monaco' };
        }
      }

      // CodeMirror
      const cm = document.querySelector('.CodeMirror');
      if (cm && cm.CodeMirror) {
        cm.CodeMirror.setValue(strategyCode);
        return { success: true, method: 'codemirror' };
      }

      // textarea
      const ta = document.querySelector('textarea');
      if (ta) {
        ta.value = strategyCode;
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        return { success: true, method: 'textarea' };
      }

      // 尝试查找contenteditable
      const editable = document.querySelector('[contenteditable="true"]');
      if (editable) {
        editable.textContent = strategyCode;
        return { success: true, method: 'contenteditable' };
      }

      return { success: false };
    }, code);

    console.log('代码输入:', codeResult);

    // 7. 输入策略名称
    console.log('\n步骤7: 输入策略名称...');
    const nameInput = await page.$('input[type="text"]:visible, input[name*="name"]:visible');
    if (nameInput) {
      await nameInput.fill(name);
      console.log(`策略名: ${name}`);
    }

    // 8. 保存
    console.log('\n步骤8: 保存策略...');
    await page.click('button:has-text("保存"), .save-btn');
    await page.waitForTimeout(3000);

    // 9. 运行回测
    console.log('\n步骤9: 运行回测...');

    // 设置回测参数
    const startInput = await page.$('input[name*="start"], input[placeholder*="开始"]');
    if (startInput) await startInput.fill(config.startDate || '2023-01-01');

    const endInput = await page.$('input[name*="end"], input[placeholder*="结束"]');
    if (endInput) await endInput.fill(config.endDate || '2024-12-31');

    // 点击运行
    await page.click('button:has-text("运行"), button:has-text("回测")');
    console.log('已启动回测');

    // 10. 等待结果
    console.log('\n步骤10: 等待回测结果 (30秒)...');
    await page.waitForTimeout(30000);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, `v2-result-${name}-${Date.now()}.png`) });

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    console.log('\n完成！浏览器保持打开30秒...');
    await page.waitForTimeout(30000);

    await browser.close();
    return { success: true };

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `v2-error-${Date.now()}.png`) });
    await browser.close();
    throw error;
  }
}

// CLI
const args = process.argv.slice(2);
const strategyFile = args[0];

if (!strategyFile) {
  console.log('\n用法: node browser/submit-v2.js <策略文件.py>');
  process.exit(1);
}

submitStrategy(strategyFile).catch(console.error);