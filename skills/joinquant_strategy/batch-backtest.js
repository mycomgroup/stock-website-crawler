#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGIES = [
  {
    name: 'V1_月度_15只',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_v1_monthly_15hold.py',
    params: { hold: [15, 12, 10, 0], freq: 'monthly' }
  },
  {
    name: 'V1.1_周度_10只',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_v1.1_weekly_10hold.py',
    params: { hold: [10, 8, 6, 0], freq: 'weekly' }
  },
  {
    name: 'V1.2_周度_12只',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_v1.2_weekly_12hold.py',
    params: { hold: [12, 9, 6, 0], freq: 'weekly' }
  },
  {
    name: 'V1.3_月度_10只',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_v1.3_monthly_10hold.py',
    params: { hold: [10, 8, 6, 0], freq: 'monthly' }
  }
];

const BACKTEST_CONFIG = {
  startTime: '2022-01-01',
  endTime: '2025-12-31',
  baseCapital: '100000',
  frequency: 'day'
};

async function runSingleBacktest(client, context, strategy, index) {
  console.log(`\n=== Running ${strategy.name} (${index + 1}/${STRATEGIES.length}) ===`);
  
  const code = fs.readFileSync(strategy.file, 'utf8');
  
  const strategyName = `RFScore_${strategy.name}_test`;
  console.log(`Updating strategy name to: ${strategyName}`);
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
  
  console.log(`Starting backtest: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
  
  const backtestId = buildResult.backtestId;
  console.log(`Backtest started, ID: ${backtestId}`);
  
  console.log('Waiting for completion...');
  let attempts = 0;
  const maxAttempts = 60;
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};
      
      process.stdout.write(`[${attempts}/${maxAttempts} Status: ${bt.status}, Progress: ${bt.progress || 0}%]`);
      
      if (result.status === 'error') {
        console.log('\nBacktest failed:', result.message);
        return { success: false, error: result.message, backtestId };
      }
      
      if (bt.finished_time || bt.status === 'finished') {
        console.log('\nBacktest completed!');
        
        const summary = result.data?.result?.summary || {};
        
        return {
          success: true,
          backtestId,
          summary: {
            name: strategy.name,
            totalReturn: summary.total_returns || 0,
            annualReturn: summary.annual_returns || 0,
            sharpe: summary.sharpe || 0,
            maxDrawdown: summary.max_drawdown || 0,
            winRate: summary.win_rate || 0,
            tradeCount: summary.trade_count || 0
          }
        };
      }
      
      if (bt.status === 'failed') {
        console.log('\nBacktest failed on server');
        return { success: false, error: 'Server failed', backtestId };
      }
    } catch (err) {
      console.log('\nError polling result:', err.message);
    }
  }
  
  console.log('\nTimeout waiting for backtest');
  return { success: false, error: 'Timeout', backtestId };
}

async function main() {
  console.log('=== RFScore Parameter Comparison Batch Backtest ===');
  console.log('Strategies to test:', STRATEGIES.length);
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Target strategy:', context.name);
  
  const results = [];
  
  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);
    
    if (result.success) {
      console.log(`\n✓ ${result.summary.name} completed`);
      console.log(`  Total Return: ${result.summary.totalReturn}%`);
      console.log(`  Annual Return: ${result.summary.annualReturn}%`);
      console.log(`  Sharpe: ${result.summary.sharpe}`);
      console.log(`  Max Drawdown: ${result.summary.maxDrawdown}%`);
    } else {
      console.log(`\n✗ Failed: ${result.error}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
  
  console.log('\n\n=== Summary ===');
  console.log('Successful backtests:', results.filter(r => r.success).length);
  console.log('Failed backtests:', results.filter(r => !r.success).length);
  
  const successful = results.filter(r => r.success).map(r => r.summary);
  if (successful.length > 0) {
    console.log('\nComparison Table:');
    console.log('-'.repeat(80));
    console.log('Name            | TotalReturn | AnnualReturn | Sharpe | MaxDD | WinRate');
    console.log('-'.repeat(80));
    
    successful.sort((a, b) => (b.totalReturn || 0) - (a.totalReturn || 0));
    
    for (const s of successful) {
      console.log(
        `${s.name.padEnd(16)} | ${(s.totalReturn || 0).toFixed(2).padStart(11)}% | ${(s.annualReturn || 0).toFixed(2).padStart(11)}% | ${(s.sharpe || 0).toFixed(2).padStart(6)} | ${(s.maxDrawdown || 0).toFixed(2).padStart(5)}% | ${(s.winRate || 0).toFixed(1).padStart(6)}%`
      );
    }
    
    const best = successful[0];
    console.log('\nBest performer:', best.name);
    console.log('Total Return:', best.totalReturn, '%');
    console.log('Sharpe Ratio:', best.sharpe);
  }
  
  const outputPath = path.join(client.outputRoot, `batch-comparison-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\nResults saved to:', outputPath);
}

main().catch(err => {
  console.error('Batch backtest failed:', err);
  process.exit(1);
});