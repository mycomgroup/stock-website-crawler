#!/usr/bin/env node
/**
 * 从未跑和失败的策略中筛选今天批次的75个高潜力策略
 * 排除所有已成功提交的策略（批次1/2/3）
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..', '..');

const SOURCE_DIR = path.resolve(REPO_ROOT, 'jk2bt-main', 'strategies');
const BATCH1_DIR = path.resolve(__dirname, 'data', 'jq558_batch_20260403');
const BATCH2_DIR = path.resolve(__dirname, 'data', 'jq558_batch_20260404');
const BATCH3_DIR = path.resolve(__dirname, 'data', 'jq558_top100_20260405');
const OUTPUT_FILE = path.resolve(__dirname, 'data', 'selected_batch4_75.json');

const SELECT_COUNT = 75;

const KEYWORD_SCORES = {
  '年化': 3, '倍': 3, '收益': 2, '超额': 2, '稳定': 2, '低回撤': 3, '胜率': 3,
  '小市值': 2, '龙头': 2, '首板': 2, '涨停': 2, 'ETF': 2, '轮动': 2,
  '择时': 1, '动量': 1, '因子': 1, '多因子': 2, '机器学习': 2, 'AI': 2, '随机森林': 2,
  '价值': 1, '红利': 2, '股息': 2, '低估': 1, 'PEG': 1, 'PB': 1, 'PE': 1,
  '打板': 2, '连板': 2, '竞价': 1, '分钟': 1, '超短': 1,
  '测试': -2, 'test': -2, '实验': -1, '尝试': -1,
};

function walkStrategyFiles(rootDir) {
  const files = [];
  const stack = [rootDir];
  while (stack.length) {
    const current = stack.pop();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) { stack.push(fullPath); continue; }
      if (entry.isFile() && (entry.name.endsWith('.txt') || entry.name.endsWith('.py'))) {
        files.push(fullPath);
      }
    }
  }
  return files;
}

function readBatchRecords(batchDirs) {
  const submitted = new Set();
  const failed = new Set();
  for (const batchDir of batchDirs) {
    const jsonlPath = path.join(batchDir, 'submissions.jsonl');
    if (!fs.existsSync(jsonlPath)) continue;
    const lines = fs.readFileSync(jsonlPath, 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const item = JSON.parse(line);
        const basename = path.basename(item.file || item.relativePath || '');
        if (item.status === 'submitted') submitted.add(basename);
        else if (item.status === 'failed') failed.add(basename);
      } catch { /* ignore */ }
    }
  }
  return { submitted, failed };
}

function calculateScore(filename) {
  let score = 0;
  const lowerName = filename.toLowerCase();
  for (const [keyword, points] of Object.entries(KEYWORD_SCORES)) {
    if (lowerName.includes(keyword.toLowerCase())) score += points;
  }
  const yearlyMatch = filename.match(/年化[^\d]*(\d+)/);
  if (yearlyMatch) {
    const pct = parseInt(yearlyMatch[1]);
    if (pct >= 50) score += 3;
    else if (pct >= 30) score += 2;
    else if (pct >= 20) score += 1;
  }
  const multipleMatch = filename.match(/(\d+)倍/);
  if (multipleMatch) {
    const mul = parseInt(multipleMatch[1]);
    if (mul >= 10) score += 3;
    else if (mul >= 5) score += 2;
    else if (mul >= 3) score += 1;
  }
  return score;
}

function main() {
  console.log(`开始筛选今天批次的 ${SELECT_COUNT} 个高潜力策略...\n`);

  const allFiles = walkStrategyFiles(SOURCE_DIR);
  console.log(`总策略文件数: ${allFiles.length}`);

  const { submitted, failed } = readBatchRecords([BATCH1_DIR, BATCH2_DIR, BATCH3_DIR]);
  console.log(`所有批次已成功提交: ${submitted.size}`);
  console.log(`所有批次失败记录: ${failed.size}`);

  const candidates = [];
  for (const file of allFiles) {
    const basename = path.basename(file);
    const relativePath = path.relative(path.dirname(SOURCE_DIR), file);
    if (submitted.has(basename)) continue; // 跳过已成功提交的
    const score = calculateScore(basename);
    const isFailed = failed.has(basename);
    candidates.push({
      file, relativePath, basename, score, isFailed,
      finalScore: isFailed ? score - 0.5 : score
    });
  }

  console.log(`候选策略数: ${candidates.length}`);
  console.log(`  - 未跑过: ${candidates.filter(c => !c.isFailed).length}`);
  console.log(`  - 之前失败: ${candidates.filter(c => c.isFailed).length}`);

  candidates.sort((a, b) => {
    if (b.finalScore !== a.finalScore) return b.finalScore - a.finalScore;
    if (a.isFailed !== b.isFailed) return a.isFailed ? 1 : -1;
    return a.basename.localeCompare(b.basename, 'zh-Hans-CN');
  });

  const selected = candidates.slice(0, SELECT_COUNT);

  const output = {
    generatedAt: new Date().toISOString(),
    batchName: 'jq558_batch4_20260407',
    totalCandidates: candidates.length,
    selected: selected.length,
    statistics: {
      newStrategies: selected.filter(c => !c.isFailed).length,
      retryFailed: selected.filter(c => c.isFailed).length,
      avgScore: (selected.reduce((sum, c) => sum + c.finalScore, 0) / selected.length).toFixed(2)
    },
    strategies: selected.map((c, idx) => ({
      rank: idx + 1,
      file: c.relativePath,
      basename: c.basename,
      score: c.finalScore,
      status: c.isFailed ? 'retry' : 'new'
    }))
  };

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2), 'utf8');

  console.log('\n筛选完成！');
  console.log(`输出文件: ${OUTPUT_FILE}`);
  console.log(`\n统计:`);
  console.log(`  新策略: ${output.statistics.newStrategies}`);
  console.log(`  重试失败: ${output.statistics.retryFailed}`);
  console.log(`  平均分数: ${output.statistics.avgScore}`);
  console.log('\n前10名:');
  for (let i = 0; i < Math.min(10, selected.length); i++) {
    const s = selected[i];
    console.log(`  ${i + 1}. [${s.finalScore.toFixed(1)}分] ${s.isFailed ? '(重试)' : '(新)'} ${s.basename}`);
  }
}

main();
