#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const STRATEGIES = [
  {
    name: '原版_final_v2',
    algorithmId: '801d56e162b037ed1a6e0ba5d26ff092',
    file: null, // 使用已有策略
  },
  {
    name: '优化版_optimized_v2',
    algorithmId: '309ebf2421687fcf4d41223fdec01f2c',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/rfscore7_pb10_optimized.py',
  }
];

const BACKTEST_CONFIG = {
  startTime: '2022-12-01',
  endTime: '2026-03-30',
  baseCapital: '1000000',
  frequency: 'day'
};

async function runBacktestForStrategy(client, strategy) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`策略: ${strategy.name}`);
  console.log('='.repeat(60));
  
  const context = await client.getStrategyContext(strategy.algorithmId);
  
  if (strategy.file) {
    console.log('上传优化策略...');
    const code = fs.readFileSync(strategy.file, 'utf8');
    await client.saveStrategy(strategy.algorithmId, `RFScore7_PB10_${strategy.name}`, code, context);
  }
  
  console.log(`运行回测: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(strategy.algorithmId, '', BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  
  console.log('等待回测完成...');
  let result = null;
  let retries = 0;
  const maxRetries = 90; // 3分钟
  
  while (retries < maxRetries) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    result = await client.getBacktestResult(backtestId, context);
    
    if (result && result.results) {
      console.log('✓ 回测完成！');
      return result;
    }
    
    retries++;
    if (retries % 15 === 0) {
      console.log(`  等待中... ${Math.floor(retries * 2 / 60)}分钟`);
    }
  }
  
  console.log('⚠ 回测超时，获取当前状态...');
  const log = await client.getLog(backtestId);
  return { log, timeout: true };
}

async function main() {
  console.log('RFScore7 PB10 策略对比回测');
  console.log('='.repeat(60));
  console.log(`回测区间: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  console.log(`初始资金: ${BACKTEST_CONFIG.baseCapital}`);
  
  console.log('\n[准备] 确保 Session 有效...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  const results = {};
  
  for (const strategy of STRATEGIES) {
    try {
      const result = await runBacktestForStrategy(client, strategy);
      results[strategy.name] = result;
      
      if (result.results) {
        const r = result.results;
        console.log('\n回测结果:');
        console.log(`  年化收益: ${(r.annualized_returns * 100).toFixed(2)}%`);
        console.log(`  累计收益: ${(r.total_returns * 100).toFixed(2)}%`);
        console.log(`  夏普比率: ${r.sharpe.toFixed(3)}`);
        console.log(`  最大回撤: ${(r.max_drawdown * 100).toFixed(2)}%`);
        console.log(`  Alpha: ${(r.alpha * 100).toFixed(2)}%`);
        console.log(`  Beta: ${r.beta.toFixed(3)}`);
      }
    } catch (error) {
      console.error(`策略 ${strategy.name} 执行失败:`, error.message);
      results[strategy.name] = { error: error.message };
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('对比汇总');
  console.log('='.repeat(60));
  
  const summaryFile = path.join('data', `comparison_${Date.now()}.json`);
  fs.writeFileSync(summaryFile, JSON.stringify(results, null, 2));
  console.log(`\n完整结果已保存: ${summaryFile}`);
}

main().catch(console.error);