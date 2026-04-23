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
  console.log('=== Simple Backtest Test ===');
  
  console.log('\n[1] Ensuring session...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  
  const client = new JoinQuantStrategyClient();
  
  console.log('\n[2] Getting strategy context...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('Strategy:', context.name);
  
  console.log('\n[3] Reading strategy code...');
  const code = fs.readFileSync(BASE_STRATEGY_FILE, 'utf8');
  console.log('Code length:', code.length, 'chars');
  
  console.log('\n[4] Saving strategy...');
  await client.saveStrategy(ALGORITHM_ID, 'RFScore7_PB10_Final_Test', code, context);
  console.log('Saved!');
  
  console.log('\n[5] Running backtest...');
  console.log(`Period: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, '', BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log('Backtest ID:', backtestId);
  
  console.log('\n[6] Polling for results (max 2 minutes)...');
  const startTime = Date.now();
  const maxWait = 120000;
  
  while (Date.now() - startTime < maxWait) {
    await new Promise(r => setTimeout(r, 5000));
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      
      if (result && result.results) {
        console.log('\n✓ BACKTEST COMPLETE!');
        console.log('='.repeat(60));
        const r = result.results;
        console.log(`Total Return: ${(r.total_returns * 100).toFixed(2)}%`);
        console.log(`Annual Return: ${(r.annualized_returns * 100).toFixed(2)}%`);
        console.log(`Sharpe: ${r.sharpe.toFixed(3)}`);
        console.log(`Max Drawdown: ${(r.max_drawdown * 100).toFixed(2)}%`);
        
        const outFile = path.join('data', `simple_test_${Date.now()}.json`);
        fs.writeFileSync(outFile, JSON.stringify(result, null, 2));
        console.log('\nSaved to:', outFile);
        return;
      }
      
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      console.log(`[${elapsed}s] Waiting...`);
    } catch (err) {
      console.log('Error:', err.message);
    }
  }
  
  console.log('\n⚠ Timeout after 2 minutes');
  console.log('Backtest may still be running on JoinQuant platform');
  console.log('Check manually: https://www.joinquant.com/algorithm/index/edit?algorithmId=' + ALGORITHM_ID);
}

main().catch(err => {
  console.error('Failed:', err);
  process.exit(1);
});