#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const OPTIMIZED_STRATEGY = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/rfscore7_pb10_optimized.py';
const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BACKTEST_CONFIG = {
  startTime: '2024-01-01',  // 只测试2024年，快速验证
  endTime: '2024-12-31',
  baseCapital: '1000000',
  frequency: 'day'
};

async function main() {
  console.log('RFScore7 PB10 优化策略 - 快速验证（2024年）');
  console.log('='.repeat(60));
  
  console.log('\n[1/5] 确保 Session 有效...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  console.log('\n[2/5] 读取优化策略...');
  const code = fs.readFileSync(OPTIMIZED_STRATEGY, 'utf8');
  console.log(`代码长度: ${code.length} 字符`);
  
  console.log('\n[3/5] 获取策略上下文...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log(`策略ID: ${ALGORITHM_ID}`);
  
  console.log('\n[4/5] 保存策略...');
  await client.saveStrategy(ALGORITHM_ID, 'RFScore7_PB10_Optimized_2024Test', code, context);
  console.log('策略已保存');
  
  console.log('\n[5/5] 运行回测...');
  console.log(`时间区间: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  console.log(`初始资金: ${BACKTEST_CONFIG.baseCapital}`);
  
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  
  console.log('\n等待回测完成（最多5分钟）...');
  let attempts = 0;
  const maxAttempts = 75; // 5分钟
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 4000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      
      if (result.status === 'error') {
        console.log('\n回测失败:', result.message);
        break;
      }
      
      if (result.data?.result?.summary) {
        const summary = result.data.result.summary;
        console.log('\n✓ 回测完成！\n');
        console.log('='.repeat(60));
        console.log('回测结果:');
        console.log('='.repeat(60));
        
        if (summary.annualized_returns !== undefined) {
          console.log(`年化收益: ${(summary.annualized_returns * 100).toFixed(2)}%`);
        }
        if (summary.total_returns !== undefined) {
          console.log(`累计收益: ${(summary.total_returns * 100).toFixed(2)}%`);
        }
        if (summary.sharpe !== undefined) {
          console.log(`夏普比率: ${summary.sharpe.toFixed(3)}`);
        }
        if (summary.max_drawdown !== undefined) {
          console.log(`最大回撤: ${(summary.max_drawdown * 100).toFixed(2)}%`);
        }
        if (summary.alpha !== undefined) {
          console.log(`Alpha: ${(summary.alpha * 100).toFixed(2)}%`);
        }
        if (summary.beta !== undefined) {
          console.log(`Beta: ${summary.beta.toFixed(3)}`);
        }
        if (summary.win_rate !== undefined) {
          console.log(`胜率: ${(summary.win_rate * 100).toFixed(1)}%`);
        }
        
        const resultFile = path.join('data', `backtest_2024_${Date.now()}.json`);
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        console.log(`\n完整结果已保存: ${resultFile}`);
        
        return;
      }
      
      if (attempts % 10 === 0) {
        console.log(`  等待中... ${Math.floor(attempts * 4 / 60)}分钟`);
      }
    } catch (error) {
      if (attempts % 10 === 0) {
        console.log(`  等待中... ${Math.floor(attempts * 4 / 60)}分钟`);
      }
    }
  }
  
  console.log('\n⚠ 回测超时');
  console.log('\n请手动访问网页查看结果:');
  console.log(`https://www.joinquant.com/algorithm/index/edit?algorithmId=${ALGORITHM_ID}`);
}

main().catch(error => {
  console.error('执行失败:', error.message);
  process.exit(1);
});