#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 回测ID映射
const backtestIds = {
  'rfscore7_pb10_final_v2': '0db2a65f73983ffdef8de5aa89f2ca3a',
  'rfscore7_pb10_release_v1': 'dc592d1ba64acf6a905f5f87073b19bf',
  'rfscore_defensive_combined': '3485c8bb3282df192e9cb0eaa4f841bb',
  'rfscore7_pb10_enhanced_selection': '12b1f52ce8c011eacd22383df009367a',
  'rfscore7_pb10_multi_signal_risk_control': 'f4cbd9181c473d73dde0f781b70dfbe4',
  'rfscore_defensive_dynamic_hedge': '59438eac66db9d145104b70066bdb2b8'
};

const strategies = [
  { id: 'rfscore7_pb10_final_v2', name: 'V2原版', file: 'rfscore7_pb10_final_v2.py' },
  { id: 'rfscore7_pb10_release_v1', name: 'Release V1', file: 'rfscore7_pb10_release_v1.py' },
  { id: 'rfscore_defensive_combined', name: 'Defensive原版', file: 'rfscore_defensive_combined.py' },
  { id: 'rfscore7_pb10_enhanced_selection', name: '增强选股版', file: 'rfscore7_pb10_enhanced_selection.py' },
  { id: 'rfscore7_pb10_multi_signal_risk_control', name: '多信号风控版', file: 'rfscore7_pb10_multi_signal_risk_control.py' },
  { id: 'rfscore_defensive_dynamic_hedge', name: '动态对冲版', file: 'rfscore_defensive_dynamic_hedge.py' }
];

async function collectResults() {
  console.log('正在收集RFScore策略回测结果...\n');
  
  const results = [];
  
  for (const strategy of strategies) {
    const backtestId = backtestIds[strategy.id];
    console.log(`检查策略: ${strategy.name} (ID: ${backtestId})`);
    
    try {
      const result = await fetchBacktestResult(backtestId);
      if (result) {
        results.push({
          strategy: strategy.name,
          file: strategy.file,
          backtestId: backtestId,
          ...result
        });
        console.log(`  ✓ 成功获取结果`);
      } else {
        console.log(`  ✗ 未找到结果`);
        results.push({
          strategy: strategy.name,
          file: strategy.file,
          backtestId: backtestId,
          status: 'pending',
          message: '回测可能仍在运行中'
        });
      }
    } catch (error) {
      console.log(`  ✗ 获取失败: ${error.message}`);
      results.push({
        strategy: strategy.name,
        file: strategy.file,
        backtestId: backtestId,
        status: 'error',
        message: error.message
      });
    }
  }
  
  // 保存结果到文件
  const outputPath = path.join(__dirname, 'output', 'rfscore_all_results.json');
  fs.writeFileSync(outputPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    strategies: results
  }, null, 2));
  
  console.log(`\n✓ 结果已保存到: ${outputPath}`);
  
  // 打印摘要
  console.log('\n=== RFScore策略回测结果摘要 ===\n');
  results.forEach((r, i) => {
    console.log(`${i + 1}. ${r.strategy}`);
    console.log(`   文件: ${r.file}`);
    console.log(`   回测ID: ${r.backtestId}`);
    if (r.status === 'pending') {
      console.log(`   状态: ⏳ 运行中`);
    } else if (r.status === 'error') {
      console.log(`   状态: ❌ 错误 - ${r.message}`);
    } else if (r.annualized_return !== undefined) {
      console.log(`   年化收益: ${r.annualized_return}%`);
      console.log(`   最大回撤: ${r.max_drawdown}%`);
      console.log(`   夏普比率: ${r.sharpe_ratio}`);
      console.log(`   胜率: ${r.win_rate}%`);
    }
    console.log('');
  });
}

async function fetchBacktestResult(backtestId) {
  try {
    const outputDir = '/Users/fengzhi/Downloads/git/testlixingren/output';
    const files = fs.readdirSync(outputDir)
      .filter(f => f.includes(backtestId) && f.endsWith('.json'))
      .map(f => ({
        path: path.join(outputDir, f),
        mtime: fs.statSync(path.join(outputDir, f)).mtime
      }))
      .sort((a, b) => b.mtime - a.mtime);
    
    if (files.length > 0) {
      const data = JSON.parse(fs.readFileSync(files[0].path, 'utf8'));
      const summary = data.summary || {};
      
      return {
        status: 'completed',
        annualized_return: summary.annual_algo_return ? (summary.annual_algo_return * 100).toFixed(2) : 'N/A',
        total_return: summary.algorithm_return ? (summary.algorithm_return * 100).toFixed(2) : 'N/A',
        max_drawdown: summary.max_drawdown ? (summary.max_drawdown * 100).toFixed(2) : 'N/A',
        sharpe_ratio: summary.sharpe ? summary.sharpe.toFixed(2) : 'N/A',
        win_rate: summary.win_ratio ? (summary.win_ratio * 100).toFixed(2) : 'N/A',
        benchmark_return: summary.benchmark_return ? (summary.benchmark_return * 100).toFixed(2) : 'N/A',
        beta: summary.beta ? summary.beta.toFixed(2) : 'N/A',
        alpha: summary.alpha ? (summary.alpha * 100).toFixed(2) : 'N/A'
      };
    }
    return null;
  } catch (e) {
    return null;
  }
}

collectResults().catch(console.error);
