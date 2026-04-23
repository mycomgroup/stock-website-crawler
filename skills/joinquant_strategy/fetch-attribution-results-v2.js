#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const VERSION_MAP = {
  'RFScore7_Attribution_A_原版': 'A_原版_Release_V1',
  'RFScore7_Attribution_B_Pure_PB': 'B_纯PB低估值',
  'RFScore7_Attribution_C_Pure_RFScore': 'C_纯RFScore7',
  'RFScore7_Attribution_D_No_Market_State': 'D_无市场状态风控',
  'RFScore7 PB10 Release V1': 'A_原版_Release_V1',
};

async function main() {
  console.log('获取因子剥离验证结果\n');
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext('801d56e162b037ed1a6e0ba5d26ff092');
  
  const backtests = await client.getBacktests('801d56e162b037ed1a6e0ba5d26ff092');
  const completed = backtests.filter(bt => bt.status === '2' || bt.status === 2);
  
  console.log('已完成回测:', completed.length);
  
  const results = [];
  const seen = new Set();
  
  for (const bt of completed) {
    if (results.length >= 4) break;
    
    const log = await client.getLog(bt.id);
    const logArr = log.data?.logArr || [];
    if (logArr.length === 0) continue;
    
    const firstLog = logArr[0];
    let version = 'Unknown';
    for (const [key, label] of Object.entries(VERSION_MAP)) {
      if (firstLog.includes(key)) {
        version = label;
        break;
      }
    }
    
    if (seen.has(version)) continue;
    seen.add(version);
    
    const statsResult = await client.getBacktestStats(bt.id, context);
    const stats = statsResult.data || {};
    
    if (stats.annual_algo_return !== undefined) {
      results.push({
        version,
        id: bt.id,
        annual: stats.annual_algo_return,
        total: stats.algorithm_return,
        sharpe: stats.sharpe,
        maxDD: stats.max_drawdown,
        alpha: stats.alpha,
        beta: stats.beta,
        winRatio: stats.win_ratio,
        benchmarkReturn: stats.benchmark_return,
        algoVolatility: stats.algorithm_volatility,
      });
      console.log('Found: ' + version + ' (' + bt.id.slice(0, 8) + ')');
    }
  }
  
  console.log('\n' + '='.repeat(90));
  console.log('因子剥离验证 - 对比结果');
  console.log('='.repeat(90));
  console.log('\n| 版本 | 年化 | 累计 | 夏普 | 最大回撤 | Alpha | Beta | 胜率 |');
  console.log('|------|------|------|------|---------|-------|------|------|');
  
  for (const r of results) {
    console.log(`| ${r.version} | ${(r.annual * 100).toFixed(2)}% | ${(r.total * 100).toFixed(2)}% | ${r.sharpe.toFixed(3)} | ${(r.maxDD * 100).toFixed(2)}% | ${(r.alpha * 100).toFixed(2)}% | ${r.beta.toFixed(3)} | ${(r.winRatio * 100).toFixed(2)}% |`);
  }
  
  if (results.length >= 2) {
    console.log('\n' + '='.repeat(90));
    console.log('对比分析');
    console.log('='.repeat(90));
    
    const a = results.find(r => r.version.includes('A_原版'));
    const b = results.find(r => r.version.includes('B_纯PB'));
    const c = results.find(r => r.version.includes('C_纯RFScore'));
    const d = results.find(r => r.version.includes('D_无市场'));
    
    if (a && b) {
      const diff = a.annual - b.annual;
      console.log('\nA vs B (RFScore7增量贡献):');
      console.log('  年化差异: ' + (diff * 100).toFixed(2) + '%');
      console.log(diff > 2 ? '  → RFScore7有显著增量贡献' : diff > -2 ? '  → RFScore7贡献有限，PB是核心因子' : '  → RFScore7可能拖累收益');
    }
    
    if (a && c) {
      const diff = a.annual - c.annual;
      console.log('\nA vs C (PB筛选必要性):');
      console.log('  年化差异: ' + (diff * 100).toFixed(2) + '%');
      console.log(diff > 2 ? '  → PB筛选是必要的' : '  → PB筛选不是关键');
    }
    
    if (a && d) {
      const sharpeDiff = a.sharpe - d.sharpe;
      const ddDiff = a.maxDD - d.maxDD;
      console.log('\nA vs D (市场状态风控有效性):');
      console.log('  夏普差异: ' + sharpeDiff.toFixed(3));
      console.log('  回撤差异: ' + (ddDiff * 100).toFixed(2) + '%');
      console.log(sharpeDiff > 0.1 ? '  → 市场状态风控有效' : '  → 市场状态风控效果不明显');
    }
  }
  
  const outputDir = path.join(__dirname, 'data', `attribution_${Date.now()}`);
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, 'results.json'), JSON.stringify(results, null, 2));
  console.log('\n结果已保存: ' + path.join(outputDir, 'results.json'));
}

main().catch(console.error);
