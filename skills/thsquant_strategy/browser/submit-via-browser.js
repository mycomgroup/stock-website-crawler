#!/usr/bin/env node
/**
 * THSQuant 浏览器策略提交工具
 * 直接通过浏览器界面提交策略并运行回测
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.resolve(__dirname, '../../strategies/thsquant');

async function submitStrategyViaBrowser(strategyFile, config = {}) {
  // 读取策略代码
  const strategyPath = path.resolve(strategyFile);
  if (!fs.existsSync(strategyPath)) {
    throw new Error(`策略文件不存在: ${strategyPath}`);
  }

  const code = fs.readFileSync(strategyPath, 'utf8');
  const name = config.name || path.basename(strategyPath, '.py');

  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 浏览器策略提交');
  console.log('='.repeat(70));
  console.log(`\n策略: ${name}`);
  console.log(`文件: ${strategyPath}`);
  console.log(`代码: ${code.split('\n').length} 行`);

  // 回测配置
  const backtestConfig = {
    startDate: config.startDate || '2023-01-01',
    endDate: config.endDate || '2024-12-31',
    capital: config.capital || '100000',
    benchmark: config.benchmark || '000300.SH',
    frequency: config.frequency || '1d'
  };

  console.log(`\n回测配置:`);
  console.log(`  开始: ${backtestConfig.startDate}`);
  console.log(`  结束: ${backtestConfig.endDate}`);
  console.log(`  资金: ${backtestConfig.capital}`);
  console.log(`  基准: ${backtestConfig.benchmark}`);

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // 1. 打开平台
    console.log('\n步骤1: 打开策略研究页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `step1-strategy-page-${Date.now()}.png`) });

    // 2. 点击新建策略
    console.log('\n步骤2: 点击新建策略...');

    // 尝试多种按钮选择器
    const newBtnSelectors = [
      'button:has-text("新建")',
      'button:has-text("新建策略")',
      'a:has-text("新建")',
      '.btn-new',
      '[class*="new-strategy"]'
    ];

    let clicked = false;
    for (const sel of newBtnSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn) {
          await btn.click();
          clicked = true;
          console.log(`  点击了: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    if (!clicked) {
      // 直接导航到新建页面
      await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/new', {
        waitUntil: 'networkidle'
      });
    }

    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `step2-new-strategy-${Date.now()}.png`) });

    // 3. 输入策略名称
    console.log('\n步骤3: 输入策略名称...');

    const nameInput = await page.$('input[name="name"], input[placeholder*="名称"], input[placeholder*="策略名"]');
    if (nameInput) {
      await nameInput.fill(name);
      console.log(`  策略名: ${name}`);
    } else {
      console.log('  未找到名称输入框，可能已有默认名称');
    }

    await page.waitForTimeout(1000);

    // 4. 输入策略代码
    console.log('\n步骤4: 输入策略代码...');

    // 使用evaluate直接操作编辑器
    const codeResult = await page.evaluate((strategyCode) => {
      // 尝试Monaco编辑器
      if (window.monaco && window.monaco.editor) {
        const editors = window.monaco.editor.getEditors();
        if (editors.length > 0) {
          editors[0].setValue(strategyCode);
          return { success: true, method: 'monaco' };
        }
      }

      // 尝试CodeMirror
      const cmElements = document.querySelectorAll('.CodeMirror');
      if (cmElements.length > 0) {
        const cm = cmElements[0].CodeMirror;
        if (cm) {
          cm.setValue(strategyCode);
          return { success: true, method: 'codemirror' };
        }
      }

      // 尝试普通textarea
      const textarea = document.querySelector('textarea.code-editor, textarea[name="code"]');
      if (textarea) {
        textarea.value = strategyCode;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        return { success: true, method: 'textarea' };
      }

      return { success: false };
    }, code);

    if (codeResult.success) {
      console.log(`  ✓ 代码已输入 (${codeResult.method})`);
    } else {
      console.log('  ⚠ 未找到编辑器，需要手动输入代码');
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `step3-code-entered-${Date.now()}.png`) });

    // 5. 保存策略
    console.log('\n步骤5: 保存策略...');

    const saveSelectors = [
      'button:has-text("保存")',
      'button:has-text("保存策略")',
      '.save-btn',
      '[class*="save"]'
    ];

    for (const sel of saveSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn) {
          await btn.click();
          console.log(`  点击了: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `step4-saved-${Date.now()}.png`) });

    // 6. 设置回测参数
    console.log('\n步骤6: 设置回测参数...');

    // 设置开始日期
    const startInput = await page.$('input[name="start_date"], input[placeholder*="开始"]');
    if (startInput) {
      await startInput.fill(backtestConfig.startDate);
    }

    // 设置结束日期
    const endInput = await page.$('input[name="end_date"], input[placeholder*="结束"]');
    if (endInput) {
      await endInput.fill(backtestConfig.endDate);
    }

    // 设置初始资金
    const capitalInput = await page.$('input[name="capital"], input[placeholder*="资金"]');
    if (capitalInput) {
      await capitalInput.fill(backtestConfig.capital);
    }

    console.log('  参数已设置');
    await page.waitForTimeout(1000);

    // 7. 运行回测
    console.log('\n步骤7: 运行回测...');

    const runSelectors = [
      'button:has-text("运行")',
      'button:has-text("回测")',
      'button:has-text("开始回测")',
      '.run-btn',
      '[class*="run"]'
    ];

    for (const sel of runSelectors) {
      try {
        const btn = await page.$(sel);
        if (btn) {
          await btn.click();
          console.log(`  点击了: ${sel}`);
          break;
        }
      } catch (e) {}
    }

    // 8. 等待回测结果
    console.log('\n步骤8: 等待回测结果 (最多60秒)...');
    await page.waitForTimeout(5000);

    // 截图结果
    const resultPath = path.join(OUTPUT_ROOT, `backtest-result-${name}-${Date.now()}.png`);
    await page.screenshot({ path: resultPath, fullPage: true });
    console.log(`\n结果截图: ${resultPath}`);

    // 等待更多结果
    await page.waitForTimeout(30000);

    // 再次截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `backtest-final-${name}-${Date.now()}.png`) });

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    console.log('\n浏览器保持打开60秒，可以查看结果...');
    await page.waitForTimeout(60000);

    await browser.close();

    return { success: true, name };

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-${Date.now()}.png`) });

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

// 批量提交多个策略
async function batchSubmit(strategyFiles, config = {}) {
  const results = [];

  for (const file of strategyFiles) {
    try {
      const result = await submitStrategyViaBrowser(file, config);
      results.push({ file, ...result });
    } catch (error) {
      results.push({ file, success: false, error: error.message });
    }
  }

  return results;
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const strategyArg = args.find(a => !a.startsWith('--'));

  if (!strategyArg) {
    console.log(`
用法:
  node browser/submit-via-browser.js <策略文件.py> [选项]

选项:
  --name <name>      策略名称 (默认: 文件名)
  --start <date>     开始日期 (默认: 2023-01-01)
  --end <date>       结束日期 (默认: 2024-12-31)
  --capital <num>    初始资金 (默认: 100000)
  --benchmark <id>   基准指数 (默认: 000300.SH)

示例:
  node browser/submit-via-browser.js ../../strategies/thsquant/rfscore7_base_800.py
  node browser/submit-via-browser.js my_strategy.py --name "我的策略" --start 2024-01-01
`);
    process.exit(1);
  }

  const config = {};

  const nameIdx = args.indexOf('--name');
  if (nameIdx !== -1) config.name = args[nameIdx + 1];

  const startIdx = args.indexOf('--start');
  if (startIdx !== -1) config.startDate = args[startIdx + 1];

  const endIdx = args.indexOf('--end');
  if (endIdx !== -1) config.endDate = args[endIdx + 1];

  const capitalIdx = args.indexOf('--capital');
  if (capitalIdx !== -1) config.capital = args[capitalIdx + 1];

  const benchmarkIdx = args.indexOf('--benchmark');
  if (benchmarkIdx !== -1) config.benchmark = args[benchmarkIdx + 1];

  await submitStrategyViaBrowser(strategyArg, config);
}

main().catch(err => {
  console.error('\n错误:', err.message);
  process.exit(1);
});