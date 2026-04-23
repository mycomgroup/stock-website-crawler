#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';
const BACKTEST_ID = '534e1c6a1a4d918be370c69b6d2eea2c';

async function main() {
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  const log = await client.getLog(BACKTEST_ID);
  const logs = log?.data?.logArr || [];
  
  console.log('Total log entries:', logs.length);
  console.log('\n=== Last 20 log entries ===');
  logs.slice(-20).forEach(l => console.log(l));
  
  // Check for errors
  const errors = logs.filter(l => l.includes('ERROR'));
  if (errors.length > 0) {
    console.log('\n=== ERRORS ===');
    errors.forEach(l => console.log(l.slice(0, 500)));
  }
}

main().catch(console.error);