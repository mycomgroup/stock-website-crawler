#!/usr/bin/env node
/**
 * 重新提交所有 error_exit 的策略（更新代码 + 重跑回测）
 * 从 NEW_STRATEGY_RESULTS.md 读取 error_exit 列表
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';
import { ensureRiceQuantSession } from '../../skills/ricequant_strategy/browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.join(__dirname, 'strategies');
const MAPPING_FILE = path.join(__dirname, 'rq_strategy_mapping.json');
const RESULTS_FILE = path.join(__dirname, 'NEW_STRATEGY_RESULTS.md');

const START_DATE = '2023-01-01';
const END_DATE = '2026-04-01';
const POLL_INTERVAL_MS = 15000;

function loadMapping() {
  try { return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8')); } catch { return {}; }
}
function saveMapping(m) {
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(m, null, 2));
}

// Parse error_exit files from results md
function getErrorFiles() {
  const content = fs.readFileSync(RESULTS_FILE, 'utf8');
  const matches = [...content.matchAll(/\| (rq_[^\|]+\.py) \|[^\|]+\|[^\|]+\| - \| - \| - \| - \| ❌ error_exit \|/g)];
  return matches.map(m => m[1].trim());
}

async function resubmitFile(client, filename, mapping) {
  const filepath = path.join(STRATEGIES_DIR, filename);
  if (!fs.existsSync(filepath)) {
    console.log(`  ⚠️  文件不存在: ${filename}`);
    return false;
  }
  const code = fs.readFileSync(filepath, 'utf8');
  const existing = mapping[filename];
  let strategyId = existing?.strategyId;

  // 1. Update or create strategy
  if (strategyId) {
    try {
      const ctx = await client.getStrategyContext(strategyId);
      const name = ctx?.name || filename.replace(/\.py$/, '');
      await client.saveStrategy(strategyId, name, code, ctx);
    } catch (e) {
      console.log(`  ✗ 更新失败: ${e.message.slice(0, 80)}, 新建...`);
      strategyId = null;
    }
  }
  if (!strategyId) {
    try {
      const name = `rq_${filename.replace(/\.py$/, '').slice(0, 50)}_${Date.now()}`;
      const res = await client.createStrategy(name, code);
      strategyId = res.strategy_id || res._id || res.id;
    } catch (e) {
      console.log(`  ✗ 新建失败: ${e.message.slice(0, 80)}`);
      return false;
    }
  }

  // 2. Get context
  let context;
  try {
    context = await client.getStrategyContext(strategyId);
  } catch (e) {
    console.log(`  ✗ 获取上下文失败: ${e.message.slice(0, 80)}`);
    return false;
  }

  // 3. Submit backtest with retry on rate limit
  let backtestId;
  for (let attempt = 0; attempt < 30; attempt++) {
    try {
      const btResult = await client.runBacktest(strategyId, code, {
        startTime: START_DATE, endTime: END_DATE,
        baseCapital: '100000', frequency: 'day', benchmark: '000300.XSHG',
      }, context);
      backtestId = btResult.backtestId || btResult._id || btResult.id;
      if (typeof backtestId === 'string') backtestId = backtestId.replace(/"/g, '');
      break;
    } catch (e) {
      if (e.message.includes('最大数量') || e.message.includes('403')) {
        process.stdout.write(`  ⏳ 等待槽位... (${attempt + 1}/30)\r`);
        await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
      } else {
        console.log(`  ✗ 回测提交失败: ${e.message.slice(0, 80)}`);
        return false;
      }
    }
  }

  if (!backtestId) {
    console.log(`  ✗ 超时放弃`);
    return false;
  }

  // 4. Update mapping
  mapping[filename] = { strategyId, backtestId: String(backtestId), submittedAt: new Date().toISOString() };
  saveMapping(mapping);
  console.log(`  ✓ 提交成功: backtest=${backtestId}`);
  return true;
}

async function main() {
  const errorFiles = getErrorFiles();
  console.log(`=== 重提交 error_exit 策略 ===`);
  console.log(`共 ${errorFiles.length} 个文件需要重提交\n`);

  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD,
  };
  const cookies = await ensureRiceQuantSession(credentials);
  const client = new RiceQuantClient({ cookies });
  const mapping = loadMapping();

  let success = 0, fail = 0;
  for (let i = 0; i < errorFiles.length; i++) {
    const filename = errorFiles[i];
    console.log(`[${i + 1}/${errorFiles.length}] ${filename}`);
    const ok = await resubmitFile(client, filename, mapping);
    if (ok) success++; else fail++;
    // Small delay between submissions
    if (i < errorFiles.length - 1) await new Promise(r => setTimeout(r, 1000));
  }

  console.log(`\n=== 完成 ===`);
  console.log(`成功: ${success}, 失败: ${fail}`);
  console.log(`运行 fetch_new_results.mjs 获取结果`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
