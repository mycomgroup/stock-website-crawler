#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';
const BACKTEST_ID = 'f52307c6e526434e65d5a99b3e0e27ce';

async function main() {
  console.log('=== Get Backtest Result Directly ===');
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  console.log('\nFetching result for:', BACKTEST_ID);
  const result = await client.getBacktestResult(BACKTEST_ID, context);
  
  console.log('\nResult structure:');
  console.log(JSON.stringify(result, null, 2).slice(0, 2000));
  
  console.log('\nFetching log:');
  const log = await client.getLog(BACKTEST_ID);
  console.log('Log lines:', log?.data?.logArr?.length || 0);
  if (log?.data?.logArr?.length > 0) {
    console.log('First 5 log entries:');
    log.data.logArr.slice(0, 5).forEach(l => console.log(l));
  }
  
  console.log('\nFetching stats:');
  const stats = await client.getBacktestStats(BACKTEST_ID, context);
  console.log(JSON.stringify(stats, null, 2).slice(0, 1000));
}

main().catch(console.error);