#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATE_TAG = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const DEFAULT_RUN_DIR = path.resolve(__dirname, 'data', `jq558_batch_${DATE_TAG}`);

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function formatPct(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '';
  return `${(Number(value) * 100).toFixed(2)}%`;
}

function formatNum(value, digits = 3) {
  if (value === null || value === undefined || Number.isNaN(value)) return '';
  return Number(value).toFixed(digits);
}

function readSubmittedItems(jsonlPath) {
  const items = [];
  if (!fs.existsSync(jsonlPath)) return items;
  const seen = new Set();
  const lines = fs.readFileSync(jsonlPath, 'utf8').split('\n').filter(Boolean);
  for (const line of lines) {
    try {
      const item = JSON.parse(line);
      if (item.status !== 'submitted' || !item.backtestId) continue;
      if (seen.has(item.backtestId)) continue;
      seen.add(item.backtestId);
      items.push(item);
    } catch {
      // Ignore malformed lines.
    }
  }
  return items;
}

function extractSummary(result) {
  const data = result?.data || {};
  const summary = data?.result?.summary || {};
  const backtest = data?.result?.backtest || data?.backtest || {};
  return {
    state: data.state || backtest.status || result?.status || '',
    totalReturns: summary.total_returns,
    annualizedReturns: summary.annualized_returns,
    sharpe: summary.sharpe,
    maxDrawdown: summary.max_drawdown,
    alpha: summary.alpha,
    beta: summary.beta,
    winRate: summary.win_rate
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const runDir = path.resolve(args.dir || DEFAULT_RUN_DIR);
  const jsonlPath = path.join(runDir, 'submissions.jsonl');
  const outputJson = path.join(runDir, 'results_snapshot.json');
  const outputMd = path.join(runDir, 'results_snapshot.md');

  const items = readSubmittedItems(jsonlPath);
  if (items.length === 0) {
    throw new Error(`No submitted backtests found in ${jsonlPath}`);
  }

  console.log(`发现已提交回测: ${items.length}`);
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();

  const completed = [];
  const pending = [];
  const failed = [];

  for (let i = 0; i < items.length; i += 1) {
    const item = items[i];
    console.log(`[${i + 1}/${items.length}] ${item.relativePath}`);
    try {
      const context = await client.getStrategyContext(item.algorithmId);
      const result = await client.getBacktestResult(item.backtestId, context);
      const summary = extractSummary(result);
      const row = {
        file: item.relativePath,
        strategyName: item.strategyName,
        algorithmId: item.algorithmId,
        backtestId: item.backtestId,
        backtestUrl: item.backtestUrl,
        state: summary.state,
        totalReturns: summary.totalReturns,
        annualizedReturns: summary.annualizedReturns,
        sharpe: summary.sharpe,
        maxDrawdown: summary.maxDrawdown,
        alpha: summary.alpha,
        beta: summary.beta,
        winRate: summary.winRate
      };

      if (summary.totalReturns !== undefined || summary.annualizedReturns !== undefined) {
        completed.push(row);
      } else if (String(summary.state).toLowerCase().includes('fail') || result?.status === 'error') {
        failed.push(row);
      } else {
        pending.push(row);
      }
    } catch (error) {
      failed.push({
        file: item.relativePath,
        strategyName: item.strategyName,
        algorithmId: item.algorithmId,
        backtestId: item.backtestId,
        backtestUrl: item.backtestUrl,
        state: 'fetch_error',
        error: error.message
      });
    }
  }

  completed.sort((a, b) => (b.totalReturns ?? -Infinity) - (a.totalReturns ?? -Infinity));

  const payload = {
    generatedAt: new Date().toISOString(),
    runDir,
    totals: {
      submitted: items.length,
      completed: completed.length,
      pending: pending.length,
      failed: failed.length
    },
    completed,
    pending,
    failed
  };
  fs.writeFileSync(outputJson, JSON.stringify(payload, null, 2), 'utf8');

  const lines = [];
  lines.push('# JQ558 最近1年回测结果快照');
  lines.push(`> 生成时间: ${payload.generatedAt}`);
  lines.push(`> 运行目录: ${runDir}`);
  lines.push('');
  lines.push(`- 已提交: ${items.length}`);
  lines.push(`- 已完成: ${completed.length}`);
  lines.push(`- 运行中/排队中: ${pending.length}`);
  lines.push(`- 失败: ${failed.length}`);
  lines.push('');
  lines.push('## 已完成前50名');
  lines.push('');
  lines.push('| 排名 | 文件 | 累计收益 | 年化收益 | 夏普 | 最大回撤 | Alpha | Beta | 胜率 |');
  lines.push('|------|------|----------|----------|------|----------|-------|------|------|');

  completed.slice(0, 50).forEach((row, index) => {
    lines.push(
      `| ${index + 1} | ${row.file.replace(/\|/g, '/')} | ${formatPct(row.totalReturns)} | ${formatPct(row.annualizedReturns)} | ${formatNum(row.sharpe)} | ${formatPct(row.maxDrawdown)} | ${formatPct(row.alpha)} | ${formatNum(row.beta)} | ${formatPct(row.winRate)} |`
    );
  });

  if (pending.length) {
    lines.push('');
    lines.push('## 仍在运行或排队');
    lines.push('');
    lines.push('| 文件 | BacktestID | 状态 |');
    lines.push('|------|------------|------|');
    pending.slice(0, 100).forEach((row) => {
      lines.push(`| ${row.file.replace(/\|/g, '/')} | ${row.backtestId} | ${row.state || 'pending'} |`);
    });
  }

  if (failed.length) {
    lines.push('');
    lines.push('## 拉取失败或回测失败');
    lines.push('');
    lines.push('| 文件 | BacktestID | 状态 | 备注 |');
    lines.push('|------|------------|------|------|');
    failed.slice(0, 100).forEach((row) => {
      lines.push(`| ${row.file.replace(/\|/g, '/')} | ${row.backtestId || ''} | ${row.state || 'failed'} | ${(row.error || '').replace(/\|/g, '/')} |`);
    });
  }

  fs.writeFileSync(outputMd, lines.join('\n'), 'utf8');

  console.log(`结果 JSON: ${outputJson}`);
  console.log(`结果 Markdown: ${outputMd}`);
}

main().catch((error) => {
  console.error('汇总失败:', error.message);
  process.exit(1);
});
