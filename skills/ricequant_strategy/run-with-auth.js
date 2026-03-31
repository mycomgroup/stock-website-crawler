import { RiceQuantClient } from './request/ricequant-client.js';
import { RiceQuantAuth } from './auto-login.js';
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

async function ensureAuth() {
  const client = new RiceQuantClient();
  
  // 检查当前状态
  console.log('Checking authentication status...');
  const status = await client.checkLogin();
  
  if (status.code === 0) {
    console.log('✓ Already authenticated\n');
    return true;
  }
  
  console.log('✗ Not authenticated, running auto-login...\n');
  
  // 运行自动登录
  const auth = new RiceQuantAuth();
  return await auth.run();
}

async function runBacktest(options) {
  const { strategyId, codeFilePath, startTime, endTime, baseCapital, frequency, benchmark } = options;
  
  if (!strategyId || !codeFilePath) {
    console.error('Error: --id and --file are required');
    process.exit(1);
  }
  
  if (!fs.existsSync(codeFilePath)) {
    console.error('Error: File not found:', codeFilePath);
    process.exit(1);
  }
  
  const code = fs.readFileSync(codeFilePath, 'utf8');
  
  console.log('Strategy file:', codeFilePath);
  console.log('Strategy ID:', strategyId);
  console.log('Start date:', startTime || '2021-01-01');
  console.log('End date:', endTime || '2025-03-28');
  console.log('Initial capital:', baseCapital || '100000');
  console.log('');
  
  // 确保已登录
  const authSuccess = await ensureAuth();
  
  if (!authSuccess) {
    console.error('Authentication failed. Cannot run backtest.');
    process.exit(1);
  }
  
  // 创建客户端
  const client = new RiceQuantClient();
  
  try {
    // 获取策略上下文
    console.log('\nFetching strategy context...');
    const context = await client.getStrategyContext(strategyId);
    console.log('Strategy name:', context.name);
    
    // 保存策略代码
    console.log('\nSaving strategy code...');
    const saveResult = await client.saveStrategy(strategyId, context.name || 'Strategy', code, context);
    console.log('Save result:', JSON.stringify(saveResult));
    
    // 运行回测
    console.log('\nStarting backtest...');
    const backtestResult = await client.runBacktest(strategyId, code, {
      startTime: startTime || '2021-01-01',
      endTime: endTime || '2025-03-28',
      baseCapital: baseCapital || '100000',
      frequency: frequency || 'day',
      benchmark: benchmark || '000300.XSHG'
    }, context);
    
    console.log('\nBacktest result:');
    console.log(JSON.stringify(backtestResult, null, 2));
    
    if (backtestResult.backtestId || backtestResult.data?.backtestId) {
      const backtestId = backtestResult.backtestId || backtestResult.data.backtestId;
      console.log('\n✓ Backtest started! ID:', backtestId);
      
      // 等待回测完成
      console.log('\nWaiting for backtest to complete...');
      let attempts = 0;
      let result = null;
      
      while (attempts < 60) {
        await new Promise(r => setTimeout(r, 5000));
        attempts++;
        
        try {
          result = await client.getBacktestResult(backtestId);
          
          if (!result) {
            process.stdout.write(`[${attempts}] Waiting for result...\r`);
            continue;
          }
          
          if (result.status === 'finished' || result.progress === 100) {
            console.log('\n✓ Backtest completed!');
            break;
          }
          
          if (result.status === 'error_exit' || result.status === 'failed') {
            console.log('\n✗ Backtest failed:', result.exception || result.message || 'Unknown error');
            break;
          }
          
          process.stdout.write(`[${attempts}] Progress: ${result.progress || 0}%\r`);
        } catch (e) {
          if (e.message && (e.message.includes('network') || e.message.includes('ECONN') || e.message.includes('timeout'))) {
            process.stdout.write(`[${attempts}] Network error, retrying...\r`);
          } else {
            console.log('\nPoll error:', e.message);
          }
        }
      }
      
      // 获取完整报告
      if (result) {
        const reportPath = client.writeArtifact(`ricequant-backtest-${backtestId}`, result);
        console.log('\nFull report saved to:', reportPath);
        
        // 打印摘要
        if (result.summary || result.risk) {
          console.log('\n=== Backtest Summary ===');
          const summary = result.summary || {};
          const risk = result.risk || {};
          
          console.log('Total Return:', (summary.totalReturn || risk.total_return || 0) * 100, '%');
          console.log('Annual Return:', (summary.annualReturn || risk.annual_return || 0) * 100, '%');
          console.log('Max Drawdown:', (summary.maxDrawdown || risk.max_drawdown || 0) * 100, '%');
          console.log('Sharpe Ratio:', summary.sharpe || risk.sharpe || 'N/A');
        }
      }
      
      return backtestId;
    } else {
      console.log('\n✗ Failed to start backtest');
      return null;
    }
    
  } catch (e) {
    console.error('\nError:', e.message);
    console.error(e.stack);
    return null;
  }
}

// 主函数
async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  if (args.help) {
    console.log(`
Usage: node run-with-auth.js [options]

Options:
  --id <strategyId>     Strategy ID (required)
  --file <path>         Strategy code file path (required)
  --start <date>        Start date (default: 2021-01-01)
  --end <date>          End date (default: 2025-03-28)
  --capital <num>       Initial capital (default: 100000)
  --freq <frequency>    day or minute (default: day)
  --benchmark <code>    Benchmark index (default: 000300.XSHG)

Examples:
  # Run original strategy
  node run-with-auth.js --id abc123 --file ../strategies/Ricequant/rfscore7_pb10_final_v2.py

  # Run enhanced strategy
  node run-with-auth.js --id abc123 --file ../strategies/Ricequant/rfscore7_pb10_enhanced.py

  # With custom date range
  node run-with-auth.js --id abc123 --file strategy.py --start 2023-01-01 --end 2024-12-31
`);
    process.exit(0);
  }
  
  // 如果只运行登录
  if (args.login) {
    const auth = new RiceQuantAuth();
    const success = await auth.run();
    process.exit(success ? 0 : 1);
  }
  
  // 运行回测
  await runBacktest({
    strategyId: args.id,
    codeFilePath: args.file,
    startTime: args.start,
    endTime: args.end,
    baseCapital: args.capital,
    frequency: args.freq,
    benchmark: args.benchmark
  });
}

main();