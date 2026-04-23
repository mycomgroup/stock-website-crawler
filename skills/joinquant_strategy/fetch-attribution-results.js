#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function main() {
  console.log('获取已完成的回测结果\n');
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext('801d56e162b037ed1a6e0ba5d26ff092');
  
  const backtests = await client.getBacktests('801d56e162b037ed1a6e0ba5d26ff092');
  
  console.log('总回测数:', backtests.length);
  
  const completed = backtests.filter(bt => bt.status === '2' || bt.status === 2);
  console.log('已完成:', completed.length);
  
  const results = [];
  
  for (const bt of completed.slice(0, 10)) {
    const statsResult = await client.getBacktestStats(bt.id, context);
    const stats = statsResult.data || {};
    
    if (stats.annual_algo_return !== undefined) {
      results.push({
        id: bt.id,
        name: bt.name,
        annual: stats.annual_algo_return,
        total: stats.algorithm_return,
        sharpe: stats.sharpe,
        maxDD: stats.max_drawdown,
        alpha: stats.alpha,
        beta: stats.beta,
        winRatio: stats.win_ratio,
      });
    }
  }
  
  console.log('\n' + '='.repeat(80));
  console.log('回测结果汇总');
  console.log('='.repeat(80));
  console.log('\n| 名称 | 年化 | 累计 | 夏普 | 最大回撤 | Alpha | Beta | 胜率 |');
  console.log('|------|------|------|------|---------|-------|------|------|');
  
  for (const r of results) {
    console.log(`| ${r.name.slice(0, 30)} | ${(r.annual * 100).toFixed(2)}% | ${(r.total * 100).toFixed(2)}% | ${r.sharpe.toFixed(3)} | ${(r.maxDD * 100).toFixed(2)}% | ${(r.alpha * 100).toFixed(2)}% | ${r.beta.toFixed(3)} | ${(r.winRatio * 100).toFixed(2)}% |`);
  }
  
  // Save results
  const outputDir = path.join(__dirname, 'data', `attribution_${Date.now()}`);
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, 'results.json'), JSON.stringify(results, null, 2));
  console.log('\n结果已保存: ' + path.join(outputDir, 'results.json'));
}

main().catch(console.error);
