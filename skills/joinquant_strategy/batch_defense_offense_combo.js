#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STATIC_COMBOS = [
  { name: 'Defense70_Offense30', defense: 0.7, offense: 0.3 },
  { name: 'Defense60_Offense40', defense: 0.6, offense: 0.4 },
  { name: 'Defense50_Offense50', defense: 0.5, offense: 0.5 },
  { name: 'Defense40_Offense60', defense: 0.4, offense: 0.6 }
];

const STRATEGIES = [];

STATIC_COMBOS.forEach(combo => {
  STRATEGIES.push({
    name: `${combo.name}_IS`,
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/defense_offense_combo_static.py',
    type: 'static',
    period: 'IS',
    startTime: '2020-01-01',
    endTime: '2022-10-01',
    config: combo
  });
  
  STRATEGIES.push({
    name: `${combo.name}_OOS`,
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/defense_offense_combo_static.py',
    type: 'static',
    period: 'OOS',
    startTime: '2022-10-01',
    endTime: '2025-03-30',
    config: combo
  });
});

STRATEGIES.push({
  name: 'DynamicRouter_IS',
  file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/defense_offense_combo_dynamic.py',
  type: 'dynamic',
  period: 'IS',
  startTime: '2020-01-01',
  endTime: '2022-10-01'
});

STRATEGIES.push({
  name: 'DynamicRouter_OOS',
  file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/defense_offense_combo_dynamic.py',
  type: 'dynamic',
  period: 'OOS',
  startTime: '2022-10-01',
  endTime: '2025-03-30'
});

const BACKTEST_CONFIG = {
  baseCapital: '100000',
  frequency: 'day'
};

async function runSingleBacktest(client, context, strategy, index) {
  console.log(`\n=== Running ${strategy.name} (${index + 1}/${STRATEGIES.length}) ===`);
  
  const code = fs.readFileSync(strategy.file, 'utf8');
  
  let modifiedCode = code;
  if (strategy.config) {
    modifiedCode = code.replace(/DEFENSE_WEIGHT = 0\.6/, `DEFENSE_WEIGHT = ${strategy.config.defense}`);
    modifiedCode = modifiedCode.replace(/OFFENSE_WEIGHT = 0\.4/, `OFFENSE_WEIGHT = ${strategy.config.offense}`);
  }
  
  const strategyName = `Defense_Offense_${strategy.name}_test`;
  console.log(`Updating strategy name to: ${strategyName}`);
  await client.saveStrategy(ALGORITHM_ID, strategyName, modifiedCode, context);
  
  console.log(`Starting backtest: ${strategy.startTime} ~ ${strategy.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, modifiedCode, {
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
            type: strategy.type,
            period: strategy.period,
            config: strategy.config,
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
  console.log('=== Defense-Offense Combination Batch Backtest ===');
  console.log('Strategies to test:', STRATEGIES.length);
  console.log('IS Period: 2020-01-01 ~ 2022-10-01 (60%)');
  console.log('OOS Period: 2022-10-01 ~ 2025-03-30 (40%)');
  console.log('\nStatic Weight Combinations:');
  STATIC_COMBOS.forEach(c => {
    console.log(`  - ${c.name}: Defense ${c.defense*100}% + Offense ${c.offense*100}%`);
  });
  console.log('Dynamic Router: State-based allocation');
  
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
    console.log('-'.repeat(120));
    console.log('Strategy                         | Type    | Period | TotalReturn | AnnualReturn | Sharpe | MaxDD   | WinRate');
    console.log('-'.repeat(120));
    
    for (const s of successful) {
      console.log(
        `${s.name.padEnd(31)} | ${(s.type || 'static').padEnd(7)} | ${s.period.padEnd(6)} | ${(s.totalReturn || 0).toFixed(2).padStart(11)}% | ${(s.annualReturn || 0).toFixed(2).padStart(11)}% | ${(s.sharpe || 0).toFixed(2).padStart(6)} | ${(s.maxDrawdown || 0).toFixed(2).padStart(6)}% | ${(s.winRate || 0).toFixed(1).padStart(6)}%`
      );
    }
    
    console.log('\n=== Static Weight Analysis ===');
    
    for (const combo of STATIC_COMBOS) {
      const comboResults = successful.filter(s => s.name.startsWith(combo.name));
      if (comboResults.length >= 2) {
        const isResult = comboResults.find(r => r.period === 'IS');
        const oosResult = comboResults.find(r => r.period === 'OOS');
        
        console.log(`\n${combo.name}:`);
        console.log(`  IS:  Annual Return ${isResult?.annualReturn || 0}%, Sharpe ${isResult?.sharpe || 0}, MaxDD ${isResult?.maxDrawdown || 0}%`);
        console.log(`  OOS: Annual Return ${oosResult?.annualReturn || 0}%, Sharpe ${oosResult?.sharpe || 0}, MaxDD ${oosResult?.maxDrawdown || 0}%`);
        
        const oosSharpe = oosResult?.sharpe || 0;
        const oosMaxDD = oosResult?.maxDrawdown || 0;
        const meetsStandard = oosSharpe > 0.5 && Math.abs(oosMaxDD) < 20;
        console.log(`  Meets Standard: ${meetsStandard ? '✅ YES' : '❌ NO'}`);
      }
    }
    
    console.log('\n=== Dynamic Router Analysis ===');
    const dynamicResults = successful.filter(s => s.type === 'dynamic');
    if (dynamicResults.length >= 2) {
      const isResult = dynamicResults.find(r => r.period === 'IS');
      const oosResult = dynamicResults.find(r => r.period === 'OOS');
      
      console.log(`\nDynamic Router:`);
      console.log(`  IS:  Annual Return ${isResult?.annualReturn || 0}%, Sharpe ${isResult?.sharpe || 0}, MaxDD ${isResult?.maxDrawdown || 0}%`);
      console.log(`  OOS: Annual Return ${oosResult?.annualReturn || 0}%, Sharpe ${oosResult?.sharpe || 0}, MaxDD ${oosResult?.maxDrawdown || 0}%`);
      
      const oosSharpe = oosResult?.sharpe || 0;
      const oosMaxDD = oosResult?.maxDrawdown || 0;
      const meetsStandard = oosSharpe > 0.5 && Math.abs(oosMaxDD) < 20;
      console.log(`  Meets Standard: ${meetsStandard ? '✅ YES' : '❌ NO'}`);
    }
  }
  
  const outputPath = path.join(client.outputRoot, `defense-offense-comparison-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\nResults saved to:', outputPath);
}

main().catch(err => {
  console.error('Batch backtest failed:', err);
  process.exit(1);
});