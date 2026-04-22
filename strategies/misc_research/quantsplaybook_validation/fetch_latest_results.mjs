#!/usr/bin/env node
/**
 * 按 strategyId 拉取每个策略的最新回测结果（不依赖 mapping 里的 backtestId）
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';
import { ensureRiceQuantSession } from '../../skills/ricequant_strategy/browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.join(__dirname, 'strategies');
const MAPPING_FILE = path.join(__dirname, 'rq_strategy_mapping.json');
const RESUBMIT_RESULTS_FILE = path.join(__dirname, 'RESUBMIT_RESULTS.md');
const OUTPUT_FILE = path.join(__dirname, 'NEW_STRATEGY_RESULTS.md');
const filenameCollator = new Intl.Collator('zh-Hans-CN', { numeric: true, sensitivity: 'base' });

function loadMapping() {
  try { return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8')); } catch { return {}; }
}

function loadResubmitStatuses() {
  try {
    const text = fs.readFileSync(RESUBMIT_RESULTS_FILE, 'utf8');
    const map = new Map();
    for (const line of text.split('\n')) {
      if (!line.startsWith('| rq_')) continue;
      const parts = line.split('|').map(part => part.trim()).filter(Boolean);
      if (parts.length < 4) continue;
      map.set(parts[0], parts[3]);
    }
    return map;
  } catch {
    return new Map();
  }
}

function fmtPct(v) {
  if (v == null || isNaN(v)) return '-';
  return (v * 100).toFixed(2) + '%';
}
function fmtNum(v, d = 3) {
  if (v == null || isNaN(v)) return '-';
  return v.toFixed(d);
}
function fmtTime(v) {
  if (!v) return '-';
  const dt = new Date(v);
  if (Number.isNaN(dt.getTime())) return String(v);
  return dt.toLocaleString('zh-CN', { hour12: false });
}
function fileExists(filename) {
  return fs.existsSync(path.join(STRATEGIES_DIR, filename));
}
function summarizeResubmitStatus(status) {
  if (!status) return '-';
  if (status.includes('文件不存在')) return '⚠️ 文件不存在';
  if (status.includes('获取上下文失败')) return '❌ 获取上下文失败';
  if (status.includes('提交异常')) return '❌ 提交异常';
  if (status.includes('已提交')) return '🔄 已提交';
  return status;
}
function normalizeMapping(mapping) {
  const normalized = {};
  for (const filename of Object.keys(mapping).sort((a, b) => filenameCollator.compare(a, b))) {
    const info = mapping[filename] || {};
    const ordered = {};
    for (const key of ['strategyId', 'backtestId', 'submittedAt', 'resubmittedAt', 'lastFetched']) {
      if (info[key] != null) ordered[key] = info[key];
    }
    ordered.localFileExists = fileExists(filename);
    for (const key of Object.keys(info).sort()) {
      if (!(key in ordered)) ordered[key] = info[key];
    }
    normalized[filename] = ordered;
  }
  return normalized;
}

async function main() {
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD,
  };
  const cookies = await ensureRiceQuantSession(credentials);
  const client = new RiceQuantClient({ cookies });
  const mapping = loadMapping();
  const resubmitStatuses = loadResubmitStatuses();

  const entries = Object.entries(mapping)
    .filter(([, v]) => v.strategyId)
    .sort(([a], [b]) => filenameCollator.compare(a, b));
  console.log(`共 ${entries.length} 个策略，按 strategyId 拉最新回测...\n`);

  const rows = [];
  const BATCH = 5;

  for (let i = 0; i < entries.length; i += BATCH) {
    const batch = entries.slice(i, i + BATCH);
    await Promise.all(batch.map(async ([filename, info]) => {
      try {
        const { backtestId, result } = await client.getLatestBacktestResult(info.strategyId);
        const status = result?.status || 'unknown';
        const summary = result?.summary || {};
        const ret = summary.algorithm_return ?? summary.total_returns ?? null;
        const annual = summary.annualized_returns ?? null;
        const sharpe = summary.sharpe ?? null;
        const maxdd = summary.max_drawdown ?? null;
        const localFileExists = fileExists(filename);
        const resubmitStatus = summarizeResubmitStatus(resubmitStatuses.get(filename));

        // Update mapping with latest backtestId
        mapping[filename].backtestId = String(backtestId);
        mapping[filename].lastFetched = new Date().toISOString();

        if (status === 'done' || status === 'complete' || status === 'normal_exit') {
          console.log(`✓ ${filename}: ret=${fmtPct(ret)}, sharpe=${fmtNum(sharpe)}`);
          rows.push({
            filename,
            strategyId: info.strategyId,
            backtestId,
            ret,
            annual,
            sharpe,
            maxdd,
            fetchStatus: '✅ 完成',
            localFileExists,
            submittedAt: info.submittedAt,
            resubmittedAt: info.resubmittedAt,
            resubmitStatus
          });
        } else if (status === 'error_exit') {
          console.log(`❌ ${filename}: error_exit`);
          rows.push({
            filename,
            strategyId: info.strategyId,
            backtestId,
            ret: null,
            annual: null,
            sharpe: null,
            maxdd: null,
            fetchStatus: '❌ error_exit',
            localFileExists,
            submittedAt: info.submittedAt,
            resubmittedAt: info.resubmittedAt,
            resubmitStatus
          });
        } else if (status === 'running') {
          console.log(`⏳ ${filename}: running`);
          rows.push({
            filename,
            strategyId: info.strategyId,
            backtestId,
            ret: null,
            annual: null,
            sharpe: null,
            maxdd: null,
            fetchStatus: '⏳ 运行中',
            localFileExists,
            submittedAt: info.submittedAt,
            resubmittedAt: info.resubmittedAt,
            resubmitStatus
          });
        } else {
          rows.push({
            filename,
            strategyId: info.strategyId,
            backtestId,
            ret: null,
            annual: null,
            sharpe: null,
            maxdd: null,
            fetchStatus: `❓ ${status}`,
            localFileExists,
            submittedAt: info.submittedAt,
            resubmittedAt: info.resubmittedAt,
            resubmitStatus
          });
        }
      } catch (e) {
        rows.push({
          filename,
          strategyId: info.strategyId,
          backtestId: info.backtestId,
          ret: null,
          annual: null,
          sharpe: null,
          maxdd: null,
          fetchStatus: '⚠️ 拉取失败',
          localFileExists: fileExists(filename),
          submittedAt: info.submittedAt,
          resubmittedAt: info.resubmittedAt,
          resubmitStatus: summarizeResubmitStatus(resubmitStatuses.get(filename)),
          fetchError: e?.message || 'unknown'
        });
      }
    }));
    process.stdout.write(`  进度: ${Math.min(i + BATCH, entries.length)}/${entries.length}\r`);
    await new Promise(r => setTimeout(r, 500));
  }

  // Save updated mapping
  const normalizedMapping = normalizeMapping(mapping);
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(normalizedMapping, null, 2));

  // Write results MD
  const now = new Date().toLocaleString();
  const done = rows.filter(r => r.fetchStatus === '✅ 完成').length;
  const errors = rows.filter(r => r.fetchStatus.includes('error_exit')).length;
  const running = rows.filter(r => r.fetchStatus.includes('运行中')).length;
  const fetchFailed = rows.filter(r => r.fetchStatus === '⚠️ 拉取失败').length;
  const localMissing = rows.filter(r => !r.localFileExists).length;
  const resubmitContextFailed = rows.filter(r => r.resubmitStatus === '❌ 获取上下文失败').length;
  const resubmitFileMissing = rows.filter(r => r.resubmitStatus === '⚠️ 文件不存在').length;

  let md = `# 新策略回测结果（整理版）\n`;
  md += `> 更新时间: ${now}\n`;
  md += `> 说明: 当前页面以 \`rq_strategy_mapping.json\` 为准，优先展示策略和平台映射关系。本轮 RiceQuant 结果拉取统一失败时，不再把整页写成“策略失败”。\n\n`;
  md += `## 汇总\n\n`;
  md += `| 指标 | 数量 |\n`;
  md += `|------|------|\n`;
  md += `| 映射总数 | ${rows.length} |\n`;
  md += `| StrategyID 完整 | ${rows.filter(r => r.strategyId).length} |\n`;
  md += `| BacktestID 完整 | ${rows.filter(r => r.backtestId).length} |\n`;
  md += `| 本地文件存在 | ${rows.length - localMissing} |\n`;
  md += `| 本地文件缺失 | ${localMissing} |\n`;
  md += `| 本轮拉取完成 | ${done} |\n`;
  md += `| 本轮拉取 error_exit | ${errors} |\n`;
  md += `| 本轮拉取运行中 | ${running} |\n`;
  md += `| 本轮拉取失败 | ${fetchFailed} |\n`;
  md += `| 曾记录 resubmittedAt | ${rows.filter(r => r.resubmittedAt).length} |\n`;
  md += `| 原路径重提上下文失败 | ${resubmitContextFailed} |\n`;
  md += `| 原路径重提本地文件缺失 | ${resubmitFileMissing} |\n\n`;

  md += `## 明细\n\n`;
  md += `| 策略文件 | 本地文件 | StrategyID | BacktestID | 首次提交 | 最近重提 | 本轮拉取 | 原路径重提 | 收益率 | 年化 | 夏普 | 最大回撤 |\n`;
  md += `|----------|----------|------------|------------|----------|----------|----------|------------|--------|------|------|----------|\n`;

  for (const r of rows) {
    const retStr = r.ret != null ? (r.ret > 0 ? `**${fmtPct(r.ret)}**` : fmtPct(r.ret)) : '-';
    const link = r.backtestId ? `[${r.backtestId}](https://www.ricequant.com/quant/backtest/${r.backtestId})` : '-';
    const fileStatus = r.localFileExists ? '✅' : '❌';
    md += `| ${r.filename} | ${fileStatus} | ${r.strategyId} | ${link} | ${fmtTime(r.submittedAt)} | ${fmtTime(r.resubmittedAt)} | ${r.fetchStatus} | ${r.resubmitStatus} | ${retStr} | ${fmtPct(r.annual)} | ${fmtNum(r.sharpe)} | ${fmtPct(r.maxdd)} |\n`;
  }

  fs.writeFileSync(OUTPUT_FILE, md);

  console.log(`\n=== 汇总 ===`);
  console.log(`✅ 完成: ${done}`);
  console.log(`❌ error_exit: ${errors}`);
  console.log(`⏳ 运行中: ${running}`);
  console.log(`⚠️ 拉取失败: ${fetchFailed}`);
  console.log(`📁 本地文件缺失: ${localMissing}`);
  console.log(`结果已写入 ${OUTPUT_FILE}`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
