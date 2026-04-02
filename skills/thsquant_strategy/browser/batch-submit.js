#!/usr/bin/env node
/**
 * THSQuant 策略批量提交工具
 * 打开浏览器让用户手动完成策略提交
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.resolve(__dirname, '../../strategies/thsquant');

// 要提交的策略列表
const STRATEGIES = [
  { file: 'pure_cash_defense.py', name: '纯现金防守策略' },
  { file: 'smallcap_quality_defense.py', name: '小市值质量防御策略' },
  { file: 'rfscore7_base_800.py', name: 'RF评分策略' }
];

async function batchSubmit() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 策略批量提交工具');
  console.log('='.repeat(70));

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  console.log('\n待提交策略:');
  STRATEGIES.forEach((s, i) => {
    const filePath = path.join(STRATEGIES_DIR, s.file);
    const exists = fs.existsSync(filePath);
    const code = exists ? fs.readFileSync(filePath, 'utf8') : '';
    console.log(`  ${i + 1}. ${s.name} (${code.split('\n').length} 行) ${exists ? '✓' : '✗'}`);
  });

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 打开策略研究页面
  await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
    waitUntil: 'domcontentloaded'
  });
  await page.waitForTimeout(3000);

  console.log('\n' + '='.repeat(70));
  console.log('操作指引');
  console.log('='.repeat(70));
  console.log('\n对于每个策略，请执行以下步骤:');
  console.log('  1. 点击"新建策略"');
  console.log('  2. 输入策略名称');
  console.log('  3. 复制并粘贴策略代码');
  console.log('  4. 点击"保存"');
  console.log('  5. 设置回测参数 (2023-01-01 到 2024-12-31)');
  console.log('  6. 点击"运行回测"');
  console.log('\n' + '='.repeat(70));

  // 打印每个策略的代码
  for (const s of STRATEGIES) {
    const filePath = path.join(STRATEGIES_DIR, s.file);
    if (fs.existsSync(filePath)) {
      const code = fs.readFileSync(filePath, 'utf8');
      console.log('\n' + '-'.repeat(70));
      console.log(`策略: ${s.name}`);
      console.log(`文件: ${s.file}`);
      console.log('-'.repeat(70));
      console.log('\n代码 (复制以下内容):');
      console.log('\n' + code + '\n');
    }
  }

  console.log('='.repeat(70));
  console.log('\n浏览器保持打开，请在浏览器中完成策略提交。');
  console.log('完成后可以关闭浏览器。');
  console.log('\n提示: 代码已打印在上方，可以直接复制粘贴。');

  // 保持浏览器打开
  await new Promise(() => {});
}

batchSubmit().catch(console.error);