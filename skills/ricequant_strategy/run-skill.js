#!/usr/bin/env node
import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
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

async function runBacktest(options) {
  const { id, file, start, end, capital, freq, benchmark } = options;
  
  if (!id || !file) {
    console.error('Error: --id and --file are required');
    console.log('\nUsage: node run-skill.js --id <strategyId> --file <path> [options]');
    console.log('\nOptions:');
    console.log('  --start <date>    Start date (default: 2021-01-01)');
    console.log('  --end <date>      End date (default: 2025-03-28)');
    console.log('  --capital <num>   Initial capital (default: 100000)');
    console.log('  --freq <string>   day or minute (default: day)');
    console.log('  --benchmark <id>  Benchmark index (default: 000300.XSHG)');
    return null;
  }
  
  if (!fs.existsSync(file)) {
    console.error('Error: File not found:', file);
    return null;
  }
  
  const code = fs.readFileSync(file, 'utf8');
  
  console.log('='.repeat(60));
  console.log('RiceQuant Backtest Runner');
  console.log('='.repeat(60));
  console.log('Strategy ID:', id);
  console.log('Strategy File:', file);
  console.log('Start Date:', start || '2021-01-01');
  console.log('End Date:', end || '2025-03-28');
  console.log('Initial Capital:', capital || '100000');
  console.log('Frequency:', freq || 'day');
  console.log('Benchmark:', benchmark || '000300.XSHG');
  console.log('='.repeat(60) + '\n');
  
  try {
    // 1. 确保会话有效（纯 HTTP 验证，只在过期时启动浏览器）
    console.log('1. Verifying session...');
    const credentials = {
      username: process.env.RICEQUANT_USERNAME,
      password: process.env.RICEQUANT_PASSWORD
    };
    const cookies = await ensureRiceQuantSession(credentials);
    console.log('   Session OK (' + cookies.length + ' cookies)');
    
    const client = new RiceQuantClient({ cookies });
    
    // 2. HTTP 验证登录状态
    console.log('\n2. Checking login status...');
    const loginStatus = await client.checkLogin();
    
    if (loginStatus.code !== 0) {
      console.error('Error: Session invalid after verification');
      return null;
    }
    console.log('   Logged in as:', loginStatus.fullname || loginStatus.phone);
    
    // 3. 获取策略上下文
    console.log('\n3. Getting strategy context...');
    const context = await client.getStrategyContext(id);
    console.log('   Strategy name:', context.name || 'N/A');
    console.log('   Workspace ID:', context.workspaceId);
    
    // 4. 保存策略代码
    console.log('\n4. Saving strategy code...');
    const saveResult = await client.saveStrategy(id, context.name || 'Strategy', code, context);
    console.log('   Save result:', saveResult?.message || JSON.stringify(saveResult).substring(0, 100) || 'OK');
    
    // 5. 准备运行回测
    // 如果指定了 wait-if-full，检查运行中的回测数量
    if (options.waitIfFull) {
      const maxRunning = parseInt(options.maxRunning || '3', 10);
      console.log(`\n5. Checking capacity (Max: ${maxRunning})...`);
      let runningCount = await client.getRunningBacktestCount();
      
      while (runningCount >= maxRunning) {
        process.stdout.write(`   Capacity full (${runningCount}/${maxRunning}). Waiting 10s...\r`);
        await new Promise(resolve => setTimeout(resolve, 10000));
        runningCount = await client.getRunningBacktestCount();
      }
      console.log(`   Capacity available (${runningCount}/${maxRunning}). Proceeding.`);
    }

    console.log('\n6. Starting backtest...');
    const backtestResult = await client.runBacktest(id, code, {
      startTime: start || '2021-01-01',
      endTime: end || '2025-03-28',
      baseCapital: capital || '100000',
      frequency: freq || 'day',
      benchmark: benchmark || '000300.XSHG'
    }, context);
    
    console.log('   Backtest result:', JSON.stringify(backtestResult).substring(0, 200));
    
    // 提取回测 ID（可能是字符串或对象）
    let backtestId = backtestResult.backtestId || backtestResult._id || backtestResult.id;
    if (typeof backtestId === 'string') {
      backtestId = backtestId.replace(/"/g, '');  // 移除引号
    }
    
    if (backtestId) {
      console.log(`\n   ✓ Backtest started! ID: ${backtestId}`);
      
      if (options.noWait) {
        console.log('   --no-wait specified, skipping result polling.');
        return backtestId;
      }
      
      // 6. 等待回测完成
      console.log('\n6. Waiting for backtest to complete...');
      let attempts = 0;
      let result = null;
      
      while (attempts < 60) {
        await new Promise(r => setTimeout(r, 3000));
        attempts++;
        
        try {
          result = await client.getBacktestResult(backtestId);
          
          if (!result) {
            process.stdout.write(`   [${attempts}/60] Waiting for result...\r`);
            continue;
          }
          
          if (result.status === 'finished' || result.progress === 100) {
            console.log('\n   ✓ Backtest completed!');
            break;
          }
          
          if (result.status === 'error_exit' || result.status === 'failed') {
            console.log('\n   ✗ Backtest failed:', result.exception || result.message || 'Unknown error');
            break;
          }
          
          const progress = result.progress || 0;
          process.stdout.write(`   [${attempts}/60] Progress: ${progress}%\r`);
        } catch (e) {
          if (e.message && (e.message.includes('network') || e.message.includes('ECONN') || e.message.includes('timeout'))) {
            process.stdout.write(`   [${attempts}/60] Network error, retrying...\r`);
          } else {
            console.log('\n   ✗ Error:', e.message);
          }
        }
      }
      
      // 7. 获取完整报告
      if (result) {
        console.log('\n7. Generating full report...');
        const report = await client.getFullReport(backtestId);
        const reportPath = client.writeArtifact(`ricequant-backtest-${backtestId}`, report);
        console.log('   Report saved:', reportPath);
        
        // 7. 打印摘要
        console.log('\n' + '='.repeat(60));
        console.log('Backtest Summary');
        console.log('='.repeat(60));
        
        if (result.summary || result.risk) {
          const summary = result.summary || {};
          const risk = result.risk || {};
          
          console.log('Total Return:', ((risk.total_returns || summary.totalReturn || 0) * 100).toFixed(2), '%');
          console.log('Annual Return:', ((risk.annual_returns || summary.annualReturn || 0) * 100).toFixed(2), '%');
          console.log('Max Drawdown:', ((risk.max_drawdown || summary.maxDrawdown || 0) * 100).toFixed(2), '%');
          console.log('Sharpe Ratio:', risk.sharpe || summary.sharpe || 'N/A');
          console.log('Win Rate:', ((risk.win_rate || summary.winRate || 0) * 100).toFixed(1), '%');
        }
        
        console.log('='.repeat(60));
      }
      
      return backtestId;
    } else {
      console.log('\n   ✗ Failed to start backtest');
      console.log('   Response:', JSON.stringify(backtestResult));
      return null;
    }
    
  } catch (e) {
    console.error('\nError:', e.message);
    console.error(e.stack);
    return null;
  }
}

// 主函数
const args = parseArgs(process.argv.slice(2));
runBacktest({
  id: args.id,
  file: args.file,
  start: args.start,
  end: args.end,
  capital: args.capital,
  freq: args.freq,
  benchmark: args.benchmark,
  noWait: args['no-wait'] === true,
  waitIfFull: args['wait-if-full'] === true,
  maxRunning: args['max-running']
});