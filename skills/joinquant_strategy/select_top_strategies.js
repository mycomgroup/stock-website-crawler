#!/usr/bin/env node
/**
 * 从未跑和失败的策略中筛选最有潜力的100个
 * 基于策略名称关键词评分
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..', '..');

// 配置
const SOURCE_DIR = path.resolve(REPO_ROOT, 'jk2bt-main', 'strategies');
const BATCH1_DIR = path.resolve(__dirname, 'data', 'jq558_batch_20260403');
const BATCH2_DIR = path.resolve(__dirname, 'data', 'jq558_batch_20260404');
const OUTPUT_FILE = path.resolve(__dirname, 'data', 'selected_top100.json');

// 高价值关键词评分表（基于策略名称）
const KEYWORD_SCORES = {
  // 高收益关键词
  '年化': 3,
  '倍': 3,
  '收益': 2,
  '超额': 2,
  '稳定': 2,
  '低回撤': 3,
  '胜率': 3,
  
  // 策略类型（经过验证的有效策略）
  '小市值': 2,
  '龙头': 2,
  '首板': 2,
  '涨停': 2,
  'ETF': 2,
  '轮动': 2,
  '择时': 1,
  '动量': 1,
  
  // 因子策略
  '因子': 1,
  '多因子': 2,
  '机器学习': 2,
  'AI': 2,
  '随机森林': 2,
  
  // 价值投资
  '价值': 1,
  '红利': 2,
  '股息': 2,
  '低估': 1,
  'PEG': 1,
  'PB': 1,
  'PE': 1,
  
  // 短线策略
  '打板': 2,
  '连板': 2,
  '竞价': 1,
  '分钟': 1,
  '超短': 1,
  
  // 负面关键词（降低分数）
  '测试': -2,
  'test': -2,
  '实验': -1,
  '尝试': -1,
};

function walkStrategyFiles(rootDir) {
  const files = [];
  const stack = [rootDir];
  while (stack.length) {
    const current = stack.pop();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
        continue;
      }
      if (entry.isFile() && (entry.name.endsWith('.txt') || entry.name.endsWith('.py'))) {
        files.push(fullPath);
      }
    }
  }
  return files;
}

function readSubmittedAndFailed() {
  const submitted = new Set();
  const failed = new Set();
  
  // 读取两个批次的日志
  for (const batchDir of [BATCH1_DIR, BATCH2_DIR]) {
    const jsonlPath = path.join(batchDir, 'submissions.jsonl');
    if (!fs.existsSync(jsonlPath)) continue;
    
    const lines = fs.readFileSync(jsonlPath, 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const item = JSON.parse(line);
        const basename = path.basename(item.file || item.relativePath || '');
        
        if (item.status === 'submitted') {
          submitted.add(basename);
        } else if (item.status === 'failed') {
          failed.add(basename);
        }
      } catch {
        // 忽略解析错误
      }
    }
  }
  
  return { submitted, failed };
}

function calculateScore(filename) {
  let score = 0;
  const lowerName = filename.toLowerCase();
  
  for (const [keyword, points] of Object.entries(KEYWORD_SCORES)) {
    if (lowerName.includes(keyword.toLowerCase())) {
      score += points;
    }
  }
  
  // 数字提取：如果包含"年化XX%"或"XX倍"，额外加分
  const yearlyReturnMatch = filename.match(/年化[^\d]*(\d+)/);
  if (yearlyReturnMatch) {
    const percent = parseInt(yearlyReturnMatch[1]);
    if (percent >= 50) score += 3;
    else if (percent >= 30) score += 2;
    else if (percent >= 20) score += 1;
  }
  
  const multipleMatch = filename.match(/(\d+)倍/);
  if (multipleMatch) {
    const multiple = parseInt(multipleMatch[1]);
    if (multiple >= 10) score += 3;
    else if (multiple >= 5) score += 2;
    else if (multiple >= 3) score += 1;
  }
  
  return score;
}

function main() {
  console.log('开始筛选最有潜力的100个策略...\n');
  
  // 1. 获取所有策略文件
  const allFiles = walkStrategyFiles(SOURCE_DIR);
  console.log(`总策略文件数: ${allFiles.length}`);
  
  // 2. 读取已提交和失败的记录
  const { submitted, failed } = readSubmittedAndFailed();
  console.log(`已成功提交: ${submitted.size}`);
  console.log(`之前失败: ${failed.size}`);
  
  // 3. 筛选候选策略（未跑的 + 失败的）
  const candidates = [];
  for (const file of allFiles) {
    const basename = path.basename(file);
    const relativePath = path.relative(path.dirname(SOURCE_DIR), file);
    
    // 跳过已成功提交的
    if (submitted.has(basename)) continue;
    
    const score = calculateScore(basename);
    const isFailed = failed.has(basename);
    
    candidates.push({
      file,
      relativePath,
      basename,
      score,
      isFailed,
      // 失败的策略稍微降低优先级
      finalScore: isFailed ? score - 0.5 : score
    });
  }
  
  console.log(`候选策略数: ${candidates.length}`);
  console.log(`  - 未跑过: ${candidates.filter(c => !c.isFailed).length}`);
  console.log(`  - 之前失败: ${candidates.filter(c => c.isFailed).length}`);
  
  // 4. 按分数排序，取前100
  candidates.sort((a, b) => {
    if (b.finalScore !== a.finalScore) {
      return b.finalScore - a.finalScore;
    }
    // 分数相同时，优先选未跑过的
    if (a.isFailed !== b.isFailed) {
      return a.isFailed ? 1 : -1;
    }
    // 最后按文件名排序
    return a.basename.localeCompare(b.basename, 'zh-Hans-CN');
  });
  
  const top100 = candidates.slice(0, 100);
  
  // 5. 输出结果
  const output = {
    generatedAt: new Date().toISOString(),
    totalCandidates: candidates.length,
    selected: top100.length,
    statistics: {
      newStrategies: top100.filter(c => !c.isFailed).length,
      retryFailed: top100.filter(c => c.isFailed).length,
      avgScore: (top100.reduce((sum, c) => sum + c.finalScore, 0) / top100.length).toFixed(2)
    },
    strategies: top100.map((c, idx) => ({
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
  console.log(`\n统计信息:`);
  console.log(`  - 新策略: ${output.statistics.newStrategies}`);
  console.log(`  - 重试失败: ${output.statistics.retryFailed}`);
  console.log(`  - 平均分数: ${output.statistics.avgScore}`);
  
  // 显示前10名
  console.log('\n前10名策略:');
  for (let i = 0; i < Math.min(10, top100.length); i++) {
    const s = top100[i];
    console.log(`  ${i + 1}. [${s.finalScore.toFixed(1)}分] ${s.isFailed ? '(重试)' : '(新)'} ${s.basename}`);
  }
}

main();
