#!/usr/bin/env node
/**
 * THSQuant 策略提交工具 - 自动填充版本
 * 使用Playwright自动填充编辑器并提交
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
  console.log('THSQuant 策略自动提交');
  console.log('='.repeat(70));
  console.log(`\n策略: ${name}`);
  console.log(`代码: ${code.split('\n').length} 行`);

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // 1. 打开策略研究页面
    console.log('\n步骤1: 打开策略研究页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(3000);

    // 2. 检查登录状态
    console.log('\n步骤2: 检查登录状态...');
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

    // 3. 点击新建策略按钮
    console.log('\n步骤3: 点击新建策略...');
    await page.waitForTimeout(2000);

    // 尝试多种方式点击新建
    const newBtnSelectors = [
      'text=新建',
      'text=新建策略',
      'button:has-text("新建")',
      '.create-btn',
      '[class*="new"]'
    ];

    let clicked = false;
    for (const sel of newBtnSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn) {
          await btn.click();
          clicked = true;
          console.log(`点击: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    if (!clicked) {
      // 直接导航到编辑器
      await page.goto('https://quant.10jqka.com.cn/platform/study/html/editor.html');
      console.log('直接打开编辑器页面');
    }

    await page.waitForTimeout(5000);

    // 4. 查找并填充编辑器
    console.log('\n步骤4: 查找编辑器...');

    // 截图当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `editor-page-${Date.now()}.png`) });

    // 尝试在页面中查找编辑器元素
    const editorInfo = await page.evaluate(() => {
      // 检查是否有Monaco编辑器
      if (window.monaco && window.monaco.editor) {
        const editors = window.monaco.editor.getEditors();
        if (editors.length > 0) {
          return { type: 'monaco', count: editors.length };
        }
      }

      // 检查CodeMirror
      const cm = document.querySelector('.CodeMirror');
      if (cm) {
        return { type: 'codemirror' };
      }

      // 检查textarea
      const ta = document.querySelector('textarea');
      if (ta) {
        return { type: 'textarea' };
      }

      // 检查所有可能的编辑器容器
      const containers = document.querySelectorAll('[class*="editor"], [id*="editor"]');
      return { type: 'unknown', containers: containers.length };
    });

    console.log('编辑器信息:', editorInfo);

    // 5. 使用键盘输入方式填充代码
    console.log('\n步骤5: 填充策略代码...');

    // 先复制代码到剪贴板
    await page.evaluate((c) => {
      navigator.clipboard.writeText(c);
    }, code);

    console.log('代码已复制到剪贴板');

    // 尝试聚焦编辑器并粘贴
    // 点击页面中心区域尝试聚焦编辑器
    await page.click('body', { position: { x: 700, y: 400 } });
    await page.waitForTimeout(500);

    // 使用Ctrl+A全选 + Ctrl+V粘贴
    await page.keyboard.press('Control+a');
    await page.waitForTimeout(300);
    await page.keyboard.press('Control+v');
    await page.waitForTimeout(2000);

    // 截图填充结果
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `after-paste-${Date.now()}.png`) });

    // 6. 输入策略名称
    console.log('\n步骤6: 输入策略名称...');

    // 尝试点击名称输入框
    const nameSelectors = [
      'input[type="text"]',
      'input[placeholder*="名称"]',
      'input[placeholder*="策略"]',
      '[class*="name"] input'
    ];

    for (const sel of nameSelectors) {
      try {
        const input = await page.$(sel);
        if (input && await input.isVisible()) {
          await input.click();
          await input.fill(name);
          console.log(`名称输入: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    // 7. 点击保存
    console.log('\n步骤7: 保存策略...');
    await page.waitForTimeout(1000);

    const saveSelectors = [
      'text=保存',
      'button:has-text("保存")',
      '[class*="save"]'
    ];

    for (const sel of saveSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn && await btn.isVisible()) {
          await btn.click();
          console.log(`点击: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    await page.waitForTimeout(3000);

    // 8. 设置回测参数并运行
    console.log('\n步骤8: 设置回测参数...');

    // 设置日期
    const startInput = await page.$('input[placeholder*="开始"], input[name*="start"]');
    if (startInput) {
      await startInput.fill(config.startDate || '2023-01-01');
    }

    const endInput = await page.$('input[placeholder*="结束"], input[name*="end"]');
    if (endInput) {
      await endInput.fill(config.endDate || '2024-12-31');
    }

    // 9. 点击运行回测
    console.log('\n步骤9: 运行回测...');

    const runSelectors = [
      'text=运行',
      'text=回测',
      'button:has-text("运行")',
      '[class*="run"]'
    ];

    for (const sel of runSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn && await btn.isVisible()) {
          await btn.click();
          console.log(`点击: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    // 10. 等待结果
    console.log('\n步骤10: 等待回测结果...');
    await page.waitForTimeout(10000);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, `result-${name}-${Date.now()}.png`) });

    console.log('\n浏览器保持打开30秒，请检查回测结果...');
    await page.waitForTimeout(30000);

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    await browser.close();
    return { success: true, name };

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-${Date.now()}.png`) });
    await browser.close();
    throw error;
  }
}

// CLI
const args = process.argv.slice(2);
const strategyFile = args.find(a => !a.startsWith('--'));

if (!strategyFile) {
  console.log('\n用法: node browser/auto-submit.js <策略文件.py> [--name 策略名] [--start 日期] [--end 日期]');
  process.exit(1);
}

const config = {};
const nameIdx = args.indexOf('--name');
if (nameIdx !== -1) config.name = args[nameIdx + 1];

const startIdx = args.indexOf('--start');
if (startIdx !== -1) config.startDate = args[startIdx + 1];

const endIdx = args.indexOf('--end');
if (endIdx !== -1) config.endDate = args[endIdx + 1];

submitStrategy(strategyFile, config).catch(console.error);