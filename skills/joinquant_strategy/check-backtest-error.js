#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const BACKTEST_ID = 'd9d98d32ae03a370535215858b835f7c';
const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

async function main() {
  console.log('检查回测错误日志\n');
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  console.log('回测ID:', BACKTEST_ID);
  console.log('回测链接:', `https://www.joinquant.com/algorithm/backtest?backtestId=${BACKTEST_ID}`);
  
  console.log('\n获取日志...');
  const log = await client.getLog(BACKTEST_ID);
  
  if (log.data && log.data.logArr) {
    console.log(`\n日志条数: ${log.data.logArr.length}`);
    console.log('\n完整日志:');
    log.data.logArr.forEach((line, i) => {
      console.log(`${i + 1}. ${line}`);
    });
  } else {
    console.log('无日志数据');
    console.log(JSON.stringify(log, null, 2));
  }
}

main().catch(console.error);