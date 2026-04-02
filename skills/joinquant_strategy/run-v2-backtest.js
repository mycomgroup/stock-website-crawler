#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '801d56e162b037ed1a6e0ba5d26ff092'; // rfscore7_pb10_final_v2.py

const BACKTEST_CONFIG = {
  startTime: '2022-12-01',
  endTime: '2026-03-30',
  baseCapital: '1000000',
  frequency: 'day'
};

async function main() {
  console.log('RFScore7 PB10 原版策略回测');
  console.log('=' . repeat(60));
  
  console.log('\n[1/3] 确保 Session 有效...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  
  const client = new JoinQuantStrategyClient();
  
  console.log('\n[2/3] 获取策略上下文...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('策略名称:', context.name);
  console.log('用户ID:', context.userId);
  
  console.log('\n[3/3] 运行回测...');
  console.log(`时间区间: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  console.log(`初始资金: ${BACKTEST_CONFIG.baseCapital}`);
  
  const buildResult = await client.runBacktest(ALGORITHM_ID, '', BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  
  console.log('\n等待回测完成...');
  let result = null;
  let retries = 0;
  const maxRetries = 60;
  
  while (retries < maxRetries) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    result = await client.getBacktestResult(backtestId, context);
    
    if (result && result.results) {
      console.log('回测完成！');
      break;
    }
    
    retries++;
    if (retries % 10 === 0) {
      console.log(`等待中... (${retries}/${maxRetries})`);
    }
  }
  
  if (result && result.results) {
    console.log('\n回测结果:');
    console.log('=' . repeat(60));
    const r = result.results;
    console.log(`年化收益: ${(r.annualized_returns * 100).toFixed(2)}%`);
    console.log(`累计收益: ${(r.total_returns * 100).toFixed(2)}%`);
    console.log(`夏普比率: ${r.sharpe.toFixed(3)}`);
    console.log(`最大回撤: ${(r.max_drawdown * 100).toFixed(2)}%`);
    console.log(`Alpha: ${(r.alpha * 100).toFixed(2)}%`);
    console.log(`Beta: ${r.beta.toFixed(3)}`);
    console.log(`胜率: ${(r.win_rate * 100).toFixed(1)}%`);
    
    const resultFile = path.join('data', `rfscore7_v2_backtest_${Date.now()}.json`);
    fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
    console.log(`\n完整结果已保存: ${resultFile}`);
  } else {
    console.log('\n获取日志...');
    const log = await client.getLog(backtestId);
    console.log('日志:', JSON.stringify(log, null, 2).slice(0, 500));
    
    const resultFile = path.join('data', `backtest_log_${Date.now()}.json`);
    fs.writeFileSync(resultFile, JSON.stringify({ result, log }, null, 2));
    console.log(`日志已保存: ${resultFile}`);
  }
}

main().catch(console.error);