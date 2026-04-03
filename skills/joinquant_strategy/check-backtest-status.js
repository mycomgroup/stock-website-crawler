#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const BACKTEST_ID = 'e87056050dfd8274b3a4e6e2692e7b5b';
const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

async function main() {
  console.log('检查回测状态');
  console.log('='.repeat(60));
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  console.log('\n回测信息:');
  console.log(`  回测ID: ${BACKTEST_ID}`);
  console.log(`  回测链接: https://www.joinquant.com/algorithm/backtest?backtestId=${BACKTEST_ID}`);
  
  console.log('\n获取回测结果...');
  const context = await client.getStrategyContext(ALGORITHM_ID);
  const result = await client.getBacktestResult(BACKTEST_ID, context);
  
  console.log('\n回测状态:');
  console.log(`  status: ${result.status}`);
  console.log(`  code: ${result.code}`);
  console.log(`  msg: ${result.msg}`);
  
  if (result.data) {
    console.log('\n数据结构:');
    console.log(`  data.state: ${result.data.state}`);
    
    if (result.data.result) {
      console.log('\n结果结构:');
      const keys = Object.keys(result.data.result);
      console.log(`  可用字段: ${keys.join(', ')}`);
      
      if (result.data.result.summary) {
        const summary = result.data.result.summary;
        console.log('\n✓ 找到回测结果！');
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
        
        // 保存完整结果
        const resultFile = path.join('data', `backtest_result_${Date.now()}.json`);
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        console.log(`\n完整结果已保存: ${resultFile}`);
      } else {
        console.log('\n⚠ 未找到 summary 字段');
        console.log('result.data.result 字段:', JSON.stringify(result.data.result, null, 2).slice(0, 500));
      }
    }
  }
  
  // 获取日志
  console.log('\n获取回测日志...');
  try {
    const log = await client.getLog(BACKTEST_ID);
    if (log.data && log.data.logArr) {
      console.log(`日志条数: ${log.data.logArr.length}`);
      console.log('\n最近日志:');
      log.data.logArr.slice(-5).forEach(line => {
        console.log(`  ${line}`);
      });
    }
  } catch (error) {
    console.log(`获取日志失败: ${error.message}`);
  }
}

main().catch(console.error);