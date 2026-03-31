#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGIES = [
  {
    name: 'Quality_SmallCap_IS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_quality_defense.py',
    period: 'IS',
    startTime: '2018-01-01',
    endTime: '2022-04-01'
  },
  {
    name: 'Quality_SmallCap_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_quality_defense.py',
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  },
  {
    name: 'Dividend_SmallCap_IS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_dividend_defense.py',
    period: 'IS',
    startTime: '2018-01-01',
    endTime: '2022-04-01'
  },
  {
    name: 'Dividend_SmallCap_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_dividend_defense.py',
    period: 'OOS',
    startTime: '2022-04-01',
    endTime: '2025-03-30'
  },
  {
    name: 'LowPB_SmallCap_IS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense.py',
    period: 'IS',
    startTime: '2018-01-01',
    endTime: '2022-04-01'
  },
  {
    name: 'LowPB_SmallCap_OOS',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense.py',
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
  
  const strategyName = `SmallCap_Defense_${strategy.name}_test`;
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
  console.log('=== SmallCap Defense Line Batch Backtest ===');
  console.log('Strategies to test:', STRATEGIES.length);
  console.log('IS Period: 2018-01-01 ~ 2022-04-01');
  console.log('OOS Period: 2022-04-01 ~ 2025-03-30');
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Target strategy:', context.name);
  
  const results = [];
  
  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);
    
    if (result.success) {
      console.log(`\n✓ ${result.summary.name} (${result.summary.period}) completed`);
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
    console.log('\nIS/OOS Comparison Table:');
    console.log('-'.repeat(100));
    console.log('Strategy                    | Period | TotalReturn | AnnualReturn | Sharpe | MaxDD   | WinRate');
    console.log('-'.repeat(100));
    
    for (const s of successful) {
      console.log(
        `${s.name.padEnd(27)} | ${s.period.padEnd(6)} | ${(s.totalReturn || 0).toFixed(2).padStart(11)}% | ${(s.annualReturn || 0).toFixed(2).padStart(11)}% | ${(s.sharpe || 0).toFixed(2).padStart(6)} | ${(s.maxDrawdown || 0).toFixed(2).padStart(6)}% | ${(s.winRate || 0).toFixed(1).padStart(6)}%`
      );
    }
    
    console.log('\n=== Strategy Type Summary ===');
    const strategyTypes = ['Quality', 'Dividend', 'LowPB'];
    
    for (const type of strategyTypes) {
      const typeResults = successful.filter(s => s.name.startsWith(type));
      if (typeResults.length >= 2) {
        const isResult = typeResults.find(r => r.period === 'IS');
        const oosResult = typeResults.find(r => r.period === 'OOS');
        
        console.log(`\n${type} Strategy:`);
        console.log(`  IS:  Annual Return ${isResult?.annualReturn || 0}%, Sharpe ${isResult?.sharpe || 0}, MaxDD ${isResult?.maxDrawdown || 0}%`);
        console.log(`  OOS: Annual Return ${oosResult?.annualReturn || 0}%, Sharpe ${oosResult?.sharpe || 0}, MaxDD ${oosResult?.maxDrawdown || 0}%`);
        
        if (oosResult) {
          const meetsStandard = (oosResult.annualReturn || 0) > 8 && (oosResult.maxDrawdown || 0) <= 25;
          console.log(`  Meets Defense Standard: ${meetsStandard ? '✅ YES' : '❌ NO'}`);
        }
      }
    }
  }
  
  const outputPath = path.join(client.outputRoot, `smallcap-defense-comparison-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\nResults saved to:', outputPath);
}

main().catch(err => {
  console.error('Batch backtest failed:', err);
  process.exit(1);
});