import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = path.join(__dirname, 'data');

async function runBacktest(codeFile, startDate, endDate, capital) {
  const code = fs.readFileSync(codeFile, 'utf8');
  const strategyName = path.basename(codeFile, '.py');
  
  console.log('\n' + '='.repeat(60));
  console.log('RiceQuant Backtest - Create, Run, Delete');
  console.log('='.repeat(60));
  console.log('Strategy:', strategyName);
  console.log('Period:', startDate, '-', endDate);
  console.log('Capital:', capital);
  console.log('Code length:', code.length);
  console.log('='.repeat(60) + '\n');
  
  const client = new RiceQuantClient();
  let strategyId = null;
  let backtestId = null;
  
  try {
    // Step 1: 检查登录
    console.log('1. Checking login...');
    const loginStatus = await client.checkLogin();
    
    if (loginStatus.code !== 0) {
      console.log('   ❌ Not logged in!');
      console.log('   Please run: node auto-login.js');
      return null;
    }
    console.log('   ✓ Logged in as:', loginStatus.fullname || loginStatus.phone);
    
    // Step 2: 创建新策略
    console.log('\n2. Creating new strategy...');
    const createResult = await client.createStrategy(`Test_${strategyName}_${Date.now()}`, code);
    
    strategyId = createResult.strategy_id || createResult._id || createResult.id;
    
    if (!strategyId) {
      console.log('   ❌ Failed to create strategy');
      console.log('   Response:', JSON.stringify(createResult).substring(0, 300));
      return null;
    }
    console.log('   ✓ Strategy created:', strategyId);
    
    // Step 3: 运行回测
    console.log('\n3. Running backtest...');
    const backtestResult = await client.runBacktest(strategyId, code, {
      startTime: startDate,
      endTime: endDate,
      baseCapital: capital,
      frequency: 'day',
      benchmark: '000300.XSHG'
    });
    
    backtestId = backtestResult.backtestId;
    
    if (typeof backtestId === 'string') {
      backtestId = backtestId.replace(/"/g, '');
    }
    
    if (!backtestId) {
      console.log('   ❌ Failed to start backtest');
      console.log('   Response:', JSON.stringify(backtestResult).substring(0, 300));
      return null;
    }
    console.log('   ✓ Backtest started:', backtestId);
    
    // Step 4: 等待回测完成
    console.log('\n4. Waiting for completion...');
    
    let completed = false;
    let attempts = 0;
    const maxAttempts = 120; // 10分钟
    
    while (!completed && attempts < maxAttempts) {
      await new Promise(r => setTimeout(r, 5000));
      attempts++;
      
      try {
        const result = await client.getBacktestResult(backtestId);
        const status = result.status || 'unknown';
        const progress = result.progress || 0;
        
        process.stdout.write(`   [${attempts}/${maxAttempts}] Status: ${status}, Progress: ${progress}%   \r`);
        
        if (status === 'finished' || status === 'completed' || progress >= 100) {
          completed = true;
          console.log('\n   ✓ Backtest completed!');
        } else if (status === 'error_exit' || status === 'failed') {
          console.log('\n   ❌ Backtest failed!');
          console.log('   Error:', result.exception || result.description);
          completed = true;
        }
      } catch (e) {
        console.log(`\n   Error checking: ${e.message}`);
      }
    }
    
    if (!completed) {
      console.log('\n   ⚠ Timeout waiting for backtest');
    }
    
    // Step 5: 获取结果
    console.log('\n5. Fetching results...');
    
    const fullResult = await client.getBacktestResult(backtestId);
    
    // 保存结果
    const timestamp = Date.now();
    const resultFile = path.join(OUTPUT_DIR, `backtest-${strategyName}-${timestamp}.json`);
    fs.writeFileSync(resultFile, JSON.stringify(fullResult, null, 2));
    console.log('   Result saved:', resultFile);
    
    // 提取关键指标
    const risk = fullResult.risk || {};
    const summary = fullResult.summary || {};
    
    const results = {
      strategyId,
      backtestId,
      strategyName,
      startDate,
      endDate,
      capital,
      annualReturn: (risk.annual_returns || 0) * 100,
      totalReturn: (risk.total_returns || 0) * 100,
      maxDrawdown: (risk.max_drawdown || 0) * 100,
      sharpe: risk.sharpe || 0,
      alpha: risk.alpha || 0,
      beta: risk.beta || 0,
      winRate: (risk.win_rate || 0) * 100,
      status: fullResult.status
    };
    
    // 打印结果
    console.log('\n' + '='.repeat(60));
    console.log('BACKTEST RESULTS');
    console.log('='.repeat(60));
    console.log('Status:', fullResult.status);
    console.log('Annual Return:', results.annualReturn.toFixed(2), '%');
    console.log('Total Return:', results.totalReturn.toFixed(2), '%');
    console.log('Max Drawdown:', results.maxDrawdown.toFixed(2), '%');
    console.log('Sharpe Ratio:', results.sharpe.toFixed(2));
    console.log('Alpha:', results.alpha.toFixed(2));
    console.log('Beta:', results.beta.toFixed(2));
    console.log('Win Rate:', results.winRate.toFixed(1), '%');
    console.log('='.repeat(60));
    
    // 保存摘要
    const summaryFile = path.join(OUTPUT_DIR, `summary-${strategyName}-${timestamp}.json`);
    fs.writeFileSync(summaryFile, JSON.stringify(results, null, 2));
    console.log('\nSummary saved:', summaryFile);
    
    return results;
    
  } catch (e) {
    console.error('\n❌ Error:', e.message);
    console.error(e.stack);
    return null;
    
  } finally {
    // Step 6: 删除策略
    if (strategyId) {
      console.log('\n6. Cleaning up...');
      const deleted = await client.deleteStrategy(strategyId);
      if (deleted) {
        console.log('   ✓ Strategy deleted:', strategyId);
      } else {
        console.log('   ⚠ Failed to delete strategy');
      }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('Done!');
    console.log('='.repeat(60));
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length < 1) {
  console.log(`
Usage: node run-backtest.js <codeFile> [startDate] [endDate] [capital]

Arguments:
  codeFile    - Strategy Python file path
  startDate   - Backtest start date (default: 2021-01-01)
  endDate     - Backtest end date (default: 2025-03-28)
  capital     - Initial capital (default: 100000)

Examples:
  # Run original strategy
  node run-backtest.js ../../strategies/Ricequant/rfscore7_pb10_final_v2.py

  # Run enhanced strategy
  node run-backtest.js ../../strategies/Ricequant/rfscore7_pb10_enhanced.py 2023-01-01 2024-12-31

  # With custom capital
  node run-backtest.js strategy.py 2021-01-01 2025-03-28 500000
`);
  process.exit(0);
}

runBacktest(
  args[0],
  args[1] || '2021-01-01',
  args[2] || '2025-03-28',
  args[3] || '100000'
);