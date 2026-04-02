#!/usr/bin/env node
/**
 * THSQuant 完整工具集
 * 整合登录、策略列表、提交等功能
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import './load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from './paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.resolve(__dirname, '../../strategies/thsquant');

// 打印帮助
function printHelp() {
  console.log(`
${'='.repeat(70)}
THSQuant 完整工具集
${'='.repeat(70)}

命令:
  check          检查登录状态
  login          打开浏览器进行登录
  list           列出所有策略
  simu           列出模拟交易
  submit <file>  提交策略并运行回测 (通过浏览器)
  api-list       通过API列出策略
  help           显示此帮助

示例:
  node run.js check
  node run.js login
  node run.js list
  node run.js submit ../../strategies/thsquant/rfscore7_base_800.py

配置:
  账号: mx_kj1ku00qp
  密码: f09173228552

文件位置:
  Session: data/session.json
  截图: data/*.png
  API结果: data/api-*.json
`);
}

// 检查登录
async function checkLogin() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  try {
    const resp = await fetch('https://quant.10jqka.com.cn/platform/user/getauthdata', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookieHeader
      },
      body: 'isajax=1'
    });
    const data = await resp.json();

    if (data.errorcode === 0) {
      console.log('\n✓ 已登录');
      console.log(`  用户ID: ${data.result?.user_id}`);
      console.log(`  VIP: ${data.result?.vip ? '是' : '否'}`);
      return true;
    } else {
      console.log('\n✗ 未登录');
      console.log('  运行: node run.js login');
      return false;
    }
  } catch (e) {
    console.log('\n✗ Session无效');
    return false;
  }
}

// 列出策略 (通过API)
async function listStrategies() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  console.log('\n获取策略列表...\n');

  const resp = await fetch('https://quant.10jqka.com.cn/platform/algorithms/queryall2/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': cookieHeader
    },
    body: 'isajax=1&datatype=jsonp'
  });

  const text = await resp.text();
  const match = text.match(/\((.+)\)/s);

  if (match) {
    const data = JSON.parse(match[1]);
    const strategies = data.result?.strategys || [];

    if (strategies.length === 0) {
      console.log('没有策略');
    } else {
      console.log(`共 ${strategies.length} 个策略:\n`);
      strategies.forEach((s, i) => {
        console.log(`${(i + 1).toString().padStart(2)}. ${s.algo_name}`);
        console.log(`     ID: ${s.algo_id}`);
        console.log(`     回测: ${s.backtest_number} 次, 修改: ${s.modified}`);
        console.log();
      });
    }
  }
}

// 列出模拟交易
async function listSimu() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  console.log('\n获取模拟交易...\n');

  const resp = await fetch('https://quant.10jqka.com.cn/platform/simupaper/queryall/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': cookieHeader
    },
    body: 'isajax=1'
  });

  const data = await resp.json();

  if (data.errorcode === 0 && data.result) {
    const simus = Array.isArray(data.result) ? data.result : [data.result];

    console.log(`共 ${simus.length} 个模拟交易:\n`);

    simus.forEach((s, i) => {
      console.log(`${i + 1}. ${s.name}`);
      console.log(`   收益率: ${(s.annual_yield * 100).toFixed(2)}%`);
      console.log(`   最大回撤: ${(s.max_drawdown * 100).toFixed(2)}%`);
      console.log(`   状态: ${s.status}`);
      console.log();
    });
  }
}

// 提交策略 (通过浏览器)
async function submitStrategy(strategyFile) {
  const { chromium } = await import('playwright');

  const strategyPath = path.resolve(strategyFile);
  if (!fs.existsSync(strategyPath)) {
    console.log(`\n✗ 文件不存在: ${strategyPath}`);
    return;
  }

  const code = fs.readFileSync(strategyPath, 'utf8');
  const name = path.basename(strategyPath, '.py');

  console.log(`\n策略: ${name}`);
  console.log(`代码: ${code.split('\n').length} 行`);

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
    console.log('\n打开策略编辑器...');
    await page.goto('https://quant.10jqka.com.cn/platform/study/html/editor.html', {
      waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(5000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, `editor-${Date.now()}.png`) });

    console.log('\n请在浏览器中:');
    console.log('  1. 输入策略名称');
    console.log('  2. 粘贴策略代码');
    console.log('  3. 设置回测参数');
    console.log('  4. 点击运行回测');
    console.log('\n代码已复制到剪贴板（请在浏览器中粘贴）');

    // 复制代码到剪贴板
    await page.evaluate((c) => {
      navigator.clipboard.writeText(c);
    }, code);

    console.log('\n浏览器保持打开，完成后手动关闭...');

    // 保持浏览器打开直到用户关闭
    await new Promise(() => {});

  } catch (error) {
    console.error('\n错误:', error.message);
    await browser.close();
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'check':
      await checkLogin();
      break;

    case 'login':
      console.log('\n启动登录...');
      console.log('运行: node browser/auto-login-v6.js');
      break;

    case 'list':
    case 'api-list':
      await listStrategies();
      break;

    case 'simu':
      await listSimu();
      break;

    case 'submit':
      if (!args[1]) {
        console.log('\n用法: node run.js submit <策略文件.py>');

        // 显示可用策略
        console.log('\n可用策略:');
        const strategies = fs.readdirSync(STRATEGIES_DIR)
          .filter(f => f.endsWith('.py') && !f.includes('test'));
        strategies.forEach((s, i) => console.log(`  ${i + 1}. ${s}`));
      } else {
        await submitStrategy(args[1]);
      }
      break;

    case 'help':
    default:
      printHelp();
  }
}

main().catch(console.error);