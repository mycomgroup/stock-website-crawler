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

// 增强的重试函数
async function retryWithBackoff(fn, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 2000,
    maxDelay = 30000,
    retryOn = ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND', '504', '502', '503']
  } = options;
  
  let lastError;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      const errorMsg = error.message || String(error);
      
      // 检查是否应该重试
      const shouldRetry = retryOn.some(pattern => errorMsg.includes(pattern));
      
      if (!shouldRetry || attempt === maxRetries - 1) {
        throw error;
      }
      
      // 计算延迟时间（指数退避）
      const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
      
      console.log(`   ⚠️  Attempt ${attempt + 1}/${maxRetries} failed: ${errorMsg.slice(0, 100)}`);
      console.log(`   ⏳  Retrying in ${delay/1000}s...`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
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
  console.log('RiceQuant Backtest Runner (Enhanced with Retry)');
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
    // 1. 确保会话有效
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
    const loginStatus = await retryWithBackoff(
      () => client.checkLogin(),
      { maxRetries: 3, baseDelay: 2000 }
    );
    
    if (loginStatus.code !== 0) {
      console.error('Error: Session invalid after verification');
      return null;
    }
    console.log('   Logged in as:', loginStatus.fullname || loginStatus.phone);
    
    // 3. 获取策略上下文
    console.log('\n3. Getting strategy context...');
    const context = await retryWithBackoff(
      () => client.getStrategyContext(id),
      { maxRetries: 3, baseDelay: 2000 }
    );
    console.log('   Strategy name:', context.name || 'N/A');
    console.log('   Workspace ID:', context.workspaceId);
    
    // 4. 保存策略代码
    console.log('\n4. Saving strategy code...');
    const saveResult = await retryWithBackoff(
      () => client.saveStrategy(id, context.name || 'Strategy', code, context),
      { maxRetries: 3, baseDelay: 2000 }
    );
    console.log('   Save result:', saveResult?.message || JSON.stringify(saveResult).substring(0, 100) || 'OK');
    
    // 5. 运行回测（带重试）
    console.log('\n5. Starting backtest...');
    let backtestResult;
    
    try {
      backtestResult = await retryWithBackoff(
        () => client.runBacktest(id, code, {
          startTime: start || '2021-01-01',
          endTime: end || '2025-03-28',
          baseCapital: capital || '100000',
          frequency: freq || 'day',
          benchmark: benchmark || '000300.XSHG'
        }, context),
        { 
          maxRetries: 5, 
          baseDelay: 5000,
          maxDelay: 60000,
          retryOn: ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND', '504', '502', '503', 'Gateway Time-out', 'network']
        }
      );
    } catch (error) {
      console.log('\n   ✗ Backtest start failed after retries:', error.message);
      console.log('   💡 Tip: RiceQuant server may be busy. Try again later or use a shorter time range.');
      return null;
    }
    
    console.log('   Backtest result:', JSON.stringify(backtestResult).substring(0, 200));
    
    // 提取回测 ID
    let backtestId = backtestResult.backtestId || backtestResult._id || backtestResult.id;
    if (typeof backtestId === 'string') {
      backtestId = backtestId.replace(/"/g, '');
    }
    
    if (backtestId) {
      console.log('\n   ✓ Backtest started! ID:', backtestId);
      
      // 6. 等待回测完成（增加等待时间）
      console.log('\n6. Waiting for backtest to complete...');
      let attempts = 0;
      let result = null;
      const maxAttempts = 120; // 增加到120次
      const pollInterval = 5000; // 增加到5秒
      
      while (attempts < maxAttempts) {
        await new Promise(r => setTimeout(r, pollInterval));
        attempts++;
        
        try {
          result = await retryWithBackoff(
            () => client.getBacktestResult(backtestId),
            { maxRetries: 2, baseDelay: 2000 }
          );
          
          if (!result) {
            process.stdout.write(`   [${attempts}/${maxAttempts}] Waiting for result...\r`);
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
          process.stdout.write(`   [${attempts}/${maxAttempts}] Progress: ${progress}%\r`);
        } catch (e) {
          const errorMsg = e.message || String(e);
          if (errorMsg.includes('network') || errorMsg.includes('ECONN') || errorMsg.includes('timeout')) {
            process.stdout.write(`   [${attempts}/${maxAttempts}] Network error, retrying...\r`);
          } else {
            console.log('\n   ✗ Error:', errorMsg.slice(0, 200));
          }
        }
      }
      
      if (attempts >= maxAttempts) {
        console.log('\n   ⚠️  Timeout waiting for backtest to complete');
        console.log('   💡 Check backtest status manually at: https://www.ricequant.com/quant/backtest/' + backtestId);
      }
      
      // 7. 获取完整报告
      if (result) {
        console.log('\n7. Generating full report...');
        
        try {
          const report = await retryWithBackoff(
            () => client.getFullReport(backtestId),
            { maxRetries: 3, baseDelay: 3000 }
          );
          const reportPath = client.writeArtifact(`ricequant-backtest-${backtestId}`, report);
          console.log('   Report saved:', reportPath);
        } catch (error) {
          console.log('   ⚠️  Failed to get full report:', error.message);
        }
        
        // 打印摘要
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
    console.error('\n✗ Error:', e.message);
    if (e.message && e.message.includes('504')) {
      console.error('\n💡 Tip: RiceQuant server timed out (504 Gateway Timeout)');
      console.error('   This usually means the server is busy. Try:');
      console.error('   - Using a shorter backtest period');
      console.error('   - Waiting a few minutes and retrying');
      console.error('   - Using JoinQuant Notebook instead (no time limit)');
    }
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
  benchmark: args.benchmark
});