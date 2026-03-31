#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGIES = [
  {
    name: 'A_PureSmallCap',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/attribution_a_pure_smallcap.py',
    desc: '纯小市值因子：流通市值最小前10%，月度调仓，持仓20只'
  },
  {
    name: 'B_SmallCapEvent',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/attribution_b_smallcap_event.py',
    desc: '小市值+事件：市值5-15亿+首板低开，次日退出，持仓1只'
  },
  {
    name: 'C_PureEvent',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/attribution_c_pure_event.py',
    desc: '纯事件：全市场首板低开，次日退出，持仓1只'
  }
];

const BACKTEST_CONFIG = {
  startTime: '2022-01-01',
  endTime: '2025-03-30',
  baseCapital: '100000',
  frequency: 'day'
};

async function runSingleBacktest(client, context, strategy, index) {
  console.log(`\n=== [${index + 1}/${STRATEGIES.length}] ${strategy.name} ===`);
  console.log(`策略描述: ${strategy.desc}`);
  
  const code = fs.readFileSync(strategy.file, 'utf8');
  
  const strategyName = `Attribution_${strategy.name}_${Date.now()}`;
  console.log(`更新策略名称: ${strategyName}`);
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
  
  console.log(`开始回测: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
  
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  
  console.log('等待回测完成...');
  let attempts = 0;
  const maxAttempts = 60;
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};
      
      process.stdout.write(`\r[${attempts}/${maxAttempts}] 状态: ${bt.status}, 进度: ${bt.progress || 0}%`);
      
      if (result.status === 'error') {
        console.log('\n❌ 回测失败:', result.message);
        return { success: false, error: result.message, strategy: strategy.name };
      }
      
      if (bt.finished_time || bt.status === 'finished') {
        console.log('\n✓ 回测完成!');
        
        const summary = result.data?.result?.summary || {};
        
        return {
          success: true,
          strategy: strategy.name,
          desc: strategy.desc,
          backtestId,
          summary: {
            totalReturn: summary.total_returns || 0,
            annualReturn: summary.annual_returns || 0,
            sharpe: summary.sharpe || 0,
            maxDrawdown: summary.max_drawdown || 0,
            winRate: summary.win_rate || 0,
            tradeCount: summary.trade_count || 0,
            benchmarkReturn: summary.benchmark_return || 0
          }
        };
      }
      
      if (bt.status === 'failed') {
        console.log('\n❌ 服务器端回测失败');
        return { success: false, error: 'Server failed', strategy: strategy.name };
      }
    } catch (err) {
      console.log('\n⚠️  轮询结果出错:', err.message);
    }
  }
  
  console.log('\n⏱️  回测超时');
  return { success: false, error: 'Timeout', strategy: strategy.name };
}

async function main() {
  console.log('========================================');
  console.log('小市值因子 vs 事件策略归因分析');
  console.log('========================================');
  console.log('策略数量:', STRATEGIES.length);
  console.log('回测期间:', BACKTEST_CONFIG.startTime, '~', BACKTEST_CONFIG.endTime);
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('目标策略:', context.name);
  
  const results = [];
  
  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);
    
    if (result.success) {
      console.log(`\n✓ ${result.strategy} 完成`);
      console.log(`  总收益: ${result.summary.totalReturn}%`);
      console.log(`  年化收益: ${result.summary.annualReturn}%`);
      console.log(`  夏普比率: ${result.summary.sharpe}`);
      console.log(`  最大回撤: ${result.summary.maxDrawdown}%`);
      console.log(`  胜率: ${result.summary.winRate}%`);
      console.log(`  交易次数: ${result.summary.tradeCount}`);
    } else {
      console.log(`\n✗ ${result.strategy} 失败: ${result.error}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
  
  console.log('\n\n========================================');
  console.log('归因分析汇总');
  console.log('========================================');
  console.log('成功:', results.filter(r => r.success).length);
  console.log('失败:', results.filter(r => !r.success).length);
  
  const successful = results.filter(r => r.success);
  if (successful.length > 0) {
    console.log('\n策略对比表:');
    console.log('-'.repeat(100));
    console.log('策略              | 总收益    | 年化收益  | 夏普   | 最大回撤  | 胜率    | 交易次数');
    console.log('-'.repeat(100));
    
    for (const s of successful) {
      const sum = s.summary;
      console.log(
        `${s.strategy.padEnd(17)} | ${(sum.totalReturn || 0).toFixed(2).padStart(7)}% | ${(sum.annualReturn || 0).toFixed(2).padStart(7)}% | ${(sum.sharpe || 0).toFixed(2).padStart(5)} | ${(sum.maxDrawdown || 0).toFixed(2).padStart(7)}% | ${(sum.winRate || 0).toFixed(1).padStart(5)}% | ${(sum.tradeCount || 0).toString().padStart(7)}`
      );
    }
    
    console.log('-'.repeat(100));
    
    if (successful.length === 3) {
      const a = successful.find(s => s.strategy === 'A_PureSmallCap').summary;
      const b = successful.find(s => s.strategy === 'B_SmallCapEvent').summary;
      const c = successful.find(s => s.strategy === 'C_PureEvent').summary;
      
      console.log('\n收益归因分解:');
      console.log('-'.repeat(60));
      console.log('因子收益 (策略A):', (a.totalReturn || 0).toFixed(2), '%');
      console.log('事件收益 (策略C):', (c.totalReturn || 0).toFixed(2), '%');
      console.log('组合收益 (策略B):', (b.totalReturn || 0).toFixed(2), '%');
      
      const interactionReturn = (b.totalReturn || 0) - (a.totalReturn || 0) - (c.totalReturn || 0);
      console.log('交互收益 (B-A-C):', interactionReturn.toFixed(2), '%');
      
      console.log('\n归因占比:');
      const totalAbs = Math.abs(a.totalReturn || 0) + Math.abs(c.totalReturn || 0) + Math.abs(interactionReturn);
      if (totalAbs > 0) {
        const factorPct = Math.abs(a.totalReturn || 0) / totalAbs * 100;
        const eventPct = Math.abs(c.totalReturn || 0) / totalAbs * 100;
        const interactionPct = Math.abs(interactionReturn) / totalAbs * 100;
        
        console.log(`  因子收益占比: ${factorPct.toFixed(1)}%`);
        console.log(`  事件收益占比: ${eventPct.toFixed(1)}%`);
        console.log(`  交互收益占比: ${interactionPct.toFixed(1)}%`);
        
        if (factorPct > 60) {
          console.log('\n策略本质判定: 因子驱动 (因子占比 > 60%)');
        } else if (eventPct > 60) {
          console.log('\n策略本质判定: 事件驱动 (事件占比 > 60%)');
        } else if (interactionReturn > 0) {
          console.log('\n策略本质判定: 混合驱动 (两者均显著，交互收益为正)');
        } else {
          console.log('\n策略本质判定: 混合驱动 (两者均显著，但交互收益为负)');
        }
      }
    }
  }
  
  const outputDir = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/output';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const outputPath = path.join(outputDir, `attribution-backtest-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\n结果已保存至:', outputPath);
}

main().catch(err => {
  console.error('批量回测失败:', err);
  process.exit(1);
});