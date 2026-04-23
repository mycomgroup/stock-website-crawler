#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';
const BACKTEST_ID = '534e1c6a1a4d918be370c69b6d2eea2c';

async function main() {
  console.log('=== Check Latest Backtest ===');
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  console.log('\nFetching result for:', BACKTEST_ID);
  const result = await client.getBacktestResult(BACKTEST_ID, context);
  
  console.log('State:', result?.data?.state);
  // state: 0=完成, 1=进行中, 2=等待中, 3=失败
  
  if (result?.data?.state === '0' || result?.data?.state === 0) {
    console.log('\n✓ BACKTEST COMPLETE!');
    const stats = await client.getBacktestStats(BACKTEST_ID, context);
    console.log(JSON.stringify(stats?.data, null, 2));
    
    const log = await client.getLog(BACKTEST_ID);
    if (log?.data?.logArr?.length > 0) {
      console.log('\nLog (first 10):');
      log.data.logArr.slice(0, 10).forEach(l => console.log(l.slice(0, 200)));
    }
  } else if (result?.data?.state === '3' || result?.data?.state === 3) {
    console.log('\n✗ BACKTEST FAILED');
    const log = await client.getLog(BACKTEST_ID);
    if (log?.data?.logArr?.length > 0) {
      console.log('\nError log:');
      log.data.logArr.forEach(l => console.log(l.slice(0, 500)));
    }
  } else {
    console.log('\n⏳ Still running or waiting');
    const log = await client.getLog(BACKTEST_ID);
    console.log('Log entries:', log?.data?.logArr?.length || 0);
  }
}

main().catch(console.error);