#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BACKTEST_CONFIG = {
  startTime: '2024-01-01',
  endTime: '2025-12-31',
  baseCapital: '100000',
  frequency: 'day'
};

const BASE_STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore7_pb10_final.py';

async function main() {
  console.log('=== Fixed Backtest Test ===');
  
  console.log('\n[1] Ensuring session...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  
  const client = new JoinQuantStrategyClient();
  
  console.log('\n[2] Getting strategy context...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Strategy:', context.name);
  
  console.log('\n[3] Reading strategy code...');
  const code = fs.readFileSync(BASE_STRATEGY_FILE, 'utf8');
  console.log('Code length:', code.length, 'chars');
  
  console.log('\n[4] Running backtest with code...');
  console.log(`Period: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  
  // 重要：传入实际的代码，而不是空字符串
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log('Backtest ID:', backtestId);
  
  console.log('\n[5] Polling for results (max 3 minutes)...');
  const startTime = Date.now();
  const maxWait = 180000;
  
  while (Date.now() - startTime < maxWait) {
    await new Promise(r => setTimeout(r, 5000));
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      
      // 检查状态
      const state = result?.data?.state;
      console.log(`[${Math.floor((Date.now() - startTime) / 1000)}s] State: ${state}`);
      
      // state: 0=完成, 1=进行中, 2=等待中, 3=失败
      if (state === '0' || state === 0) {
        console.log('\n✓ BACKTEST COMPLETE!');
        
        const log = await client.getLog(backtestId);
        const stats = await client.getBacktestStats(backtestId, context);
        
        console.log('='.repeat(60));
        const s = stats?.data || {};
        if (s.total_returns) {
          console.log(`Total Return: ${(s.total_returns * 100).toFixed(2)}%`);
          console.log(`Annual Return: ${(s.annual_returns * 100).toFixed(2)}%`);
          console.log(`Sharpe: ${s.sharpe?.toFixed(3) || 'N/A'}`);
          console.log(`Max Drawdown: ${(s.max_drawdown * 100).toFixed(2)}%`);
        } else {
          console.log('Stats not available yet');
        }
        
        if (log?.data?.logArr?.length > 0) {
          console.log('\nFirst 10 log lines:');
          log.data.logArr.slice(0, 10).forEach(l => console.log(l.slice(0, 200)));
        }
        
        const outFile = path.join('data', `fixed_test_${Date.now()}.json`);
        fs.writeFileSync(outFile, JSON.stringify({ result, stats, log }, null, 2));
        console.log('\nSaved to:', outFile);
        return;
      }
      
      if (state === '3' || state === 3) {
        console.log('\n✗ BACKTEST FAILED!');
        const log = await client.getLog(backtestId);
        if (log?.data?.logArr?.length > 0) {
          console.log('Error log:');
          log.data.logArr.slice(0, 5).forEach(l => console.log(l.slice(0, 500)));
        }
        return;
      }
    } catch (err) {
      console.log('Error:', err.message);
    }
  }
  
  console.log('\n⚠ Timeout after 3 minutes');
}

main().catch(err => {
  console.error('Failed:', err);
  process.exit(1);
});