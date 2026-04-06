#!/usr/bin/env node
/**
 * 批量提交新策略 (rq_*) 到 RiceQuant
 * - 自动为每个文件创建新策略（不删除，保留在 RiceQuant 上）
 * - 并发控制：最多同时运行3个回测
 * - 不等待回测完成（--no-wait 模式）
 * - 记录 strategy_id -> backtest_id 映射
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';
import { ensureRiceQuantSession } from '../../skills/ricequant_strategy/browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const STRATEGIES_DIR = path.join(__dirname, 'strategies');
const LOG_FILE = path.join(__dirname, 'NEW_STRATEGY_SUBMISSIONS.md');
const MAPPING_FILE = path.join(__dirname, 'rq_strategy_mapping.json');

const START_DATE = '2023-01-01';
const END_DATE = '2026-04-01';
const MAX_CONCURRENT = 3;
const POLL_INTERVAL_MS = 15000;

// ------------------------------
// Helpers
// ------------------------------

function parseArgs() {
  const args = {};
  for (let i = 0; i < process.argv.length; i++) {
    const arg = process.argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = process.argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

function slugify(filename) {
  // rq_08_科技与狠活_纯粹的数据挖掘策略.py -> rq_08_ke_ji_yu_shen_huo
  return filename
    .replace(/\.py$/, '')
    .replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_')
    .replace(/_+/g, '_')
    .slice(0, 60);
}

function loadMapping() {
  if (fs.existsSync(MAPPING_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
    } catch {
      return {};
    }
  }
  return {};
}

function saveMapping(mapping) {
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(mapping, null, 2));
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 获取目录下所有 rq_* .py 文件（排除 01-56 编号的文件）
function getNewStrategyFiles() {
  const files = fs.readdirSync(STRATEGIES_DIR)
    .filter(f => f.endsWith('.py'))
    .filter(f => f.startsWith('rq_'))
    .sort();
  return files;
}

// 更新日志文件
function updateLogFile(entries) {
  let content = `# 新策略批量提交记录\n`;
  content += `> 提交时间: ${new Date().toLocaleString()}\n`;
  content += `> 回测区间: ${START_DATE} 至 ${END_DATE}\n\n`;
  content += `| 策略文件 | StrategyID | BacktestID | 状态 |\n`;
  content += `|----------|------------|------------|------|\n`;

  for (const e of entries) {
    content += `| ${e.filename} | ${e.strategyId || '-'} | ${e.backtestId || '-'} | ${e.status} |\n`;
  }

  fs.writeFileSync(LOG_FILE, content);
}

// ------------------------------
// 核心提交逻辑
// ------------------------------

async function submitStrategy(client, filename) {
  const filepath = path.join(STRATEGIES_DIR, filename);
  const code = fs.readFileSync(filepath, 'utf8');
  const strategyName = `rq_${slugify(filename)}_${Date.now()}`;

  // 1. 创建策略
  let strategyId;
  try {
    const createResult = await client.createStrategy(strategyName, code);
    strategyId = createResult.strategy_id || createResult._id || createResult.id;
    if (!strategyId) {
      return { filename, strategyId: null, backtestId: null, status: `❌ 创建失败: ${JSON.stringify(createResult).slice(0, 100)}` };
    }
  } catch (e) {
    return { filename, strategyId: null, backtestId: null, status: `❌ 创建异常: ${e.message.slice(0, 100)}` };
  }

  // 2. 获取策略上下文（用于 runBacktest）
  let context;
  try {
    context = await client.getStrategyContext(strategyId);
  } catch (e) {
    return { filename, strategyId, backtestId: null, status: `❌ 获取上下文失败: ${e.message.slice(0, 100)}` };
  }

  // 3. 提交回测
  let backtestId;
  try {
    const btResult = await client.runBacktest(strategyId, code, {
      startTime: START_DATE,
      endTime: END_DATE,
      baseCapital: '100000',
      frequency: 'day',
      benchmark: '000300.XSHG'
    }, context);

    backtestId = btResult.backtestId || btResult._id || btResult.id;
    if (typeof backtestId === 'string') {
      backtestId = backtestId.replace(/"/g, '');
    }

    if (!backtestId) {
      return { filename, strategyId, backtestId: null, status: `❌ 回测提交失败: ${JSON.stringify(btResult).slice(0, 100)}` };
    }
  } catch (e) {
    return { filename, strategyId, backtestId: null, status: `❌ 回测异常: ${e.message.slice(0, 100)}` };
  }

  return { filename, strategyId, backtestId, status: '🔄 已提交' };
}

// ------------------------------
// 主流程
// ------------------------------

async function main() {
  const args = parseArgs();
  const noWait = !args.wait; // 默认不等待

  console.log('============================================================');
  console.log('RiceQuant 新策略批量提交 (rq_* 文件)');
  console.log('============================================================');
  console.log('回测区间:', START_DATE, '至', END_DATE);
  console.log('并发数:', MAX_CONCURRENT);
  console.log('等待模式:', noWait ? '不等待回测完成' : '等待回测完成');
  console.log('============================================================\n');

  // 1. 确保登录
  console.log('[1] 检查登录状态...');
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  };
  const cookies = await ensureRiceQuantSession(credentials);
  console.log('    登录成功, cookies:', cookies.length);

  const client = new RiceQuantClient({ cookies });

  // 2. 扫描文件
  const allFiles = getNewStrategyFiles();
  console.log(`\n[2] 扫描到 ${allFiles.length} 个 rq_* 策略文件`);

  // 3. 加载已提交记录，幂等跳过
  const mapping = loadMapping();
  const alreadyDone = new Set(Object.keys(mapping).filter(k => mapping[k].backtestId));
  const todoFiles = allFiles.filter(f => !alreadyDone.has(f));
  console.log(`    已提交: ${alreadyDone.size}，待提交: ${todoFiles.length}\n`);

  if (todoFiles.length === 0) {
    console.log('没有新文件需要提交。');
    return;
  }

  // 4. 分批提交（每批 MAX_CONCURRENT）
  const results = allFiles.map(f => ({
    filename: f,
    strategyId: mapping[f]?.strategyId || null,
    backtestId: mapping[f]?.backtestId || null,
    status: mapping[f]?.backtestId ? `🔄 已提交` : '⏳ 待提交'
  }));

  let submitted = 0;
  let batchNum = 0;

  while (submitted < todoFiles.length) {
    // 等待容量
    const runningCount = await client.getRunningBacktestCount();
    if (runningCount >= MAX_CONCURRENT) {
      process.stdout.write(`    [等待] 运行中: ${runningCount}/${MAX_CONCURRENT}，等待中...\r`);
      await sleep(POLL_INTERVAL_MS);
      continue;
    }

    // 提交一批
    const batch = todoFiles.slice(submitted, submitted + (MAX_CONCURRENT - runningCount));
    batchNum++;
    console.log(`\n[Batch ${batchNum}] 提交 ${batch.length} 个策略...`);

    const promises = batch.map(async (filename) => {
      const result = await submitStrategy(client, filename);

      // 更新 mapping
      mapping[filename] = {
        strategyId: result.strategyId,
        backtestId: result.backtestId,
        submittedAt: new Date().toISOString()
      };
      saveMapping(mapping);

      // 更新 results 并刷新日志
      const idx = results.findIndex(r => r.filename === filename);
      if (idx !== -1) {
        results[idx] = result;
      }
      updateLogFile(results);

      if (result.backtestId) {
        console.log(`    ✓ ${filename} -> strategy:${result.strategyId} backtest:${result.backtestId}`);
      } else {
        console.log(`    ✗ ${filename}: ${result.status}`);
      }

      return result;
    });

    await Promise.all(promises);
    submitted += batch.length;

    // 每批之间稍作等待
    if (submitted < todoFiles.length) {
      await sleep(5000);
    }
  }

  console.log('\n============================================================');
  console.log(`全部提交完成！共 ${allFiles.length} 个策略`);
  console.log(`日志文件: ${LOG_FILE}`);
  console.log(`映射文件: ${MAPPING_FILE}`);
  console.log('============================================================');

  if (!noWait) {
    console.log('\n正在等待所有回测完成...');
    // 可选：等待所有完成（仅在 --wait 时）
  }
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
