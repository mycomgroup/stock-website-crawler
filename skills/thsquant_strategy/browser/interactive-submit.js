#!/usr/bin/env node
/**
 * THSQuant 策略提交助手
 * 交互式方式帮助用户快速提交策略
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import readline from 'node:readline';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.resolve(__dirname, '../../strategies/thsquant');

async function submitInteractive(strategyFile, config = {}) {
  const strategyPath = path.resolve(strategyFile);
  if (!fs.existsSync(strategyPath)) {
    console.log(`\n✗ 文件不存在: ${strategyPath}`);
    return { success: false };
  }

  const code = fs.readFileSync(strategyPath, 'utf8');
  const name = config.name || path.basename(strategyPath, '.py');

  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 策略提交助手');
  console.log('='.repeat(70));
  console.log(`\n策略名称: ${name}`);
  console.log(`文件: ${strategyPath}`);
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
    // 1. 打开策略编辑器
    console.log('\n步骤1: 打开策略编辑器...');
    await page.goto('https://quant.10jqka.com.cn/platform/study/html/editor.html', {
      waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(3000);

    // 2. 复制代码到剪贴板
    console.log('\n步骤2: 复制代码到剪贴板...');
    await page.evaluate((c) => {
      navigator.clipboard.writeText(c);
    }, code);

    // 3. 显示用户指引
    console.log('\n' + '='.repeat(70));
    console.log('请在浏览器中完成以下操作:');
    console.log('='.repeat(70));
    console.log('\n  1. 输入策略名称: ' + name);
    console.log('  2. 在编辑器中按 Ctrl+V 粘贴代码');
    console.log('  3. 设置回测参数:');
    console.log(`     - 开始日期: ${config.startDate || '2023-01-01'}`);
    console.log(`     - 结束日期: ${config.endDate || '2024-12-31'}`);
    console.log('  4. 点击"保存"按钮');
    console.log('  5. 点击"运行回测"按钮');
    console.log('\n代码已复制到剪贴板，直接粘贴即可！');
    console.log('='.repeat(70));

    // 4. 等待用户操作
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    await new Promise(resolve => {
      rl.question('\n完成后按回车键继续...', () => {
        rl.close();
        resolve();
      });
    });

    // 5. 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    // 6. 截图结果
    const resultPath = path.join(OUTPUT_ROOT, `result-${name}-${Date.now()}.png`);
    await page.screenshot({ path: resultPath, fullPage: true });
    console.log(`\n截图保存: ${resultPath}`);

    console.log('\n✓ 提交完成！');
    console.log('浏览器将保持打开，您可以查看回测结果。');

    // 保持浏览器打开
    await new Promise(() => {});

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `error-${Date.now()}.png`) });
  }
}

// CLI
const args = process.argv.slice(2);
const strategyFile = args.find(a => !a.startsWith('--'));

if (!strategyFile) {
  console.log('\n用法: node browser/interactive-submit.js <策略文件.py> [--name 名称] [--start 日期] [--end 日期]');
  console.log('\n可用策略:');
  const strategies = fs.readdirSync(STRATEGIES_DIR)
    .filter(f => f.endsWith('.py') && !f.includes('test'));
  strategies.forEach(s => console.log(`  - ${s}`));
  process.exit(1);
}

const config = {};
const nameIdx = args.indexOf('--name');
if (nameIdx !== -1) config.name = args[nameIdx + 1];

const startIdx = args.indexOf('--start');
if (startIdx !== -1) config.startDate = args[startIdx + 1];

const endIdx = args.indexOf('--end');
if (endIdx !== -1) config.endDate = args[endIdx + 1];

submitInteractive(strategyFile, config).catch(console.error);