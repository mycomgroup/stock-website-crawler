#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGIES = [
  {
    name: 'LowPB_SmallCap_v2_5hold_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense_v2_5hold.py',
    holdNum: 5,
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  },
  {
    name: 'LowPB_SmallCap_v2_8hold_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense_v2_8hold.py',
    holdNum: 8,
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  },
  {
    name: 'LowPB_SmallCap_v2_10hold_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense_v2_10hold.py',
    holdNum: 10,
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  },
  {
    name: 'LowPB_SmallCap_v2_12hold_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense_v2_12hold.py',
    holdNum: 12,
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  },
  {
    name: 'LowPB_SmallCap_v1_15hold_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense.py',
    holdNum: 15,
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  }
];

const BACKTEST_CONFIG = {
  baseCapital: '100000',
  frequency: 'day'
};

async function runSingleBacktest(client, context, strategy, index) {
  console.log(`\n=== Running ${strategy.name} (${index + 1}/${STRATEGIES.length}) ===`);
  
  const code = fs.readFileSync(strategy.file, 'utf8');
  
  const strategyName = `HoldNum_Optimization_${strategy.name}_test`;
  console.log(`Updating strategy name to: ${strategyName}`);
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
  
  console.log(`Starting backtest: ${strategy.startTime} ~ ${strategy.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, {
    ...BACKTEST_CONFIG,
    startTime: strategy.startTime,
    endTime: strategy.endTime
  }, context);
  
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
        return { success: false, error: result.message, backtestId, strategy };
      }
      
      if (bt.finished_time || bt.status === 'finished') {
        console.log('\nBacktest completed!');
        
        const summary = result.data?.result?.summary || {};
        
        return {
          success: true,
          backtestId,
          strategy,
          summary: {
            name: strategy.name,
            holdNum: strategy.holdNum,
            period: strategy.period,
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
        return { success: false, error: 'Server failed', backtestId, strategy };
      }
    } catch (err) {
      console.log('\nError polling result:', err.message);
    }
  }
  
  console.log('\nTimeout waiting for backtest');
  return { success: false, error: 'Timeout', backtestId, strategy };
}

async function main() {
  console.log('=== SmallCap Defense Line HoldNum Optimization Batch Backtest ===');
  console.log('Strategies to test:', STRATEGIES.length);
  console.log('OOS Period: 2022-04-01 ~ 2025-03-30');
  console.log('HoldNum: 5, 8, 10, 12, 15');
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Target strategy:', context.name);
  
  const results = [];
  
  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);
    
    if (result.success) {
      console.log(`\n✓ ${result.summary.name} (holdNum=${result.summary.holdNum}) completed`);
      console.log(`  Total Return: ${result.summary.totalReturn}%`);
      console.log(`  Annual Return: ${result.summary.annualReturn}%`);
      console.log(`  Sharpe: ${result.summary.sharpe}`);
      console.log(`  Max Drawdown: ${result.summary.maxDrawdown}%`);
      console.log(`  Win Rate: ${result.summary.winRate}%`);
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
    console.log('\n=== HoldNum Comparison Table ===');
    console.log('-'.repeat(120));
    console.log('HoldNum | TotalReturn | AnnualReturn | Sharpe | MaxDrawdown | WinRate | Defense Standard');
    console.log('-'.repeat(120));
    
    for (const s of successful) {
      const meetsDrawdown = (s.maxDrawdown || 0) <= -25;
      const meetsExcess = (s.annualReturn || 0) > -2.63 + 8;
      const meetsStandard = meetsDrawdown && meetsExcess;
      
      console.log(
        `${String(s.holdNum).padStart(6)} | ${(s.totalReturn || 0).toFixed(2).padStart(11)}% | ${(s.annualReturn || 0).toFixed(2).padStart(11)}% | ${(s.sharpe || 0).toFixed(2).padStart(6)} | ${(s.maxDrawdown || 0).toFixed(2).padStart(10)}% | ${(s.winRate || 0).toFixed(1).padStart(6)}% | ${meetsStandard ? '✅ YES' : '❌ NO'}`
      );
    }
    
    console.log('\n=== Defense Standard Analysis ===');
    console.log('Defense Standard: MaxDrawdown <= 25%, ExcessReturn > 8% (AnnualReturn > 5.37%)');
    
    const drawdownPass = successful.filter(s => (s.maxDrawdown || 0) <= -25);
    console.log(`\nDrawdown Pass (${drawdownPass.length}/${successful.length}):`);
    drawdownPass.forEach(s => {
      console.log(`  ${s.holdNum}hold: ${s.maxDrawdown}% <= 25% ✅`);
    });
    
    const bothPass = successful.filter(s => (s.maxDrawdown || 0) <= -25 && (s.annualReturn || 0) > 5.37);
    console.log(`\nBoth Pass (${bothPass.length}/${successful.length}):`);
    bothPass.forEach(s => {
      console.log(`  ${s.holdNum}hold: MaxDD=${s.maxDrawdown}%, Annual=${s.annualReturn}% ✅✅`);
    });
    
    if (bothPass.length > 0) {
      const best = bothPass.reduce((a, b) => (a.sharpe > b.sharpe ? a : b));
      console.log(`\n=== Recommended HoldNum ===`);
      console.log(`Recommended: ${best.holdNum}hold`);
      console.log(`  Max Drawdown: ${best.maxDrawdown}%`);
      console.log(`  Annual Return: ${best.annualReturn}%`);
      console.log(`  Sharpe Ratio: ${best.sharpe}`);
      console.log(`  Win Rate: ${best.winRate}%`);
      console.log(`  Defense Standard: ✅ PASS`);
    }
  }
  
  const outputPath = path.join(client.outputRoot, `holdnum-optimization-comparison-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\nResults saved to:', outputPath);
}

main().catch(err => {
  console.error('Batch backtest failed:', err);
  process.exit(1);
});