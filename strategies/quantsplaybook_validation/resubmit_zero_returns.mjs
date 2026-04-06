#!/usr/bin/env node
/**
 * 重新提交所有收益为 0.00% 的策略（完成但无交易）
 * 从 NEW_STRATEGY_RESULTS.md 读取 0.00% 收益列表
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
const MAX_CONCURRENT = 3;
const TARGET_FILES = new Set(process.argv.slice(2));
const MINUTE_FREQUENCY_FILES = new Set([
  'rq_32_追高概率涨停.py',
  'rq_55_怎么让龟速变奔跑以首版突破一进二为例.py',
  'rq_78 首板低开策略-终极版 最大回撤15%，年化50%.py',
  'rq_83_开盘幅度决定日内方向.py',
  'rq_91_ETF-T0动量策略年化18回撤3.31.py',
  'rq_93_234板介入-2023年14倍-无未来.py',
  'rq_96_集合竞价量比策略V1.py',
  'rq_99_韶华研究之二十_竞价异动.py'
]);
const DAY_FREQUENCY_FILES = new Set([
  'rq_10_龙头首阴战法改版二.py',
  'rq_10_10倍_二板排板战法优化.py',
  'rq_13_首板高开_低开_弱转强混合策略.py',
  'rq_13_涨停研究三_连板股票收益统计与回测.py',
  'rq_14_胜率65_缩量分歧反包战法.py',
  'rq_14_为实盘做的更新_分钟级别和盘中止损.py',
  'rq_16_集合竞价三合一_今年收益1067_年化198.py',
  'rq_32_追高概率涨停.py',
  'rq_77 龙头弱转强战法.py',
  'rq_86_最新解密追涨龙头打板策略.py',
  'rq_86_预判st并过滤避雷代码740.py',
  'rq_88_打首板策略今年收益达到40绝无未来函数.py',
  'rq_88_WY大神的龙头打板策略小改.py',
  'rq_89_2020年效果很好的策略龙回头策略v3.0.py',
  'rq_93_234板介入-2023年14倍-无未来.py',
  'rq_95_冲天炮最高板策略迭代.py',
  'rq_99_韶华研究之二十_竞价异动.py',
  'rq_02_02_龙头底分型战法-两年23倍.py',
  'rq_08_14个月200_超短线实盘交易策略_无未来函数.py',
  'rq_65_低开买入小市值策略高频交易法3.0总结.py',
  'rq_94_小资金短线策略.py',
  'rq_96_首版加2版龙虎榜挖掘V2_0_年化1400.py',
  'rq_98_追涨大师超额142.py'
]);

function loadMapping() {
  try { return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8')); } catch { return {}; }
}
function saveMapping(m) {
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(m, null, 2));
}

function inferFrequency(filename, code) {
  if (DAY_FREQUENCY_FILES.has(filename)) return 'day';
  if (MINUTE_FREQUENCY_FILES.has(filename)) return '1m';
  if (/(竞价|开盘|打板|首板|一进二|龙头|日内|T0|T-?0|高频)/.test(filename)) {
    return '1m';
  }
  if (/market_open\(minute=|market_open\(hour=|scheduler\.run_daily\(.+market_open/.test(code)) {
    return '1m';
  }
  return 'day';
}

// 从 results md 中解析收益为 0.00% 的策略文件名
function getZeroReturnFiles() {
  const content = fs.readFileSync(RESULTS_FILE, 'utf8');
  const rows = content.split('\n').filter(line => line.startsWith('| rq_'));
  const files = [];
  for (const row of rows) {
    const cols = row.split('|').map(s => s.trim()).filter(Boolean);
    if (cols.length < 8) continue;
    const filename = cols[0];
    const localExists = cols[1];
    const latestStatus = cols[6];
    const totalReturn = cols[8] || '';
    if (localExists !== '✅') continue;
    if (latestStatus !== '✅ 完成') continue;
    if (totalReturn !== '0.00%') continue;
    if (TARGET_FILES.size > 0 && !TARGET_FILES.has(filename)) continue;
    files.push(filename);
  }
  return files;
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function resubmitFile(client, filename, mapping) {
  const filepath = path.join(STRATEGIES_DIR, filename);
  if (!fs.existsSync(filepath)) {
    console.log(`  ⚠️  文件不存在: ${filename}`);
    return false;
  }
  const code = fs.readFileSync(filepath, 'utf8');
  const frequency = inferFrequency(filename, code);
  const existing = mapping[filename];
  let strategyId = existing?.strategyId;

  // 1. 更新或新建策略
  if (strategyId) {
    try {
      const ctx = await client.getStrategyContext(strategyId);
      const name = ctx?.name || filename.replace(/\.py$/, '');
      await client.saveStrategy(strategyId, name, code, ctx);
    } catch (e) {
      console.log(`  ⚠️  更新失败: ${e.message.slice(0, 80)}, 尝试新建...`);
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

  // 2. 获取上下文
  let context;
  try {
    context = await client.getStrategyContext(strategyId);
  } catch (e) {
    console.log(`  ✗ 获取上下文失败: ${e.message.slice(0, 80)}`);
    return false;
  }

  // 3. 提交回测（带重试）
  let backtestId;
  for (let attempt = 0; attempt < 30; attempt++) {
    try {
      const btResult = await client.runBacktest(strategyId, code, {
        startTime: START_DATE, endTime: END_DATE,
        baseCapital: '100000', frequency, benchmark: '000300.XSHG',
      }, context);
      backtestId = btResult.backtestId || btResult._id || btResult.id;
      if (typeof backtestId === 'string') backtestId = backtestId.replace(/"/g, '');
      break;
    } catch (e) {
      if (e.message.includes('最大数量') || e.message.includes('403')) {
        process.stdout.write(`  ⏳ 等待槽位... (${attempt + 1}/30)\r`);
        await sleep(POLL_INTERVAL_MS);
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

  // 4. 更新 mapping
  mapping[filename] = {
    ...existing,
    strategyId,
    backtestId: String(backtestId),
    resubmittedAt: new Date().toISOString(),
    lastFrequency: frequency
  };
  saveMapping(mapping);
  console.log(`  ✓ 提交成功: strategy=${strategyId} backtest=${backtestId} (${frequency})`);
  return true;
}

async function main() {
  const zeroFiles = getZeroReturnFiles();
  console.log(`=== 重提交收益为 0 的策略 ===`);
  console.log(`共 ${zeroFiles.length} 个文件需要重提交\n`);

  if (zeroFiles.length === 0) {
    console.log('没有找到收益为 0 的策略。');
    return;
  }

  // 打印列表
  zeroFiles.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));
  console.log();

  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD,
  };
  const cookies = await ensureRiceQuantSession(credentials);
  console.log(`登录成功, cookies: ${cookies.length}\n`);
  const client = new RiceQuantClient({ cookies });
  const mapping = loadMapping();

  let success = 0, fail = 0;
  for (let i = 0; i < zeroFiles.length; i++) {
    const filename = zeroFiles[i];
    console.log(`[${i + 1}/${zeroFiles.length}] ${filename}`);
    const ok = await resubmitFile(client, filename, mapping);
    if (ok) success++; else fail++;
    if (i < zeroFiles.length - 1) await sleep(1000);
  }

  console.log(`\n=== 完成 ===`);
  console.log(`成功: ${success}, 失败: ${fail}`);
  console.log(`\n运行以下命令获取最新结果:`);
  console.log(`  node strategies/quantsplaybook_validation/fetch_new_results.mjs`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
