#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

// 分阶段验证配置
const BACKTEST_STAGES = [
  {
    name: '阶段1-快速验证(2024Q4)',
    config: {
      startTime: '2024-10-01',
      endTime: '2024-12-31',
      baseCapital: '1000000',
      frequency: 'day'
    }
  },
  {
    name: '阶段2-半年验证(2024H2)',
    config: {
      startTime: '2024-07-01',
      endTime: '2024-12-31',
      baseCapital: '1000000',
      frequency: 'day'
    }
  },
  {
    name: '阶段3-完整验证(2022-2026)',
    config: {
      startTime: '2022-12-01',
      endTime: '2026-03-30',
      baseCapital: '1000000',
      frequency: 'day'
    }
  }
];

async function runBacktest(client, context, stage, index) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`${stage.name}`);
  console.log('='.repeat(60));
  console.log(`时间区间: ${stage.config.startTime} ~ ${stage.config.endTime}`);
  
  try {
    const buildResult = await client.runBacktest(
      ALGORITHM_ID,
      '',
      stage.config,
      context
    );
    
    const backtestId = buildResult.backtestId;
    console.log(`回测ID: ${backtestId}`);
    console.log(`回测链接: https://www.joinquant.com/algorithm/backtest?backtestId=${backtestId}`);
    
    console.log('\n等待回测完成...');
    let attempts = 0;
    const maxAttempts = 90; // 6分钟
    
    while (attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 4000));
      attempts++;
      
      const result = await client.getBacktestResult(backtestId, context);
      
      if (result.status === 'error') {
        console.log('\n✗ 回测失败:', result.message);
        return { success: false, error: result.message };
      }
      
      if (result.data?.result?.summary) {
        const summary = result.data.result.summary;
        console.log('\n✓ 回测完成！\n');
        console.log('回测结果:');
        console.log('-'.repeat(60));
        
        const metrics = [];
        if (summary.annualized_returns !== undefined) {
          metrics.push(`年化收益: ${(summary.annualized_returns * 100).toFixed(2)}%`);
        }
        if (summary.total_returns !== undefined) {
          metrics.push(`累计收益: ${(summary.total_returns * 100).toFixed(2)}%`);
        }
        if (summary.sharpe !== undefined) {
          metrics.push(`夏普比率: ${summary.sharpe.toFixed(3)}`);
        }
        if (summary.max_drawdown !== undefined) {
          metrics.push(`最大回撤: ${(summary.max_drawdown * 100).toFixed(2)}%`);
        }
        if (summary.alpha !== undefined) {
          metrics.push(`Alpha: ${(summary.alpha * 100).toFixed(2)}%`);
        }
        if (summary.beta !== undefined) {
          metrics.push(`Beta: ${summary.beta.toFixed(3)}`);
        }
        
        metrics.forEach(m => console.log(`  ${m}`));
        
        // 保存结果
        const resultFile = path.join('data', `backtest_stage${index + 1}_${Date.now()}.json`);
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        console.log(`\n完整结果: ${resultFile}`);
        
        return { success: true, summary, backtestId };
      }
      
      if (attempts % 15 === 0) {
        console.log(`  等待中... ${Math.floor(attempts * 4 / 60)}分钟`);
      }
    }
    
    console.log('\n⚠ 回测超时，请手动查看:');
    console.log(`https://www.joinquant.com/algorithm/backtest?backtestId=${backtestId}`);
    return { success: false, timeout: true, backtestId };
    
  } catch (error) {
    console.log(`\n✗ 执行失败: ${error.message}`);
    return { success: false, error: error.message };
  }
}

async function main() {
  console.log('RFScore7 PB10 优化策略 - 分阶段验证');
  console.log('='.repeat(60));
  
  console.log('\n[准备] 验证 Session...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  console.log('\n[准备] 获取策略上下文...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log(`策略ID: ${ALGORITHM_ID}`);
  console.log(`策略名称: ${context.name}`);
  
  const results = [];
  
  // 运行阶段1（快速验证）
  for (let i = 0; i < 1; i++) {  // 先只运行第一阶段
    const result = await runBacktest(client, context, BACKTEST_STAGES[i], i);
    results.push({ stage: BACKTEST_STAGES[i].name, ...result });
    
    if (result.success) {
      console.log('\n✓ 验证成功，可以继续下一阶段');
    } else {
      console.log('\n✗ 验证失败，请检查策略');
      break;
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('验证汇总');
  console.log('='.repeat(60));
  
  results.forEach((r, i) => {
    console.log(`\n${r.stage}:`);
    if (r.success) {
      console.log('  状态: ✓ 成功');
      if (r.summary) {
        console.log(`  年化收益: ${(r.summary.annualized_returns * 100).toFixed(2)}%`);
        console.log(`  夏普比率: ${r.summary.sharpe.toFixed(3)}`);
      }
    } else {
      console.log(`  状态: ✗ 失败 (${r.error || '超时'})`);
    }
  });
}

main().catch(error => {
  console.error('执行失败:', error.message);
  process.exit(1);
});