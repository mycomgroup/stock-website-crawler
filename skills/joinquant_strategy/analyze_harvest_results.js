#!/usr/bin/env node
/**
 * 分析 harvest_results.json，找出四批次中表现最好的策略
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const harvestFile = path.join(__dirname, 'data/harvest_20260405/harvest_results.json');

const data = JSON.parse(fs.readFileSync(harvestFile, 'utf8'));

// 过滤出有效的回测结果（有年化收益、夏普、回撤数据）
const allBacktests = [];

function collectBacktests(arr, label) {
  if (!Array.isArray(arr)) return;
  for (const item of arr) {
    if (
      item.annualizedReturns != null &&
      item.sharpe != null &&
      item.maxDrawdown != null &&
      item.totalReturns != null
    ) {
      allBacktests.push({ ...item, _label: label });
    }
  }
}

collectBacktests(data.top, 'top');
collectBacktests(data.all, 'all');
collectBacktests(data.completed, 'completed');
collectBacktests(data.results, 'results');

// 去重（按 backtestId）
const seen = new Set();
const unique = [];
for (const item of allBacktests) {
  if (!seen.has(item.backtestId)) {
    seen.add(item.backtestId);
    unique.push(item);
  }
}

console.log(`总有效回测数: ${unique.length}`);

// 筛选条件：回测区间至少3个月，年化收益>0
const valid = unique.filter(item => {
  const start = new Date(item.startDate);
  const end = new Date(item.endDate);
  const days = (end - start) / (1000 * 86400);
  return days >= 60 && item.annualizedReturns > 0;
});

console.log(`有效回测（>=60天且年化>0）: ${valid.length}`);

// 按综合评分排序（年化收益 * 夏普 / (1 + 最大回撤)）
const scored = valid.map(item => ({
  ...item,
  compositeScore: (item.annualizedReturns * item.sharpe) / (1 + item.maxDrawdown)
})).sort((a, b) => b.compositeScore - a.compositeScore);

// 输出 Top20
console.log('\n========== TOP 20 策略（综合评分：年化×夏普/回撤） ==========');
console.log('排名 | 策略名 | 年化收益 | 夏普 | 最大回撤 | 胜率 | 回测区间 | 综合分');
console.log('-'.repeat(120));

for (let i = 0; i < Math.min(20, scored.length); i++) {
  const s = scored[i];
  const name = (s.backtestName || s.strategyName || '').slice(0, 35).padEnd(35);
  const annual = (s.annualizedReturns * 100).toFixed(1).padStart(8) + '%';
  const sharpe = s.sharpe.toFixed(2).padStart(7);
  const dd = (s.maxDrawdown * 100).toFixed(1).padStart(8) + '%';
  const wr = s.winRate != null ? (s.winRate * 100).toFixed(0).padStart(5) + '%' : '  N/A';
  const period = `${s.startDate} ~ ${s.endDate}`;
  const score = s.compositeScore.toFixed(2).padStart(8);
  console.log(`${String(i+1).padStart(3)}  | ${name} | ${annual} | ${sharpe} | ${dd} | ${wr} | ${period} | ${score}`);
}

// 按年化收益排序 Top10
console.log('\n========== TOP 10（按年化收益率） ==========');
const byAnnual = [...valid].sort((a, b) => b.annualizedReturns - a.annualizedReturns).slice(0, 10);
for (let i = 0; i < byAnnual.length; i++) {
  const s = byAnnual[i];
  const name = (s.backtestName || s.strategyName || '').slice(0, 40);
  console.log(`${i+1}. 年化${(s.annualizedReturns*100).toFixed(1)}% 夏普${s.sharpe.toFixed(2)} 回撤${(s.maxDrawdown*100).toFixed(1)}% 胜率${s.winRate!=null?(s.winRate*100).toFixed(0)+'%':'N/A'}`);
  console.log(`   ${name}`);
  console.log(`   区间: ${s.startDate} ~ ${s.endDate} | 总收益: ${(s.totalReturns*100).toFixed(1)}%`);
}

// 按夏普比率排序 Top10
console.log('\n========== TOP 10（按夏普比率） ==========');
const bySharpe = [...valid].sort((a, b) => b.sharpe - a.sharpe).slice(0, 10);
for (let i = 0; i < bySharpe.length; i++) {
  const s = bySharpe[i];
  const name = (s.backtestName || s.strategyName || '').slice(0, 40);
  console.log(`${i+1}. 夏普${s.sharpe.toFixed(2)} 年化${(s.annualizedReturns*100).toFixed(1)}% 回撤${(s.maxDrawdown*100).toFixed(1)}%`);
  console.log(`   ${name}`);
}

// 低回撤高收益（回撤<15%，年化>50%）
console.log('\n========== 低回撤高收益（回撤<15%，年化>50%） ==========');
const lowDD = valid.filter(s => s.maxDrawdown < 0.15 && s.annualizedReturns > 0.5)
  .sort((a, b) => b.annualizedReturns - a.annualizedReturns);
if (lowDD.length === 0) {
  console.log('无满足条件的策略');
} else {
  for (let i = 0; i < Math.min(10, lowDD.length); i++) {
    const s = lowDD[i];
    const name = (s.backtestName || s.strategyName || '').slice(0, 45);
    console.log(`${i+1}. 年化${(s.annualizedReturns*100).toFixed(1)}% 回撤${(s.maxDrawdown*100).toFixed(1)}% 夏普${s.sharpe.toFixed(2)} 胜率${s.winRate!=null?(s.winRate*100).toFixed(0)+'%':'N/A'}`);
    console.log(`   ${name}`);
    console.log(`   区间: ${s.startDate} ~ ${s.endDate}`);
  }
}

// 统计分布
console.log('\n========== 年化收益分布 ==========');
const buckets = { '亏损': 0, '0-20%': 0, '20-50%': 0, '50-100%': 0, '100-200%': 0, '200%+': 0 };
for (const s of valid) {
  const a = s.annualizedReturns * 100;
  if (a < 0) buckets['亏损']++;
  else if (a < 20) buckets['0-20%']++;
  else if (a < 50) buckets['20-50%']++;
  else if (a < 100) buckets['50-100%']++;
  else if (a < 200) buckets['100-200%']++;
  else buckets['200%+']++;
}
for (const [k, v] of Object.entries(buckets)) {
  const bar = '█'.repeat(Math.round(v / valid.length * 50));
  console.log(`${k.padEnd(8)}: ${String(v).padStart(4)}个 ${bar}`);
}
