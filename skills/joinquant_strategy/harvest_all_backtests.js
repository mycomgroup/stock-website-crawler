#!/usr/bin/env node
/**
 * harvest_all_backtests.js
 *
 * 拉取平台上所有策略的所有历史回测结果，筛选已完成的，
 * 按综合收益评分排序，输出 JSON + Markdown 报告。
 *
 * 用法：
 *   node harvest_all_backtests.js
 *   node harvest_all_backtests.js --out ./data/my_harvest
 *   node harvest_all_backtests.js --top 100
 */

import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT } from './paths.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { parseArgs } from './utils/cli.js';

// ── Helpers ───────────────────────────────────────────────────────────────────
function pct(v) {
  if (v == null || isNaN(v)) return 'N/A';
  return `${(Number(v) * 100).toFixed(2)}%`;
}
function num(v, d = 3) {
  if (v == null || isNaN(v)) return 'N/A';
  return Number(v).toFixed(d);
}

/**
 * 综合评分（越高越好）
 * 主要看年化收益，同时用夏普和回撤做修正：
 *   score = annualized_returns * sharpe_bonus * drawdown_penalty
 *
 * sharpe_bonus  = clamp(sharpe / 1.5, 0.5, 2.0)
 * drawdown_penalty = clamp(1 - max_drawdown, 0.3, 1.0)
 *   （回撤越大扣分越多，但不会把好策略完全压死）
 */
function score(row) {
  const ann = Number(row.annualizedReturns) || 0;
  const sharpe = Number(row.sharpe) || 0;
  const dd = Math.abs(Number(row.maxDrawdown) || 0);

  const sharpeFactor = Math.min(Math.max(sharpe / 1.5, 0.5), 2.0);
  const ddFactor = Math.min(Math.max(1 - dd, 0.3), 1.0);
  return ann * sharpeFactor * ddFactor;
}

function extractSummary(stats) {
  // stats 来自 getBacktestStats，数据在 stats.data
  // stats 结构: { data: {...}, status: "0", code: "00000" }
  const d = stats?.data || {};
  return {
    totalReturns: d.algorithm_return,
    annualizedReturns: d.annual_algo_return,
    sharpe: d.sharpe,
    maxDrawdown: d.max_drawdown,
    alpha: d.alpha,
    beta: d.beta,
    winRate: d.win_ratio,
  };
}

function isCompleted(stats) {
  // status 可能是数字 0 或字符串 "0"，都表示成功
  return (stats?.status == 0 || stats?.status === '0') && stats?.data?.annual_algo_return != null;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const args = parseArgs(process.argv.slice(2), { top: 100 });
  const topN = Number(args.top || 100);
  const outDir = path.resolve(
    args.out || path.join(DATA_ROOT, `harvest_${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`)
  );
  fs.mkdirSync(outDir, { recursive: true });

  console.log('确保 session 有效...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();

  // Step 1: 列出所有策略
  console.log('\n[1/3] 拉取策略列表...');
  const strategies = await client.listStrategies();
  console.log(`  找到策略: ${strategies.length} 个`);
  if (strategies.length === 0) {
    console.error('未找到任何策略，请检查 session 是否有效。');
    process.exit(1);
  }

  // Step 2: 每个策略拉取回测列表（按 algorithmId 去重，避免重复拉取）
  console.log('\n[2/3] 拉取各策略的回测列表...');
  const allBacktests = []; // { strategyId, strategyName, backtestId, backtestName, startDate, endDate, createdAt, status }
  const seenAlgoIds = new Set();
  const seenBacktestIds = new Set();

  for (let i = 0; i < strategies.length; i++) {
    const strat = strategies[i];
    if (seenAlgoIds.has(strat.id)) {
      console.log(`  [${i + 1}/${strategies.length}] ${strat.name} ... 跳过(重复 algorithmId)`);
      continue;
    }
    seenAlgoIds.add(strat.id);
    process.stdout.write(`  [${i + 1}/${strategies.length}] ${strat.name} ... `);
    try {
      const bts = await client.getBacktests(strat.id);
      let added = 0;
      for (const bt of bts) {
        if (seenBacktestIds.has(bt.id)) continue;
        seenBacktestIds.add(bt.id);
        allBacktests.push({
          strategyId: strat.id,
          strategyName: strat.name,
          backtestId: bt.id,
          backtestName: bt.name,
          backtestStatus: bt.status,
          startDate: bt.startDate,
          endDate: bt.endDate,
          createdAt: bt.createdAt,
        });
        added++;
      }
      process.stdout.write(`${bts.length} 条 (新增 ${added})\n`);
    } catch (err) {
      process.stdout.write(`失败: ${err.message}\n`);
    }
    await new Promise(r => setTimeout(r, 200));
  }

  console.log(`\n  共发现回测记录: ${allBacktests.length} 条`);

  // Step 3: 拉取每条回测的结果（只处理 HTML 列表里 status=2 的已完成回测）
  console.log('\n[3/3] 拉取回测结果...');
  const toFetch = allBacktests.filter(b => b.backtestStatus === '2');
  const skippedNotDone = allBacktests.filter(b => b.backtestStatus !== '2');
  console.log(`  已完成(status=2): ${toFetch.length} 条，跳过未完成: ${skippedNotDone.length} 条`);

  const completed = [];
  const skipped = [...skippedNotDone.map(b => ({ ...b, state: `html_status_${b.backtestStatus}` }))];
  const contextCache = new Map();

  for (let i = 0; i < toFetch.length; i++) {
    const item = toFetch[i];
    process.stdout.write(`  [${i + 1}/${toFetch.length}] ${item.backtestName} ... `);
    try {
      // getBacktestStats 不需要 token，直接传空 context
      const stats = await client.getBacktestStats(item.backtestId, {});
      const summary = extractSummary(stats);

      if (isCompleted(stats)) {
        const row = {
          strategyName: item.strategyName,
          backtestName: item.backtestName,
          createdAt: item.createdAt,
          backtestId: item.backtestId,
          backtestUrl: `https://www.joinquant.com/algorithm/backtest?backtestId=${item.backtestId}`,
          startDate: item.startDate || summary.startDate,
          endDate: item.endDate || summary.endDate,
          totalReturns: summary.totalReturns,
          annualizedReturns: summary.annualizedReturns,
          sharpe: summary.sharpe,
          maxDrawdown: summary.maxDrawdown,
          alpha: summary.alpha,
          beta: summary.beta,
          winRate: summary.winRate,
          _score: score(summary),
        };
        completed.push(row);
        process.stdout.write(`✓ 年化=${pct(summary.annualizedReturns)} 夏普=${num(summary.sharpe,2)}\n`);
      } else {
        skipped.push({ ...item, state: `stats_no_data` });
        process.stdout.write(`跳过 (无数据)\n`);
      }
    } catch (err) {
      skipped.push({ ...item, state: 'fetch_error', error: err.message });
      process.stdout.write(`错误: ${err.message}\n`);
    }
    await new Promise(r => setTimeout(r, 150));
  }

  // 按综合评分降序
  completed.sort((a, b) => b._score - a._score);

  // ── 输出 JSON ──
  const jsonOut = path.join(outDir, 'harvest_results.json');
  fs.writeFileSync(jsonOut, JSON.stringify({
    generatedAt: new Date().toISOString(),
    totals: { strategies: strategies.length, allBacktests: allBacktests.length, completed: completed.length, skipped: skipped.length },
    top: completed.slice(0, topN),
    all: completed,
    skipped,
  }, null, 2));

  // ── 输出 Markdown ──
  const mdOut = path.join(outDir, 'harvest_results.md');
  const lines = [];
  lines.push('# 聚宽历史回测收益排行');
  lines.push(`> 生成时间: ${new Date().toISOString()}`);
  lines.push(`> 策略数: ${strategies.length}  |  回测总数: ${allBacktests.length}  |  已完成: ${completed.length}  |  跳过/失败: ${skipped.length}`);
  lines.push('');
  lines.push('> 综合评分 = 年化收益 × 夏普修正系数 × 回撤惩罚系数');
  lines.push('');
  lines.push(`## Top ${Math.min(topN, completed.length)} 策略`);
  lines.push('');
  lines.push('| # | 策略名 | 回测名 | 回测时间 | 时间区间 | 累计收益 | 年化收益 | 夏普 | 最大回撤 | Alpha | Beta | 胜率 | 评分 | 链接 |');
  lines.push('|---|--------|--------|----------|----------|----------|----------|------|----------|-------|------|------|------|------|');

  completed.slice(0, topN).forEach((r, idx) => {
    lines.push(
      `| ${idx + 1} | ${r.strategyName.replace(/\|/g, '/')} | ${r.backtestName.replace(/\|/g, '/')} | ${r.createdAt || ''} | ${r.startDate || ''}~${r.endDate || ''} | ${pct(r.totalReturns)} | ${pct(r.annualizedReturns)} | ${num(r.sharpe, 2)} | ${pct(r.maxDrawdown)} | ${pct(r.alpha)} | ${num(r.beta, 2)} | ${pct(r.winRate)} | ${num(r._score, 3)} | [打开](${r.backtestUrl}) |`
    );
  });

  lines.push('');
  lines.push('---');
  lines.push(`完整数据见: \`${jsonOut}\``);

  fs.writeFileSync(mdOut, lines.join('\n'));

  console.log('\n✅ 完成！');
  console.log(`   已完成回测: ${completed.length} 条`);
  console.log(`   JSON: ${jsonOut}`);
  console.log(`   Markdown: ${mdOut}`);
}

main().catch(err => {
  console.error('执行失败:', err.message);
  process.exit(1);
});
