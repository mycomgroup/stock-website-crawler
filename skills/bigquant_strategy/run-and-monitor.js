#!/usr/bin/env node
/**
 * BigQuant 任务状态监控
 *
 * 虽然无法直接获取运行输出，但可以：
 * 1. 创建任务
 * 2. 监控任务状态变化
 * 3. 返回 Web URL 供用户查看结果
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

async function runAndMonitor(args) {
  console.log('='.repeat(60));
  console.log('BigQuant Strategy Runner (with monitoring)');
  console.log('='.repeat(60));

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
  } else {
    console.error('错误: 请指定 --strategy');
    process.exit(1);
  }

  const client = new BigQuantTaskClient();

  // 创建任务
  console.log('\n[Step 1] 创建任务...');
  const result = await client.runStrategy(name, code, {
    startDate: args['start-date'] || '2023-01-01',
    endDate: args['end-date'] || '2023-12-31',
    capital: parseInt(args.capital) || 100000
  });

  console.log('Task ID:', result.taskId);
  console.log('Web URL:', result.webUrl);

  // 监控状态
  console.log('\n[Step 2] 监控任务状态...');

  let lastState = null;
  const maxWait = parseInt(args.timeout) || 300000; // 5分钟
  const startTime = Date.now();

  while (Date.now() - startTime < maxWait) {
    const task = await client.getTask(result.taskId);
    const currentState = task.data?.last_run?.state || 'none';

    if (currentState !== lastState) {
      const timestamp = new Date().toLocaleTimeString();
      console.log(`[${timestamp}] 状态: ${currentState}`);
      lastState = currentState;
    }

    // 检查完成状态
    if (currentState === 'success') {
      console.log('\n✓ 任务执行成功！');
      break;
    }

    if (currentState === 'failed') {
      console.log('\n✗ 任务执行失败');
      break;
    }

    // 等待后继续检查
    await new Promise(r => setTimeout(r, 5000));
  }

  console.log('\n' + '='.repeat(60));
  console.log('结果查看');
  console.log('='.repeat(60));
  console.log('\n请在浏览器中打开以下 URL 查看详细结果：');
  console.log(result.webUrl);
  console.log('\n注意: BigQuant 任务可能需要手动在 Web 界面点击运行。');
  console.log('='.repeat(60));

  return result;
}

const args = parseArgs(process.argv.slice(2));
runAndMonitor(args).catch(console.error);