#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_IDS = {
  'original_v2': '801d56e162b037ed1a6e0ba5d26ff092',
  'optimized_v2': '309ebf2421687fcf4d41223fdec01f2c'
};

async function getLatestBacktestResults() {
  console.log('获取最新回测结果\n');
  console.log('='.repeat(60));
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  for (const [name, algorithmId] of Object.entries(ALGORITHM_IDS)) {
    console.log(`\n${name}:`);
    console.log('-'.repeat(60));
    console.log(`策略ID: ${algorithmId}`);
    console.log(`网页链接: https://www.joinquant.com/algorithm/index/edit?algorithmId=${algorithmId}`);
    
    try {
      const context = await client.getStrategyContext(algorithmId);
      console.log(`策略名称: ${context.name}`);
      
      const backtests = await client.getBacktests(algorithmId);
      console.log(`回测记录数: ${backtests.length}`);
      
      if (backtests.length > 0) {
        const latest = backtests[0];
        console.log(`\n最新回测:`);
        console.log(`  ID: ${latest.backtestId}`);
        console.log(`  时间: ${latest.time}`);
        console.log(`  状态: ${latest.state}`);
        
        const result = await client.getBacktestResult(latest.backtestId, context);
        
        if (result.data?.result?.summary) {
          const summary = result.data.result.summary;
          console.log('\n  回测指标:');
          if (summary.annualized_returns !== undefined) {
            console.log(`    年化收益: ${(summary.annualized_returns * 100).toFixed(2)}%`);
          }
          if (summary.total_returns !== undefined) {
            console.log(`    累计收益: ${(summary.total_returns * 100).toFixed(2)}%`);
          }
          if (summary.sharpe !== undefined) {
            console.log(`    夏普比率: ${summary.sharpe.toFixed(3)}`);
          }
          if (summary.max_drawdown !== undefined) {
            console.log(`    最大回撤: ${(summary.max_drawdown * 100).toFixed(2)}%`);
          }
          if (summary.alpha !== undefined) {
            console.log(`    Alpha: ${(summary.alpha * 100).toFixed(2)}%`);
          }
          if (summary.beta !== undefined) {
            console.log(`    Beta: ${summary.beta.toFixed(3)}`);
          }
          if (summary.win_rate !== undefined) {
            console.log(`    胜率: ${(summary.win_rate * 100).toFixed(1)}%`);
          }
        } else {
          console.log('  未找到详细结果');
        }
      }
    } catch (error) {
      console.log(`  错误: ${error.message}`);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('\n💡 提示：如需运行新回测，请访问上述网页链接');
}

getLatestBacktestResults().catch(console.error);