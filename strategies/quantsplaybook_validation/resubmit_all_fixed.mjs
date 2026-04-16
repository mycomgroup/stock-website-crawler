#!/usr/bin/env node
/**
 * 用修复后的代码重新提交所有策略的回测
 * - 复用已有 strategyId（不重新创建策略）
 * - 并发控制：最多同时 3 个
 * - 结果写入 RESUBMIT_RESULTS.md
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';
import { ensureRiceQuantSession } from '../../skills/ricequant_strategy/browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.join(__dirname, 'strategies');
const MAPPING_FILE   = path.join(__dirname, 'rq_strategy_mapping.json');
const RESULTS_FILE   = path.join(__dirname, 'RESUBMIT_RESULTS.md');
const NEW_MAPPING    = path.join(__dirname, 'rq_strategy_mapping_v2.json');

const START_DATE = '2023-01-01';
const END_DATE   = '2026-04-01';
const MAX_CONCURRENT = Math.max(1, Number(process.env.RQ_MAX_CONCURRENT || 3));
const POLL_MS = 12000;
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
  'rq_86_最新解密追涨龙头打板策略.py',
  'rq_86_预判st并过滤避雷代码740.py',
  'rq_88_打首板策略今年收益达到40绝无未来函数.py',
  'rq_88_WY大神的龙头打板策略小改.py',
  'rq_77 龙头弱转强战法.py',
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

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function inferFrequency(filename, code) {
  if (MINUTE_FREQUENCY_FILES.has(filename)) return '1m';
  if (DAY_FREQUENCY_FILES.has(filename)) return 'day';
  if (/(竞价|开盘|打板|首板|一进二|龙头|日内|T0|T-?0|高频)/.test(filename)) {
    return '1m';
  }
  if (/market_open\(minute=|market_open\(hour=|scheduler\.run_daily\(.+market_open/.test(code)) {
    return '1m';
  }
  return 'day';
}

function loadMapping() {
  return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
}

function saveNewMapping(m) {
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(m, null, 2));
  fs.writeFileSync(NEW_MAPPING, JSON.stringify(m, null, 2));
}

function writeResults(rows) {
  let md = `# 重新提交回测结果\n> ${new Date().toLocaleString()}\n> 区间: ${START_DATE} ~ ${END_DATE}\n\n`;
  md += `| 文件 | StrategyID | BacktestID | 状态 |\n|------|-----------|-----------|------|\n`;
  for (const r of rows) {
    md += `| ${r.filename} | ${r.strategyId} | ${r.backtestId || '-'} | ${r.status} |\n`;
  }
  fs.writeFileSync(RESULTS_FILE, md);
}

async function resubmit(client, filename, strategyId) {
  const filepath = path.join(STRATEGIES_DIR, filename);
  if (!fs.existsSync(filepath)) {
    return { filename, strategyId, backtestId: null, status: '⚠️ 文件不存在' };
  }
  const code = fs.readFileSync(filepath, 'utf8');
  const frequency = inferFrequency(filename, code);

  // 1. 获取上下文
  let context;
  try {
    context = await client.getStrategyContext(strategyId);
  } catch (e) {
    return { filename, strategyId, backtestId: null, status: `❌ 获取上下文失败: ${e.message.slice(0,80)}` };
  }

  // 2. 更新策略代码，确保平台使用本地最新版本
  try {
    await client.saveStrategy(
      strategyId,
      context?.name || filename.replace(/\.py$/, ''),
      code,
      context
    );
  } catch (e) {
    return { filename, strategyId, backtestId: null, status: `❌ 更新代码失败: ${e.message.slice(0,80)}` };
  }

  // 3. 提交回测
  try {
    const bt = await client.runBacktest(strategyId, code, {
      startTime: START_DATE,
      endTime:   END_DATE,
      baseCapital: '100000',
      frequency,
      benchmark: '000300.XSHG'
    }, context);

    let backtestId = bt.backtestId || bt._id || bt.id;
    if (typeof backtestId === 'string') backtestId = backtestId.replace(/"/g, '');
    if (!backtestId) {
      return { filename, strategyId, backtestId: null, status: `❌ 无 backtestId: ${JSON.stringify(bt).slice(0,80)}` };
    }
    return { filename, strategyId, backtestId, status: `🔄 已提交(${frequency})`, frequency };
  } catch (e) {
    return { filename, strategyId, backtestId: null, status: `❌ 提交异常: ${e.message.slice(0,80)}` };
  }
}

async function main() {
  console.log('='.repeat(60));
  console.log('重新提交所有修复后的策略回测');
  console.log(`区间: ${START_DATE} ~ ${END_DATE}  并发: ${MAX_CONCURRENT}`);
  console.log('='.repeat(60));

  // 登录
  const cookies = await ensureRiceQuantSession({
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  });
  console.log(`登录成功, cookies: ${cookies.length}\n`);
  const client = new RiceQuantClient({ cookies });

  // 加载 mapping
  const mapping = loadMapping();
  const newMapping = { ...mapping };

  // 只处理有 strategyId 的条目
  const todo = Object.entries(mapping)
    .filter(([, v]) => v.strategyId)
    .filter(([filename]) => TARGET_FILES.size === 0 || TARGET_FILES.has(filename))
    .map(([filename, v]) => ({ filename, strategyId: v.strategyId }));

  console.log(`待重提交: ${todo.length} 个策略\n`);

  const rows = todo.map(t => ({
    filename: t.filename,
    strategyId: t.strategyId,
    backtestId: null,
    status: '⏳ 待提交'
  }));
  writeResults(rows);

  let done = 0;
  while (done < todo.length) {
    // 检查并发
    let running = 0;
    try { running = await client.getRunningBacktestCount(); } catch {}
    if (running >= MAX_CONCURRENT) {
      process.stdout.write(`  [等待] 运行中: ${running}/${MAX_CONCURRENT}\r`);
      await sleep(POLL_MS);
      continue;
    }

    const slots = MAX_CONCURRENT - running;
    const batch = todo.slice(done, done + slots);
    console.log(`\n[${done+1}~${done+batch.length}/${todo.length}] 提交 ${batch.length} 个...`);

    const results = await Promise.all(batch.map(async ({ filename, strategyId }) => {
      const r = await resubmit(client, filename, strategyId);
      if (r.backtestId) {
        newMapping[filename] = {
          ...mapping[filename],
          backtestId: r.backtestId,
          resubmittedAt: new Date().toISOString(),
          lastFrequency: r.frequency || 'day'
        };
        saveNewMapping(newMapping);
        console.log(`  ✓ ${filename} -> ${r.backtestId} (${r.frequency || 'day'})`);
      } else {
        console.log(`  ✗ ${filename}: ${r.status}`);
      }
      return r;
    }));

    // 更新 rows
    for (const r of results) {
      const idx = rows.findIndex(x => x.filename === r.filename);
      if (idx !== -1) rows[idx] = r;
    }
    writeResults(rows);

    done += batch.length;
    if (done < todo.length) await sleep(3000);
  }

  console.log('\n' + '='.repeat(60));
  console.log(`完成！共 ${todo.length} 个策略`);
  const ok = rows.filter(r => r.backtestId).length;
  const fail = rows.filter(r => !r.backtestId).length;
  console.log(`  成功: ${ok}  失败: ${fail}`);
  console.log(`结果: ${RESULTS_FILE}`);
  console.log(`新 mapping: ${NEW_MAPPING}`);
  console.log('='.repeat(60));
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
