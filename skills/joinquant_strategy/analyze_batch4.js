#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const batches = [
  { name: '批次1 (20260403)', dir: path.join(__dirname, 'data/jq558_batch_20260403') },
  { name: '批次2 (20260404)', dir: path.join(__dirname, 'data/jq558_batch_20260404') },
  { name: '批次3 (20260405)', dir: path.join(__dirname, 'data/jq558_top100_20260405') },
  { name: '批次4 (20260407)', dir: path.join(__dirname, 'data/jq558_batch4_20260407') },
];

let grandTotal = 0, grandSuccess = 0, grandFail = 0;
const allSuccessItems = [];

for (const batch of batches) {
  const jsonlPath = path.join(batch.dir, 'submissions.jsonl');
  if (!fs.existsSync(jsonlPath)) { console.log(batch.name + ': 文件不存在'); continue; }
  const lines = fs.readFileSync(jsonlPath, 'utf8').split('\n').filter(Boolean);
  let success = 0, fail = 0;
  const errors = {};
  for (const line of lines) {
    try {
      const item = JSON.parse(line);
      if (item.status === 'submitted') {
        success++;
        allSuccessItems.push({ ...item, batchName: batch.name });
      } else {
        fail++;
        const e = (item.error || 'unknown').slice(0, 80);
        errors[e] = (errors[e] || 0) + 1;
      }
    } catch {}
  }
  grandTotal += lines.length;
  grandSuccess += success;
  grandFail += fail;
  const rate = lines.length > 0 ? (success / lines.length * 100).toFixed(1) : '0.0';
  console.log(`${batch.name}: 总=${lines.length} 成功=${success} 失败=${fail} 成功率=${rate}%`);
  const topErrors = Object.entries(errors).sort((a, b) => b[1] - a[1]).slice(0, 3);
  for (const [e, c] of topErrors) {
    console.log(`  失败(${c}次): ${e}`);
  }
}

console.log('');
const totalRate = grandTotal > 0 ? (grandSuccess / grandTotal * 100).toFixed(1) : '0.0';
console.log(`四批次合计: 总=${grandTotal} 成功=${grandSuccess} 失败=${grandFail} 成功率=${totalRate}%`);

// 按批次分析分数分布
console.log('\n--- 批次4 分数分布 ---');
const b4path = path.join(__dirname, 'data/jq558_batch4_20260407/submissions.jsonl');
if (fs.existsSync(b4path)) {
  const items = fs.readFileSync(b4path, 'utf8').split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  const scoreGroups = {};
  for (const item of items) {
    const s = String(item.score);
    scoreGroups[s] = (scoreGroups[s] || 0) + 1;
  }
  Object.entries(scoreGroups).sort((a, b) => parseFloat(b[0]) - parseFloat(a[0])).forEach(([s, c]) => {
    console.log(`  分数${s}: ${c}个`);
  });
}

// 按策略类型统计（基于名称关键词）
console.log('\n--- 四批次成功策略类型分布 ---');
const typeMap = {
  'ETF轮动': 0, '小市值': 0, '机器学习/随机森林': 0, '打板/首板': 0,
  '多因子': 0, '动量': 0, '红利/价值': 0, '其他': 0
};
for (const item of allSuccessItems) {
  const n = item.basename || '';
  if (n.includes('ETF') && (n.includes('轮动') || n.includes('动量'))) typeMap['ETF轮动']++;
  else if (n.includes('小市值')) typeMap['小市值']++;
  else if (n.includes('机器学习') || n.includes('随机森林') || n.includes('SVR') || n.includes('神经网络')) typeMap['机器学习/随机森林']++;
  else if (n.includes('打板') || n.includes('首板') || n.includes('涨停') || n.includes('连板')) typeMap['打板/首板']++;
  else if (n.includes('多因子') || n.includes('因子')) typeMap['多因子']++;
  else if (n.includes('动量')) typeMap['动量']++;
  else if (n.includes('红利') || n.includes('价值') || n.includes('股息')) typeMap['红利/价值']++;
  else typeMap['其他']++;
}
Object.entries(typeMap).sort((a, b) => b[1] - a[1]).forEach(([t, c]) => {
  if (c > 0) console.log(`  ${t}: ${c}个`);
});
