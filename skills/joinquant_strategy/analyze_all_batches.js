#!/usr/bin/env node
/**
 * 汇总分析三批次提交的策略收益情况
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const BATCH_DIRS = [
  path.resolve(__dirname, 'data', 'jq558_batch_20260403'),
  path.resolve(__dirname, 'data', 'jq558_batch_20260404'),
  path.resolve(__dirname, 'data', 'jq558_top100_20260405')
];

const OUTPUT_FILE = path.resolve(__dirname, 'data', 'all_batches_summary.json');
const MD_FILE = path.resolve(__dirname, 'data', 'all_batches_summary.md');

function readBatchSubmissions(batchDir) {
  const jsonlPath = path.join(batchDir, 'submissions.jsonl');
  const submissions = [];
  
  if (!fs.existsSync(jsonlPath)) {
    return submissions;
  }
  
  const lines = fs.readFileSync(jsonlPath, 'utf8').split('\n').filter(Boolean);
  for (const line of lines) {
    try {
      const item = JSON.parse(line);
      submissions.push(item);
    } catch {
      // 忽略解析错误
    }
  }
  
  return submissions;
}

function readBatchResults(batchDir) {
  const resultsPath = path.join(batchDir, 'results_snapshot.json');
  
  if (!fs.existsSync(resultsPath)) {
    return null;
  }
  
  try {
    return JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
  } catch {
    return null;
  }
}

function analyzeBatch(batchDir, batchName) {
  const submissions = readBatchSubmissions(batchDir);
  const results = readBatchResults(batchDir);
  
  const submitted = submissions.filter(s => s.status === 'submitted');
  const failed = submissions.filter(s => s.status === 'failed');
  
  const analysis = {
    batchName,
    batchDir,
    totalSubmissions: submissions.length,
    successfulSubmissions: submitted.length,
    failedSubmissions: failed.length,
    successRate: submissions.length > 0 
      ? ((submitted.length / submissions.length) * 100).toFixed(2) + '%'
      : '0%',
    hasResults: !!results,
    completedBacktests: 0,
    pendingBacktests: 0,
    profitableStrategies: [],
    topStrategies: []
  };
  
  if (results) {
    analysis.completedBacktests = results.totals?.completed || results.completed?.length || 0;
    analysis.pendingBacktests = results.totals?.pending || results.pending?.length || 0;
    
    // 分析已完成的回测结果
    const completed = results.completed || [];
    const profitable = completed.filter(r => {
      const returns = r.summary?.total_returns || r.summary?.annualized_returns || 0;
      return returns > 0;
    });
    
    analysis.profitableStrategies = profitable.map(r => ({
      file: r.file || r.strategyName,
      totalReturns: r.summary?.total_returns,
      annualizedReturns: r.summary?.annualized_returns,
      sharpe: r.summary?.sharpe,
      maxDrawdown: r.summary?.max_drawdown,
      winRate: r.summary?.win_rate
    }));
    
    // 按年化收益���序，取前10
    analysis.topStrategies = [...analysis.profitableStrategies]
      .sort((a, b) => (b.annualizedReturns || 0) - (a.annualizedReturns || 0))
      .slice(0, 10);
  }
  
  return analysis;
}

function generateMarkdownReport(allAnalysis) {
  const lines = [
    '# 聚宽策略批量提交三批次汇总报告',
    '',
    `生成时间: ${new Date().toISOString().replace('T', ' ').slice(0, 19)}`,
    '',
    '## 总体概况',
    ''
  ];
  
  let totalSubmissions = 0;
  let totalSuccess = 0;
  let totalFailed = 0;
  let totalCompleted = 0;
  let totalPending = 0;
  
  for (const batch of allAnalysis) {
    totalSubmissions += batch.totalSubmissions;
    totalSuccess += batch.successfulSubmissions;
    totalFailed += batch.failedSubmissions;
    totalCompleted += batch.completedBacktests;
    totalPending += batch.pendingBacktests;
  }
  
  lines.push('| 指标 | 数量 |');
  lines.push('|------|------|');
  lines.push(`| 总提交策略数 | ${totalSubmissions} |`);
  lines.push(`| 成功提交 | ${totalSuccess} |`);
  lines.push(`| 提交失败 | ${totalFailed} |`);
  lines.push(`| 提交成功率 | ${((totalSuccess / totalSubmissions) * 100).toFixed(2)}% |`);
  lines.push(`| 已完成回测 | ${totalCompleted} |`);
  lines.push(`| 待完成回测 | ${totalPending} |`);
  lines.push(`| 回测完成率 | ${totalSuccess > 0 ? ((totalCompleted / totalSuccess) * 100).toFixed(2) : 0}% |`);
  lines.push('');
  
  lines.push('## 各批次详情');
  lines.push('');
  
  for (let i = 0; i < allAnalysis.length; i++) {
    const batch = allAnalysis[i];
    lines.push(`### 批次${i + 1}: ${batch.batchName}`);
    lines.push('');
    lines.push('| 指标 | 数量 |');
    lines.push('|------|------|');
    lines.push(`| 总提交 | ${batch.totalSubmissions} |`);
    lines.push(`| 成功提交 | ${batch.successfulSubmissions} |`);
    lines.push(`| 提交失败 | ${batch.failedSubmissions} |`);
    lines.push(`| 提交成功率 | ${batch.successRate} |`);
    lines.push(`| 已完成回测 | ${batch.completedBacktests} |`);
    lines.push(`| 待完成回测 | ${batch.pendingBacktests} |`);
    lines.push('');
    
    if (batch.topStrategies.length > 0) {
      lines.push(`#### Top ${Math.min(10, batch.topStrategies.length)} 策略（按年化收益）`);
      lines.push('');
      lines.push('| 排名 | 策略 | 总收益 | 年化收益 | 夏普比率 | 最大回撤 | 胜率 |');
      lines.push('|------|------|--------|----------|----------|----------|------|');
      
      for (let j = 0; j < batch.topStrategies.length; j++) {
        const s = batch.topStrategies[j];
        const fileName = (s.file || '').split('/').pop() || s.file;
        lines.push(`| ${j + 1} | ${fileName} | ${(s.totalReturns * 100).toFixed(2)}% | ${(s.annualizedReturns * 100).toFixed(2)}% | ${s.sharpe?.toFixed(2) || 'N/A'} | ${s.maxDrawdown ? (s.maxDrawdown * 100).toFixed(2) + '%' : 'N/A'} | ${s.winRate ? (s.winRate * 100).toFixed(2) + '%' : 'N/A'} |`);
      }
      lines.push('');
    }
  }
  
  // 汇总所有盈利策略
  const allProfitable = [];
  for (const batch of allAnalysis) {
    for (const s of batch.profitableStrategies) {
      allProfitable.push({
        ...s,
        batch: batch.batchName
      });
    }
  }
  
  if (allProfitable.length > 0) {
    lines.push('## 全部盈利策略汇总');
    lines.push('');
    lines.push(`共 ${allProfitable.length} 个策略产生正收益`);
    lines.push('');
    
    const topAll = [...allProfitable]
      .sort((a, b) => (b.annualizedReturns || 0) - (a.annualizedReturns || 0))
      .slice(0, 20);
    
    lines.push('### Top 20 策略（跨批次）');
    lines.push('');
    lines.push('| 排名 | 批次 | 策略 | 总收益 | 年化收益 | 夏普比率 | 最大回撤 | 胜率 |');
    lines.push('|------|------|------|--------|----------|----------|----------|------|');
    
    for (let i = 0; i < topAll.length; i++) {
      const s = topAll[i];
      const fileName = (s.file || '').split('/').pop() || s.file;
      lines.push(`| ${i + 1} | ${s.batch} | ${fileName} | ${(s.totalReturns * 100).toFixed(2)}% | ${(s.annualizedReturns * 100).toFixed(2)}% | ${s.sharpe?.toFixed(2) || 'N/A'} | ${s.maxDrawdown ? (s.maxDrawdown * 100).toFixed(2) + '%' : 'N/A'} | ${s.winRate ? (s.winRate * 100).toFixed(2) + '%' : 'N/A'} |`);
    }
    lines.push('');
  }
  
  lines.push('## 数据说明');
  lines.push('');
  lines.push('- 回测区间：2025-04-03 至 2026-04-03（最近1年）');
  lines.push('- 初始资金：100,000元');
  lines.push('- 频率：日线');
  lines.push('- 总收益 = (期末资产 - 期初资产) / 期初资产');
  lines.push('- 年化收益 = 总收益 / 回测年数');
  lines.push('- 夏普比率：风险调整后收益指标，越高越好');
  lines.push('- 最大回撤：策略运行期间的最大亏损幅度');
  lines.push('- 胜率：盈利交易次数 / 总交易次数');
  lines.push('');
  
  return lines.join('\n');
}

function main() {
  console.log('开始分析三批次提交数据...\n');
  
  const allAnalysis = [];
  
  for (let i = 0; i < BATCH_DIRS.length; i++) {
    const batchDir = BATCH_DIRS[i];
    const batchName = path.basename(batchDir);
    
    if (!fs.existsSync(batchDir)) {
      console.log(`批次目录不存在: ${batchDir}`);
      continue;
    }
    
    console.log(`分析批次 ${i + 1}: ${batchName}`);
    const analysis = analyzeBatch(batchDir, batchName);
    allAnalysis.push(analysis);
    
    console.log(`  总提交: ${analysis.totalSubmissions}`);
    console.log(`  成功: ${analysis.successfulSubmissions}`);
    console.log(`  失败: ${analysis.failedSubmissions}`);
    console.log(`  已完成回测: ${analysis.completedBacktests}`);
    console.log(`  盈利策略: ${analysis.profitableStrategies.length}`);
    console.log('');
  }
  
  // 保存JSON
  const summary = {
    generatedAt: new Date().toISOString(),
    batches: allAnalysis,
    totals: {
      submissions: allAnalysis.reduce((sum, b) => sum + b.totalSubmissions, 0),
      successful: allAnalysis.reduce((sum, b) => sum + b.successfulSubmissions, 0),
      failed: allAnalysis.reduce((sum, b) => sum + b.failedSubmissions, 0),
      completed: allAnalysis.reduce((sum, b) => sum + b.completedBacktests, 0),
      pending: allAnalysis.reduce((sum, b) => sum + b.pendingBacktests, 0),
      profitable: allAnalysis.reduce((sum, b) => sum + b.profitableStrategies.length, 0)
    }
  };
  
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(summary, null, 2), 'utf8');
  console.log(`JSON报告已保存: ${OUTPUT_FILE}`);
  
  // 生成Markdown报告
  const markdown = generateMarkdownReport(allAnalysis);
  fs.writeFileSync(MD_FILE, markdown, 'utf8');
  console.log(`Markdown报告已保存: ${MD_FILE}`);
  
  console.log('\n汇总完成！');
  console.log(`总提交: ${summary.totals.submissions}`);
  console.log(`成功提交: ${summary.totals.successful}`);
  console.log(`已完成回测: ${summary.totals.completed}`);
  console.log(`盈利策略: ${summary.totals.profitable}`);
}

main();
