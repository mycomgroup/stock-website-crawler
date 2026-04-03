#!/usr/bin/env node

/**
 * 获取RFScore策略回测结果
 */

import fs from 'node:fs';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const backtestIds = {
  'rfscore7_pb10_final_v2': '0db2a65f73983ffdef8de5aa89f2ca3a',
  'rfscore7_pb10_release_v1': 'dc592d1ba64acf6a905f5f87073b19bf',
  'rfscore_defensive_combined': '3485c8bb3282df192e9cb0eaa4f841bb',
  'rfscore7_pb10_enhanced_selection': '12b1f52ce8c011eacd22383df009367a',
  'rfscore7_pb10_multi_signal_risk_control': 'f4cbd9181c473d73dde0f781b70dfbe4',
  'rfscore_defensive_dynamic_hedge': '59438eac66db9d145104b70066bdb2b8'
};

const strategies = [
  { key: 'rfscore7_pb10_final_v2', name: 'V2原版', file: 'rfscore7_pb10_final_v2.py' },
  { key: 'rfscore7_pb10_release_v1', name: 'Release V1', file: 'rfscore7_pb10_release_v1.py' },
  { key: 'rfscore_defensive_combined', name: 'Defensive原版', file: 'rfscore_defensive_combined.py' },
  { key: 'rfscore7_pb10_enhanced_selection', name: '增强选股版', file: 'rfscore7_pb10_enhanced_selection.py' },
  { key: 'rfscore7_pb10_multi_signal_risk_control', name: '多信号风控版', file: 'rfscore7_pb10_multi_signal_risk_control.py' },
  { key: 'rfscore_defensive_dynamic_hedge', name: '动态对冲版', file: 'rfscore_defensive_dynamic_hedge.py' }
];

async function fetchResults() {
  console.log('正在获取RFScore策略回测结果...\n');
  
  // 确保session
  await ensureJoinQuantSession({});
  const client = new JoinQuantStrategyClient({});
  
  // 从session文件获取context
  const sessionPath = './data/session.json';
  const session = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));
  const context = { cookies: session.cookies };
  
  const results = [];
  
  for (const strategy of strategies) {
    const backtestId = backtestIds[strategy.key];
    console.log(`\n${strategy.name}:`);
    console.log(`  回测ID: ${backtestId}`);
    
    try {
      // 获取回测结果
      const result = await client.getBacktestResult(backtestId, context);
      
      if (result.data?.result?.backtest?.status === 'finished' || 
          result.data?.backtest?.status === 'finished') {
        
        // 获取完整报告
        console.log('  状态: 已完成，获取详细报告...');
        const fullReport = await client.getFullReport(backtestId, context);
        
        const summary = fullReport.summary || {};
        const metrics = {
          strategy: strategy.name,
          file: strategy.file,
          backtestId: backtestId,
          status: 'completed',
          annualized_return: summary.annualized_return || summary['年化收益率'],
          max_drawdown: summary.max_drawdown || summary['最大回撤'],
          sharpe_ratio: summary.sharpe_ratio || summary['夏普比率'],
          win_rate: summary.win_rate || summary['胜率'],
          total_return: summary.total_return || summary['总收益'],
          start_date: summary.start_date,
          end_date: summary.end_date,
          trades_count: summary.trades_count || summary['交易次数']
        };
        
        results.push(metrics);
        console.log(`  ✓ 年化收益: ${metrics.annualized_return}%`);
        console.log(`  ✓ 最大回撤: ${metrics.max_drawdown}%`);
        console.log(`  ✓ 夏普比率: ${metrics.sharpe_ratio}`);
        
      } else {
        console.log('  状态: 仍在运行中...');
        results.push({
          strategy: strategy.name,
          file: strategy.file,
          backtestId: backtestId,
          status: 'running',
          message: '回测尚未完成'
        });
      }
    } catch (error) {
      console.log(`  错误: ${error.message}`);
      results.push({
        strategy: strategy.name,
        file: strategy.file,
        backtestId: backtestId,
        status: 'error',
        message: error.message
      });
    }
  }
  
  // 保存结果
  const outputDir = './output';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const outputPath = `${outputDir}/rfscore_all_results.json`;
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalStrategies: strategies.length,
    completedCount: results.filter(r => r.status === 'completed').length,
    runningCount: results.filter(r => r.status === 'running').length,
    errorCount: results.filter(r => r.status === 'error').length,
    strategies: results
  }, null, 2));
  
  console.log(`\n✓ 结果已保存到: ${outputPath}`);
  
  // 打印摘要
  console.log('\n========================================');
  console.log('   RFScore策略回测结果摘要');
  console.log('========================================\n');
  
  results.forEach((r, i) => {
    console.log(`${i + 1}. ${r.strategy}`);
    console.log(`   文件: ${r.file}`);
    if (r.status === 'completed') {
      console.log(`   状态: ✅ 完成`);
      console.log(`   年化收益: ${r.annualized_return !== undefined ? r.annualized_return + '%' : 'N/A'}`);
      console.log(`   最大回撤: ${r.max_drawdown !== undefined ? r.max_drawdown + '%' : 'N/A'}`);
      console.log(`   夏普比率: ${r.sharpe_ratio !== undefined ? r.sharpe_ratio : 'N/A'}`);
      console.log(`   胜率: ${r.win_rate !== undefined ? r.win_rate + '%' : 'N/A'}`);
    } else if (r.status === 'running') {
      console.log(`   状态: ⏳ 运行中`);
      console.log(`   ${r.message}`);
    } else {
      console.log(`   状态: ❌ 错误`);
      console.log(`   ${r.message}`);
    }
    console.log('');
  });
}

fetchResults().catch(error => {
  console.error('执行失败:', error);
  process.exit(1);
});
