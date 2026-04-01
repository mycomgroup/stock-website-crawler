#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGIES = [
  {
    name: '有路由器',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/state_router_v1_minimal.py',
    description: '状态路由器v1极简版 - 仅测试核心逻辑'
  },
  {
    name: '无路由器',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/state_router_baseline.py',
    description: '基准版本 - 始终满仓沪深300'
  }
];

const BACKTEST_CONFIG = {
  startTime: '2022-01-01',
  endTime: '2024-12-31',
  baseCapital: '100000',
  frequency: 'day'
};

async function runSingleBacktest(client, context, strategy, index) {
  console.log(`\n=== ${strategy.name} (${index + 1}/${STRATEGIES.length}) ===`);
  
  const code = fs.readFileSync(strategy.file, 'utf8');
  
  const strategyName = `状态路由器对比_${strategy.name}`;
  console.log(`上传策略: ${strategyName}`);
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
  
  console.log(`回测区间: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
  
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  
  console.log('等待回测完成...');
  let attempts = 0;
  const maxAttempts = 120;
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 3000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};
      
      if (attempts % 10 === 0) {
        console.log(`[${attempts}/${maxAttempts}] 进度: ${bt.progress || 0}%`);
      }
      
      if (result.status === 'error') {
        console.log('\n回测失败:', result.message);
        return { success: false, error: result.message, name: strategy.name };
      }
      
      if (bt.finished_time || bt.status === 'finished') {
        console.log('\n回测完成!');
        
        const summary = result.data?.result?.summary || {};
        
        return {
          success: true,
          name: strategy.name,
          backtestId,
          summary: {
            totalReturn: summary.total_returns || 0,
            annualReturn: summary.annual_returns || 0,
            sharpe: summary.sharpe || 0,
            maxDrawdown: summary.max_drawdown || 0,
            winRate: summary.win_rate || 0,
            tradeCount: summary.trade_count || 0,
            benchmarkReturn: summary.benchmark_returns || 0
          }
        };
      }
      
      if (bt.status === 'failed') {
        console.log('\n服务器端失败');
        return { success: false, error: 'Server failed', name: strategy.name };
      }
    } catch (err) {
      if (attempts % 10 === 0) {
        console.log(`查询错误: ${err.message.slice(0, 50)}`);
      }
    }
  }
  
  console.log('\n超时');
  return { success: false, error: 'Timeout', name: strategy.name };
}

async function main() {
  console.log('='.repeat(60));
  console.log('状态路由器 v1 对比回测');
  console.log('='.repeat(60));
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  const results = [];
  
  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);
    
    if (result.success) {
      console.log(`\n✓ ${result.name} 完成`);
      console.log(`  总收益: ${result.summary.totalReturn.toFixed(2)}%`);
      console.log(`  年化收益: ${result.summary.annualReturn.toFixed(2)}%`);
      console.log(`  夏普比率: ${result.summary.sharpe.toFixed(2)}`);
      console.log(`  最大回撤: ${result.summary.maxDrawdown.toFixed(2)}%`);
    } else {
      console.log(`\n✗ ${result.name} 失败: ${result.error}`);
    }
    
    if (i < STRATEGIES.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }
  
  console.log('\n\n' + '='.repeat(60));
  console.log('对比结果');
  console.log('='.repeat(60));
  
  const successful = results.filter(r => r.success);
  
  if (successful.length === 2) {
    console.log('\n指标对比表:');
    console.log('-'.repeat(80));
    console.log('指标            | 有路由器  | 无路由器  | 差异       | 改善幅度');
    console.log('-'.repeat(80));
    
    const withRouter = successful.find(r => r.name === '有路由器').summary;
    const withoutRouter = successful.find(r => r.name === '无路由器').summary;
    
    const totalDiff = withRouter.totalReturn - withoutRouter.totalReturn;
    const annualDiff = withRouter.annualReturn - withoutRouter.annualReturn;
    const sharpeDiff = withRouter.sharpe - withoutRouter.sharpe;
    const ddDiff = withRouter.maxDrawdown - withoutRouter.maxDrawdown;
    const ddImprove = withoutRouter.maxDrawdown > 0 ? 
      ((withoutRouter.maxDrawdown - withRouter.maxDrawdown) / withoutRouter.maxDrawdown * 100) : 0;
    
    console.log(`总收益          | ${withRouter.totalReturn.toFixed(2).padStart(8)}% | ${withoutRouter.totalReturn.toFixed(2).padStart(8)}% | ${totalDiff.toFixed(2).padStart(8)}% |`);
    console.log(`年化收益        | ${withRouter.annualReturn.toFixed(2).padStart(8)}% | ${withoutRouter.annualReturn.toFixed(2).padStart(8)}% | ${annualDiff.toFixed(2).padStart(8)}% |`);
    console.log(`夏普比率        | ${withRouter.sharpe.toFixed(2).padStart(8)}  | ${withoutRouter.sharpe.toFixed(2).padStart(8)}  | ${sharpeDiff.toFixed(2).padStart(8)}  |`);
    console.log(`最大回撤        | ${withRouter.maxDrawdown.toFixed(2).padStart(8)}% | ${withoutRouter.maxDrawdown.toFixed(2).padStart(8)}% | ${ddDiff.toFixed(2).padStart(8)}% | ${ddImprove.toFixed(1).padStart(6)}%`);
    
    console.log('\n关键问题回答:');
    console.log('-'.repeat(60));
    
    if (ddImprove > 20) {
      console.log(`✓ 问题1: 路由器能否显著降低回撤？YES - 回撤降低 ${ddImprove.toFixed(1)}% (>20%门槛)`);
    } else {
      console.log(`✗ 问题1: 路由器能否显著降低回撤？NO - 回撤降低 ${ddImprove.toFixed(1)}% (<20%门槛)`);
    }
    
    const annCost = Math.abs(annualDiff) / Math.abs(withoutRouter.annualReturn) * 100;
    if (annCost < 20) {
      console.log(`✓ 问题2: 是否牺牲过多收益？NO - 收益差异 ${annCost.toFixed(1)}% (<20%门槛)`);
    } else {
      console.log(`✗ 问题2: 是否牺牲过多收益？YES - 收益差异 ${annCost.toFixed(1)}% (>20%门槛)`);
    }
    
    if (ddImprove > 20 && annCost < 20) {
      console.log('\n最终结论: Go - 状态路由器有效');
    } else if (ddImprove > 20 || annCost < 20) {
      console.log('\n最终结论: Watch - 需进一步验证');
    } else {
      console.log('\n最终结论: No-Go - 效果不佳');
    }
  } else {
    console.log('\n警告: 回测未全部成功，无法对比');
    for (const r of results) {
      console.log(`  ${r.name}: ${r.success ? '成功' : '失败 - ' + r.error}`);
    }
  }
  
  const outputPath = path.join(client.outputRoot, `state-router-comparison-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\n结果保存至:', outputPath);
}

main().catch(err => {
  console.error('对比回测失败:', err);
  process.exit(1);
});