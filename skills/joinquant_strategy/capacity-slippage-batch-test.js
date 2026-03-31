#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BASE_STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/capacity_slippage_test.py';

const CAPACITIES = [
  { name: '10万', capital: '100000' },
  { name: '50万', capital: '500000' },
  { name: '100万', capital: '1000000' },
  { name: '300万', capital: '3000000' },
  { name: '500万', capital: '5000000' },
  { name: '1000万', capital: '10000000' }
];

const SLIPPAGES = [
  { name: '0bps', bps: 0 },
  { name: '10bps', bps: 10 },
  { name: '20bps', bps: 20 },
  { name: '30bps', bps: 30 },
  { name: '50bps', bps: 50 },
  { name: '100bps', bps: 100 }
];

const BACKTEST_CONFIG_BASE = {
  startTime: '2024-01-01',
  endTime: '2025-03-31',
  frequency: 'day'
};

const OUTPUT_DIR = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/data';

function generateStrategyCode(baseCode, slippageBps) {
  return baseCode.replace(
    /SLIPPAGE_BPS = \d+/,
    `SLIPPAGE_BPS = ${slippageBps}`
  );
}

async function runSingleBacktest(client, context, strategyName, code, capital) {
  console.log(`\n=== Running ${strategyName} (${capital}) ===`);

  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);

  const backtestConfig = {
    ...BACKTEST_CONFIG_BASE,
    baseCapital: capital
  };

  console.log(`Starting backtest: ${backtestConfig.startTime} ~ ${backtestConfig.endTime}, Capital: ${capital}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, backtestConfig, context);

  const backtestId = buildResult.backtestId;
  console.log(`Backtest ID: ${backtestId}`);

  console.log('Waiting for completion...');
  let attempts = 0;
  const maxAttempts = 90;

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
            name: strategyName,
            capital: capital,
            totalReturn: summary.total_returns || 0,
            annualReturn: summary.annual_returns || 0,
            sharpe: summary.sharpe || 0,
            maxDrawdown: summary.max_drawdown || 0,
            winRate: summary.win_rate || 0,
            tradeCount: summary.trade_count || 0,
            benchmarkReturn: summary.benchmark_total_returns || 0
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

async function runCapacityTests(client, context, baseCode) {
  console.log('\n\n=== 容量测试 ===');
  const results = [];

  for (const cap of CAPACITIES) {
    const strategyName = `容量测试_${cap.name}_slippage0`;

    const code = generateStrategyCode(baseCode, 0);

    const result = await runSingleBacktest(client, context, strategyName, code, cap.capital);
    results.push(result);

    if (result.success) {
      console.log(`\n✓ ${result.summary.name} completed`);
      console.log(`  Annual Return: ${result.summary.annualReturn}%`);
      console.log(`  Trade Count: ${result.summary.tradeCount}`);
    } else {
      console.log(`\n✗ Failed: ${result.error}`);
    }

    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  return results;
}

async function runSlippageTests(client, context, baseCode) {
  console.log('\n\n=== 滑点测试 ===');
  const results = [];

  const baseCapital = '1000000';

  for (const slip of SLIPPAGES) {
    const strategyName = `滑点测试_${slip.name}_100万`;

    const code = generateStrategyCode(baseCode, slip.bps);

    const result = await runSingleBacktest(client, context, strategyName, code, baseCapital);
    results.push(result);

    if (result.success) {
      console.log(`\n✓ ${result.summary.name} completed`);
      console.log(`  Annual Return: ${result.summary.annualReturn}%`);
      console.log(`  Max Drawdown: ${result.summary.maxDrawdown}%`);
    } else {
      console.log(`\n✗ Failed: ${result.error}`);
    }

    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  return results;
}

function formatResultsTable(results, type) {
  const successful = results.filter(r => r.success).map(r => r.summary);

  if (successful.length === 0) {
    return '无成功回测';
  }

  let table = '';
  if (type === 'capacity') {
    table += '| 资金规模 | 年化收益 | 最大回撤 | 交易次数 | 夏普比率 | 胜率 |\n';
    table += '|----------|----------|----------|----------|----------|------|\n';
    for (const s of successful) {
      table += `| ${s.capital} | ${s.annualReturn.toFixed(2)}% | ${s.maxDrawdown.toFixed(2)}% | ${s.tradeCount} | ${s.sharpe.toFixed(2)} | ${s.winRate.toFixed(1)}% |\n`;
    }
  } else if (type === 'slippage') {
    table += '| 滑点 | 年化收益 | 最大回撤 | 收益衰减 | 夏普比率 | 胜率 |\n';
    table += '|------|----------|----------|----------|----------|------|\n';

    const baselineReturn = successful.find(s => s.name.includes('0bps'))?.annualReturn || 0;

    for (const s of successful) {
      const slippageName = s.name.match(/滑点测试_(\d+bps)/)?.[1] || '未知';
      const decay = baselineReturn > 0 ? ((baselineReturn - s.annualReturn) / baselineReturn * 100).toFixed(1) : 'N/A';
      table += `| ${slippageName} | ${s.annualReturn.toFixed(2)}% | ${s.maxDrawdown.toFixed(2)}% | ${decay}% | ${s.sharpe.toFixed(2)} | ${s.winRate.toFixed(1)}% |\n`;
    }
  }

  return table;
}

async function main() {
  console.log('=== 小市值事件策略容量与滑点测试 ===');

  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });

  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Target strategy:', context.name);

  const baseCode = fs.readFileSync(BASE_STRATEGY_FILE, 'utf8');

  const capacityResults = await runCapacityTests(client, context, baseCode);

  const slippageResults = await runSlippageTests(client, context, baseCode);

  const report = {
    testDate: new Date().toISOString(),
    capacityResults: capacityResults.filter(r => r.success).map(r => r.summary),
    slippageResults: slippageResults.filter(r => r.success).map(r => r.summary),
    capacityTable: formatResultsTable(capacityResults, 'capacity'),
    slippageTable: formatResultsTable(slippageResults, 'slippage')
  };

  const outputPath = path.join(OUTPUT_DIR, `capacity_slippage_test_results_${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
  console.log('\nResults saved to:', outputPath);

  console.log('\n\n=== 容量测试结果 ===');
  console.log(report.capacityTable);

  console.log('\n\n=== 滑点测试结果 ===');
  console.log(report.slippageTable);

  return report;
}

main().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});