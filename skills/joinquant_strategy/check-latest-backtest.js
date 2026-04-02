#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

async function main() {
  console.log('获取最近的回测结果...\n');
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  console.log('获取回测列表...');
  const backtests = await client.getBacktests(ALGORITHM_ID);
  
  console.log(`找到 ${backtests.length} 个回测记录\n`);
  
  if (backtests.length > 0) {
    const latest = backtests[0];
    console.log('最新回测:');
    console.log(`  ID: ${latest.backtestId}`);
    console.log(`  名称: ${latest.name}`);
    console.log(`  时间: ${latest.time}`);
    console.log(`  状态: ${latest.state}`);
    
    console.log('\n获取详细结果...');
    const result = await client.getBacktestResult(latest.backtestId, context);
    
    if (result.results) {
      console.log('\n回测结果:');
      console.log('=' . repeat(60));
      const r = result.results;
      console.log(`年化收益: ${(r.annualized_returns * 100).toFixed(2)}%`);
      console.log(`累计收益: ${(r.total_returns * 100).toFixed(2)}%`);
      console.log(`夏普比率: ${r.sharpe.toFixed(3)}`);
      console.log(`最大回撤: ${(r.max_drawdown * 100).toFixed(2)}%`);
    } else {
      console.log('\n结果结构:');
      console.log(JSON.stringify(result, null, 2).slice(0, 500));
    }
    
    console.log('\n获取日志...');
    const log = await client.getLog(latest.backtestId);
    console.log('\n日志 (前1000字符):');
    console.log(JSON.stringify(log, null, 2).slice(0, 1000));
    
    const resultFile = path.join('data', `latest_backtest_${Date.now()}.json`);
    fs.writeFileSync(resultFile, JSON.stringify({ result, log }, null, 2));
    console.log(`\n完整结果已保存: ${resultFile}`);
  }
}

main().catch(console.error);