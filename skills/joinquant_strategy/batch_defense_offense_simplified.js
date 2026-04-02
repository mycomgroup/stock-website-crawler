#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

// 简化版：只测试3个关键配置，缩短回测周期
const STRATEGIES = [
  {
    name: 'Defense_Only',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/smallcap_low_pb_defense.py',
    type: 'single',
    subtype: 'defense',
    startTime: '2024-01-01',
    endTime: '2025-03-30'
  },
  {
    name: 'Static_60_40',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/defense_offense_combo_static.py',
    type: 'combo',
    subtype: 'static',
    config: { defense: 0.6, offense: 0.4 },
    startTime: '2024-01-01',
    endTime: '2025-03-30'
  },
  {
    name: 'Dynamic_Router',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/defense_offense_combo_dynamic.py',
    type: 'combo',
    subtype: 'dynamic',
    startTime: '2024-01-01',
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
  
  let modifiedCode = code;
  if (strategy.config) {
    modifiedCode = code.replace(/DEFENSE_WEIGHT = 0\.6/, `DEFENSE_WEIGHT = ${strategy.config.defense}`);
    modifiedCode = modifiedCode.replace(/OFFENSE_WEIGHT = 0\.4/, `OFFENSE_WEIGHT = ${strategy.config.offense}`);
  }
  
  const strategyName = `Defense_Offense_${strategy.name}_2024`;
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
  const maxAttempts = 30; // 减少等待次数
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 3000)); // 减少轮询间隔
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};
      
      if (attempts % 5 === 0) {
        process.stdout.write(`[${attempts}/${maxAttempts} Status: ${bt.status || 'running'}, Progress: ${bt.progress || 0}%]`);
      }
      
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
            subtype: strategy.subtype,
            totalReturn: summary.total_returns || 0,
            annualReturn: summary.annual_returns || 0,
            sharpe: summary.sharpe || 0,
            maxDrawdown: summary.max_drawdown || 0,
            winRate: summary.win_rate || 0,
            tradeCount: summary.trade_count || 0,
            startDate: strategy.startTime,
            endDate: strategy.endTime
          }
        };
      }
      
      if (bt.status === 'failed') {
        console.log('\nBacktest failed on server');
        return { success: false, error: 'Server failed', backtestId, strategy };
      }
    } catch (err) {
      if (attempts % 5 === 0) {
        console.log('\nError polling result:', err.message);
      }
    }
  }
  
  console.log('\nTimeout waiting for backtest');
  return { success: false, error: 'Timeout', backtestId, strategy };
}

async function main() {
  console.log('=== Defense-Offense Combination Test (Simplified) ===');
  console.log('Period: 2024-01-01 ~ 2025-03-30 (15 months)');
  console.log('Strategies to test:', STRATEGIES.length);
  console.log('');
  STRATEGIES.forEach((s, i) => {
    console.log(`${i+1}. ${s.name}: ${s.type}${s.config ? ` (${s.config.defense*100}%/${s.config.offense*100}%)` : ''}`);
  });
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('\nTarget strategy:', context.name);
  
  const results = [];
  
  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);
    
    if (result.success) {
      console.log(`\n✓ ${result.summary.name} completed`);
      console.log(`  Total Return: ${result.summary.totalReturn.toFixed(2)}%`);
      console.log(`  Annual Return: ${result.summary.annualReturn.toFixed(2)}%`);
      console.log(`  Sharpe: ${result.summary.sharpe.toFixed(2)}`);
      console.log(`  Max Drawdown: ${result.summary.maxDrawdown.toFixed(2)}%`);
      console.log(`  Trade Count: ${result.summary.tradeCount}`);
    } else {
      console.log(`\n✗ Failed: ${result.error}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  console.log('\n\n' + '='.repeat(80));
  console.log('SUMMARY RESULTS');
  console.log('='.repeat(80));
  
  const successful = results.filter(r => r.success).map(r => r.summary);
  console.log('\nComparison Table:');
  console.log('-'.repeat(100));
  console.log('Strategy         | Type    | TotalReturn | AnnualReturn | Sharpe | MaxDD   | Trades');
  console.log('-'.repeat(100));
  
  for (const s of successful) {
    console.log(
      `${s.name.padEnd(15)} | ${(s.subtype || s.type).padEnd(7)} | ${s.totalReturn.toFixed(2).padStart(10)}% | ${s.annualReturn.toFixed(2).padStart(11)}% | ${s.sharpe.toFixed(2).padStart(6)} | ${s.maxDrawdown.toFixed(2).padStart(6)}% | ${s.tradeCount.toString().padStart(6)}`
    );
  }
  
  if (successful.length > 0) {
    console.log('\n' + '='.repeat(80));
    console.log('ANALYSIS');
    console.log('='.repeat(80));
    
    const defenseOnly = successful.find(s => s.name === 'Defense_Only');
    const staticCombo = successful.find(s => s.name === 'Static_60_40');
    const dynamicCombo = successful.find(s => s.name === 'Dynamic_Router');
    
    if (defenseOnly && staticCombo) {
      console.log('\nStatic Combo vs Defense Only:');
      const returnDiff = staticCombo.annualReturn - defenseOnly.annualReturn;
      const sharpeDiff = staticCombo.sharpe - defenseOnly.sharpe;
      const drawdownDiff = staticCombo.maxDrawdown - defenseOnly.maxDrawdown;
      
      console.log(`  Annual Return: ${returnDiff >= 0 ? '+' : ''}${returnDiff.toFixed(2)}% (${staticCombo.annualReturn.toFixed(2)}% vs ${defenseOnly.annualReturn.toFixed(2)}%)`);
      console.log(`  Sharpe: ${sharpeDiff >= 0 ? '+' : ''}${sharpeDiff.toFixed(2)} (${staticCombo.sharpe.toFixed(2)} vs ${defenseOnly.sharpe.toFixed(2)})`);
      console.log(`  Max Drawdown: ${drawdownDiff >= 0 ? '+' : ''}${drawdownDiff.toFixed(2)}% (${staticCombo.maxDrawdown.toFixed(2)}% vs ${defenseOnly.maxDrawdown.toFixed(2)}%)`);
      
      if (returnDiff > 0 && sharpeDiff > 0) {
        console.log('  ✅ Static Combo improves both return and Sharpe ratio');
      }
    }
    
    if (staticCombo && dynamicCombo) {
      console.log('\nDynamic Router vs Static Combo:');
      const returnDiff = dynamicCombo.annualReturn - staticCombo.annualReturn;
      const sharpeDiff = dynamicCombo.sharpe - staticCombo.sharpe;
      const drawdownDiff = dynamicCombo.maxDrawdown - staticCombo.maxDrawdown;
      
      console.log(`  Annual Return: ${returnDiff >= 0 ? '+' : ''}${returnDiff.toFixed(2)}% (${dynamicCombo.annualReturn.toFixed(2)}% vs ${staticCombo.annualReturn.toFixed(2)}%)`);
      console.log(`  Sharpe: ${sharpeDiff >= 0 ? '+' : ''}${sharpeDiff.toFixed(2)} (${dynamicCombo.sharpe.toFixed(2)} vs ${staticCombo.sharpe.toFixed(2)})`);
      console.log(`  Max Drawdown: ${drawdownDiff >= 0 ? '+' : ''}${drawdownDiff.toFixed(2)}% (${dynamicCombo.maxDrawdown.toFixed(2)}% vs ${staticCombo.maxDrawdown.toFixed(2)}%)`);
      
      if (returnDiff > 0 || sharpeDiff > 0 || drawdownDiff > 0) {
        console.log('  ✅ Dynamic Router shows improvement over static weights');
      }
    }
    
    console.log('\n' + '='.repeat(80));
    console.log('RECOMMENDATION');
    console.log('='.repeat(80));
    
    if (dynamicCombo && dynamicCombo.sharpe > 0.5) {
      console.log('✅ Dynamic Router is the recommended approach');
    } else if (staticCombo && staticCombo.sharpe > 0.5) {
      console.log('✅ Static Combo (60/40) is a viable alternative');
    } else {
      console.log('⚠️  Both approaches need further optimization');
    }
  }
  
  const outputPath = path.join(client.outputRoot, `defense-offense-simplified-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\nResults saved to:', outputPath);
}

main().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});