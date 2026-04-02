#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/rfscore7_pb10_optimized.py';
const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BACKTEST_CONFIG = {
  startTime: '2022-12-01',
  endTime: '2026-03-30',
  baseCapital: '1000000',
  frequency: 'day'
};

async function main() {
  console.log('RFScore7 PB10 优化策略回测');
  console.log('=' . repeat(60));
  
  console.log('\n[1/4] 确保 Session 有效...');
  const sessionResult = await ensureJoinQuantSession({
    headed: false,
    headless: true
  });
  console.log('Session 状态:', sessionResult.reason);
  
  const client = new JoinQuantStrategyClient();
  
  console.log('\n[2/4] 读取策略文件...');
  const code = fs.readFileSync(STRATEGY_FILE, 'utf8');
  console.log(`策略文件: ${STRATEGY_FILE}`);
  console.log(`代码长度: ${code.length} 字符`);
  
  console.log('\n[3/4] 获取策略上下文...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('策略名称:', context.name);
  console.log('用户ID:', context.userId);
  
  console.log('\n[4/4] 保存并运行回测...');
  const strategyName = 'RFScore7_PB10_Optimized_V2';
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
  console.log('策略已保存:', strategyName);
  
  console.log('\n开始回测...');
  console.log(`时间区间: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  console.log(`初始资金: ${BACKTEST_CONFIG.baseCapital}`);
  
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  
  console.log('\n等待回测完成...');
  let result = null;
  let retries = 0;
  const maxRetries = 30;
  
  while (retries < maxRetries) {
    await new Promise(resolve => setTimeout(resolve, 3000));
    result = await client.getBacktestResult(backtestId, context);
    
    if (result.status === 0 || result.status === '0') {
      console.log('回测完成！');
      break;
    }
    
    retries++;
    console.log(`等待中... (${retries}/${maxRetries})`);
  }
  
  if (retries >= maxRetries) {
    console.log('回测超时，获取日志...');
    const log = await client.getLog(backtestId);
    console.log('日志:', log);
  }
  
  console.log('\n回测结果:');
  console.log('=' . repeat(60));
  
  if (result && result.results) {
    const results = result.results;
    console.log(`年化收益: ${(results.annualized_returns * 100).toFixed(2)}%`);
    console.log(`累计收益: ${(results.total_returns * 100).toFixed(2)}%`);
    console.log(`夏普比率: ${results.sharpe.toFixed(3)}`);
    console.log(`最大回撤: ${(results.max_drawdown * 100).toFixed(2)}%`);
    console.log(`Alpha: ${(results.alpha * 100).toFixed(2)}%`);
    console.log(`Beta: ${results.beta.toFixed(3)}`);
  } else {
    console.log('无详细结果，保存完整响应');
  }
  
  console.log('\n完整结果已保存到 data/ 目录');
  
  const resultFile = path.join('data', `backtest_result_${Date.now()}.json`);
  fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
  console.log(`结果文件: ${resultFile}`);
}

main().catch(error => {
  console.error('执行失败:', error.message);
  process.exit(1);
});