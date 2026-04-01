#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BASE_STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/capacity_test_simple.py';

const TEST_CASES = [
  { name: '容量10万', capital: '100000', slippage: 0 },
  { name: '容量50万', capital: '500000', slippage: 0 },
  { name: '容量100万', capital: '1000000', slippage: 0 },
  { name: '容量300万', capital: '3000000', slippage: 0 },
  { name: '容量500万', capital: '5000000', slippage: 0 },
  { name: '容量1000万', capital: '10000000', slippage: 0 },
  { name: '滑点0bps', capital: '1000000', slippage: 0 },
  { name: '滑点10bps', capital: '1000000', slippage: 10 },
  { name: '滑点20bps', capital: '1000000', slippage: 20 },
  { name: '滑点30bps', capital: '1000000', slippage: 30 },
  { name: '滑点50bps', capital: '1000000', slippage: 50 },
  { name: '滑点100bps', capital: '1000000', slippage: 100 }
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

async function runSingleBacktest(client, context, testCase, index) {
  console.log(`\n=== Running ${testCase.name} (${index + 1}/${TEST_CASES.length}) ===`);

  const baseCode = fs.readFileSync(BASE_STRATEGY_FILE, 'utf8');
  const code = generateStrategyCode(baseCode, testCase.slippage);

  const strategyName = `小市值容量滑点_${testCase.name}`;

  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);

  const backtestConfig = {
    ...BACKTEST_CONFIG_BASE,
    baseCapital: testCase.capital
  };

  console.log(`Capital: ${testCase.capital}, Slippage: ${testCase.slippage}bps`);

  const buildResult = await client.runBacktest(ALGORITHM_ID, code, backtestConfig, context);

  const backtestId = buildResult.backtestId;
  console.log(`Backtest ID: ${backtestId}`);

  console.log('Waiting for completion...');
  let attempts = 0;
  const maxAttempts = 120;

  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 3000));
    attempts++;

    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};

      if (attempts % 10 === 0) {
        process.stdout.write(`[${attempts}/${maxAttempts}]`);
      }

      if (result.status === 'error') {
        console.log('\nBacktest failed:', result.message);
        return { success: false, error: result.message, testCase };
      }

      if (bt.finished_time || bt.status === 'finished') {
        console.log('\nCompleted!');

        const summary = result.data?.result?.summary || {};

        return {
          success: true,
          backtestId,
          testCase,
          summary: {
            name: testCase.name,
            capital: testCase.capital,
            slippage: testCase.slippage,
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
        return { success: false, error: 'Server failed', testCase };
      }
    } catch (err) {
      if (attempts % 10 === 0) {
        console.log(`\nError: ${err.message.slice(0, 50)}`);
      }
    }
  }

  console.log('\nTimeout');
  return { success: false, error: 'Timeout', testCase, backtestId };
}

async function main() {
  console.log('=== 小市值事件策略容量与滑点测试 ===');

  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });

  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Target strategy:', context.name);

  const results = [];

  for (let i = 0; i < TEST_CASES.length; i++) {
    const result = await runSingleBacktest(client, context, TEST_CASES[i], i);
    results.push(result);

    if (result.success) {
      console.log(`✓ Annual Return: ${result.summary.annualReturn}%, Trades: ${result.summary.tradeCount}`);
    } else {
      console.log(`✗ Error: ${result.error}`);
    }

    await new Promise(resolve => setTimeout(resolve, 3000));
  }

  const capacityResults = results.filter(r => r.success && r.testCase.name.startsWith('容量'));
  const slippageResults = results.filter(r => r.success && r.testCase.name.startsWith('滑点'));

  const report = {
    testDate: new Date().toISOString(),
    capacityResults: capacityResults.map(r => r.summary),
    slippageResults: slippageResults.map(r => r.summary),
    allResults: results
  };

  const outputPath = path.join(OUTPUT_DIR, `capacity_slippage_results_${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
  console.log('\n\nResults saved to:', outputPath);

  console.log('\n=== 容量测试结果 ===');
  if (capacityResults.length > 0) {
    console.log('规模 | 年化收益 | 最大回撤 | 交易次数');
    capacityResults.forEach(r => {
      console.log(`${r.summary.capital} | ${r.summary.annualReturn.toFixed(2)}% | ${r.summary.maxDrawdown.toFixed(2)}% | ${r.summary.tradeCount}`);
    });
  } else {
    console.log('无成功结果');
  }

  console.log('\n=== 滑点测试结果 ===');
  if (slippageResults.length > 0) {
    const baseline = slippageResults.find(r => r.testCase.slippage === 0)?.summary?.annualReturn || 0;
    console.log('滑点 | 年化收益 | 收益衰减');
    slippageResults.forEach(r => {
      const decay = baseline > 0 ? ((baseline - r.summary.annualReturn) / baseline * 100).toFixed(1) : 'N/A';
      console.log(`${r.testCase.slippage}bps | ${r.summary.annualReturn.toFixed(2)}% | ${decay}%`);
    });
  } else {
    console.log('无成功结果');
  }

  return report;
}

main().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});