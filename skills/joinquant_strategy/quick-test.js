#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BASE_STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/capacity_minimal.py';

async function quickTest() {
  console.log('=== Quick Test ===');

  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });

  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);

  const baseCode = fs.readFileSync(BASE_STRATEGY_FILE, 'utf8');
  const code = baseCode.replace(/SLIPPAGE_BPS = \d+/, 'SLIPPAGE_BPS = 0');

  const strategyName = '小市值容量测试_快速验证';

  console.log('Saving strategy...');
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);

  const backtestConfig = {
    startTime: '2024-01-01',
    endTime: '2024-03-31',
    baseCapital: '100000',
    frequency: 'day'
  };

  console.log('Starting backtest (Q1 2024 only)...');
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, backtestConfig, context);

  const backtestId = buildResult.backtestId;
  console.log('Backtest ID:', backtestId);

  console.log('Waiting for result...');
  let attempts = 0;
  const maxAttempts = 60;

  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    attempts++;

    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};

      if (result.status === 'error') {
        console.log('Error:', result.message);
        return { error: result.message };
      }

      if (bt.finished_time || bt.status === 'finished') {
        console.log('Completed!');
        const summary = result.data?.result?.summary || {};
        console.log('Annual Return:', summary.annual_returns);
        console.log('Trade Count:', summary.trade_count);
        return { success: true, summary };
      }

      if (bt.status === 'failed') {
        console.log('Failed on server');
        return { error: 'Server failed' };
      }

      if (attempts % 10 === 0) {
        console.log(`[${attempts}/${maxAttempts}] status: ${bt.status || 'running'}`);
      }
    } catch (err) {
      console.log('Poll error:', err.message.slice(0, 50));
    }
  }

  console.log('Timeout');
  return { error: 'Timeout' };
}

quickTest().then(r => {
  console.log('\nResult:', JSON.stringify(r, null, 2));
}).catch(e => {
  console.error('Error:', e);
});