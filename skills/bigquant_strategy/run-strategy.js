#!/usr/bin/env node
/**
 * BigQuant Strategy Runner
 *
 * 对齐 JoinQuant/RiceQuant 的 CLI 接口。
 *
 * 用法:
 *   node run-strategy.js --strategy examples/simple_backtest.py
 *   node run-strategy.js --strategy examples/ma_strategy.py --start-date 2023-01-01 --end-date 2023-12-31
 *   node run-strategy.js --cell-source "print('hello')"
 *
 * 注意:
 *   BigQuant 不支持通过 API 直接运行任务，创建任务后需要在浏览器中打开 URL 运行。
 */

import './load-env.js';
import { BigQuantTaskClient } from './request/bigquant-task-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

function printUsage() {
  console.log(`
用法:
  node run-strategy.js --strategy <file.py>
  node run-strategy.js --strategy <file.py> --start-date 2023-01-01 --end-date 2023-12-31
  node run-strategy.js --cell-source "print('hello')"

参数:
  --strategy      策略文件路径
  --cell-source   内联代码字符串
  --name          任务名称（可选）
  --start-date    回测开始日期
  --end-date      回测结束日期
  --capital       初始资金
  --benchmark     基准指数
  --task-type     任务类型 (run_once, daily, papertrading)

示例:
  node run-strategy.js --strategy examples/simple_backtest.py
  node run-strategy.js --strategy ../../strategies/bigquant/pure_cash_defense.py
`);
}

async function runStrategy(args) {
  console.log('='.repeat(60));
  console.log('BigQuant Strategy Runner');
  console.log('='.repeat(60));

  // 获取代码
  let code = '';
  let name = 'strategy';

  if (args.strategy) {
    const strategyPath = path.resolve(args.strategy);
    if (!fs.existsSync(strategyPath)) {
      console.error('错误: 策略文件不存在:', strategyPath);
      process.exit(1);
    }
    code = fs.readFileSync(strategyPath, 'utf8');
    name = args.name || path.basename(strategyPath, '.py');
    console.log('策略文件:', strategyPath);
  } else if (args['cell-source']) {
    code = args['cell-source'];
    name = args.name || 'inline_code';
    console.log('内联代码');
  } else {
    console.error('错误: 请指定 --strategy 或 --cell-source');
    printUsage();
    process.exit(1);
  }

  console.log('策略名称:', name);
  console.log('代码长度:', code.length, '字符');

  // 创建客户端
  const client = new BigQuantTaskClient();

  // 检查登录
  console.log('\n[Step 1] 检查登录状态...');
  const loginStatus = await client.checkLogin();
  if (!loginStatus.loggedIn) {
    console.error('错误: 未登录:', loginStatus.error);
    process.exit(1);
  }
  console.log('✓ 已登录:', loginStatus.username);

  // 获取 studio ID
  console.log('\n[Step 2] 获取 Studio ID...');
  const studioId = await client.ensureStudioId();
  console.log('✓ Studio ID:', studioId);

  // 创建并运行策略
  console.log('\n[Step 3] 创建策略任务...');
  const result = await client.runStrategy(name, code, {
    startDate: args['start-date'] || '2023-01-01',
    endDate: args['end-date'] || '2023-12-31',
    capital: parseInt(args.capital) || 100000,
    benchmark: args.benchmark || '000300.XSHG',
    taskType: args['task-type'] || 'run_once'
  });

  console.log('\n' + '='.repeat(60));
  console.log('任务创建成功');
  console.log('='.repeat(60));
  console.log('Task ID:', result.taskId);
  console.log('Taskrun ID:', result.taskrunId || 'N/A');
  console.log('结果文件:', result.outputPath);
  console.log('\nWeb URL:', result.webUrl);
  console.log('\n提示:', result.message);
  console.log('='.repeat(60));

  return result;
}

const args = parseArgs(process.argv.slice(2));

if (args.help || args.h) {
  printUsage();
  process.exit(0);
}

runStrategy(args).catch(console.error);