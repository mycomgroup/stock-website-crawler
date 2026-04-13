#!/usr/bin/env node
/**
 * 根据selected_top100.json批量提交筛选出的策略
 */
import fs from 'node:fs';
import path from 'node:path';
import './load-env.js';
import { DATA_ROOT, REPO_ROOT } from './paths.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { createNewStockStrategy, launchBrowserWithSession } from './utils/browser-session.js';
import { parseArgs, sleep } from './utils/cli.js';

// 配置
const SELECTED_FILE = path.resolve(DATA_ROOT, 'selected_top100.json');
const SOURCE_DIR = path.resolve(REPO_ROOT, 'jk2bt-main', 'strategies');
const DATE_TAG = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const RUN_DIR = path.resolve(DATA_ROOT, `jq558_top100_${DATE_TAG}`);
const JSONL_LOG = path.join(RUN_DIR, 'submissions.jsonl');
const MD_LOG = path.join(RUN_DIR, 'submissions.md');
const STATE_FILE = path.join(RUN_DIR, 'state.json');

function ensureRunFiles() {
  fs.mkdirSync(RUN_DIR, { recursive: true });
  if (!fs.existsSync(JSONL_LOG)) fs.writeFileSync(JSONL_LOG, '', 'utf8');
  if (!fs.existsSync(MD_LOG)) {
    fs.writeFileSync(
      MD_LOG,
      [
        '# JoinQuant Top100策略批量提交记录',
        `> 基于筛选结果: ${SELECTED_FILE}`,
        `> 回测区间: 2025-04-03 至 2026-04-03`,
        '',
        '| # | 排名 | 文件 | 策略名 | 分数 | 状态类型 | AlgorithmID | BacktestID | 提交状态 |',
        '|---|------|------|--------|------|----------|-------------|------------|----------|'
      ].join('\n'),
      'utf8'
    );
  }
}

function loadSelectedStrategies() {
  if (!fs.existsSync(SELECTED_FILE)) {
    throw new Error(`筛选结果文件不存在: ${SELECTED_FILE}\n请先运行: node select_top_strategies.js`);
  }
  const data = JSON.parse(fs.readFileSync(SELECTED_FILE, 'utf8'));
  return data.strategies;
}

function readSubmittedMap() {
  const submitted = new Map();
  if (!fs.existsSync(JSONL_LOG)) return submitted;
  const lines = fs.readFileSync(JSONL_LOG, 'utf8').split('\n').filter(Boolean);
  for (const line of lines) {
    try {
      const item = JSON.parse(line);
      if (item.status === 'submitted') {
        submitted.set(item.basename, item);
      }
    } catch {
      // 忽略
    }
  }
  return submitted;
}

function appendJsonl(record) {
  fs.appendFileSync(JSONL_LOG, `${JSON.stringify(record, null, 0)}\n`, 'utf8');
}

function appendMarkdown(record) {
  const row = [
    record.index,
    record.rank,
    record.basename.replace(/\|/g, '/'),
    record.strategyName.replace(/\|/g, '/'),
    record.score,
    record.statusType,
    record.algorithmId || '',
    record.backtestId || '',
    record.status
  ];
  fs.appendFileSync(MD_LOG, `| ${row.join(' | ')} |\n`, 'utf8');
}

function writeState(extra = {}) {
  const payload = {
    updatedAt: new Date().toISOString(),
    sourceDir: SOURCE_DIR,
    runDir: RUN_DIR,
    selectedFile: SELECTED_FILE,
    ...extra
  };
  fs.writeFileSync(STATE_FILE, JSON.stringify(payload, null, 2), 'utf8');
}

function isRateLimitError(error) {
  const msg = String(error?.message || '');
  return msg.includes('当前并行编译或回测数量最多10个') ||
         msg.includes('50001') ||
         msg.includes('并发') ||
         msg.includes('rate limit');
}

function makeStrategyName(basename, rank) {
  const base = basename
    .replace(/\.(txt|py)$/i, '')
    .replace(/[\\/]/g, '_')
    .replace(/[^\p{L}\p{N}_-]+/gu, '_')
    .replace(/_+/g, '_')
    .replace(/^_+|_+$/g, '');
  const prefix = `TOP${String(rank).padStart(3, '0')}_`;
  return `${prefix}${base}`.slice(0, 80);
}

async function getContextCached(client, algorithmId, contextCache) {
  if (!contextCache.has(algorithmId)) {
    const context = await client.getStrategyContext(algorithmId);
    contextCache.set(algorithmId, context);
  }
  return contextCache.get(algorithmId);
}

async function waitForPlatformCapacity(retrySeconds = 60) {
  console.log(`  平台并发回测已满，${retrySeconds}秒后重试...`);
  await sleep(retrySeconds * 1000);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const startDate = args.start || '2025-04-03';
  const endDate = args.end || '2026-04-03';
  const capital = args.capital || '100000';
  const frequency = args.freq || 'day';
  const sleepMs = Number(args.sleepMs || args.sleep || 5000);
  const headed = Boolean(args.headed);
  const resume = !args.noResume;
  const reuseAlgorithmId = args['reuse-algorithm-id'] || null;

  ensureRunFiles();

  // 加载筛选出的策略列表
  const selectedStrategies = loadSelectedStrategies();
  console.log('='.repeat(80));
  console.log('JoinQuant Top100策略批量提交');
  console.log(`筛选文件: ${SELECTED_FILE}`);
  console.log(`策略总数: ${selectedStrategies.length}`);
  console.log(`回测区间: ${startDate} -> ${endDate}`);
  console.log(`初始资金: ${capital}`);
  console.log(`频率: ${frequency}`);
  console.log(`每次间隔: ${sleepMs}ms`);
  console.log(`日志目录: ${RUN_DIR}`);
  console.log('='.repeat(80));

  const submittedMap = readSubmittedMap();
  const pendingStrategies = resume
    ? selectedStrategies.filter(s => !submittedMap.has(s.basename))
    : selectedStrategies;

  console.log(`已提交: ${submittedMap.size}`);
  console.log(`待提交: ${pendingStrategies.length}`);
  console.log('');

  writeState({
    totalSelected: selectedStrategies.length,
    alreadySubmitted: submittedMap.size,
    pending: pendingStrategies.length,
    startDate,
    endDate,
    capital,
    frequency,
    sleepMs,
    reuseAlgorithmId
  });

  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const { browser, context, page } = await launchBrowserWithSession({ headed });
  const contextCache = new Map();

  let successCount = 0;
  let failCount = 0;

  try {
    for (let i = 0; i < pendingStrategies.length; i += 1) {
      const selected = pendingStrategies[i];
      const filePath = path.join(SOURCE_DIR, '..', selected.file);
      const debugPrefix = `rank_${String(selected.rank).padStart(3, '0')}`;
      
      if (!fs.existsSync(filePath)) {
        console.log(`[${i + 1}/${pendingStrategies.length}] 文件不存在: ${selected.basename}`);
        failCount += 1;
        continue;
      }

      const code = fs.readFileSync(filePath, 'utf8');
      const strategyName = makeStrategyName(selected.basename, selected.rank);

      console.log('');
      console.log(`[${i + 1}/${pendingStrategies.length}] Rank #${selected.rank} (${selected.score}分) ${selected.status}`);
      console.log(`  ${selected.basename}`);

      const record = {
        index: i + 1,
        rank: selected.rank,
        basename: selected.basename,
        file: selected.file,
        strategyName,
        score: selected.score,
        statusType: selected.status,
        startDate,
        endDate,
        capital,
        frequency,
        submittedAt: new Date().toISOString()
      };

      try {
        let created = null;
        if (reuseAlgorithmId) {
          record.algorithmId = reuseAlgorithmId;
          console.log(`  复用策略: ${reuseAlgorithmId}`);
        } else {
          created = await createNewStockStrategy({
            page,
            browserContext: context,
            runDir: RUN_DIR,
            debugPrefix
          });
          record.algorithmId = created.algorithmId;
          console.log(`  新建成功: ${created.algorithmId}`);
        }

        const strategyContext = await getContextCached(client, record.algorithmId, contextCache);
        await client.saveStrategy(record.algorithmId, strategyName, code, strategyContext);
        console.log(`  已保存代码`);

        let buildResult;
        while (true) {
          try {
            buildResult = await client.runBacktest(record.algorithmId, code, {
              startTime: startDate,
              endTime: endDate,
              baseCapital: capital,
              frequency
            }, {
              ...strategyContext,
              name: strategyName
            });
            break;
          } catch (error) {
            if (!isRateLimitError(error)) throw error;
            await waitForPlatformCapacity();
          }
        }

        record.backtestId = buildResult.backtestId;
        record.status = 'submitted';
        record.backtestUrl = `https://www.joinquant.com/algorithm/backtest?backtestId=${buildResult.backtestId}`;
        successCount += 1;
        console.log(`  回测已提交: ${buildResult.backtestId}`);

        if (created && created.targetPage !== page) {
          await created.targetPage.close().catch(() => {});
        }
      } catch (error) {
        record.status = 'failed';
        record.error = error.message;
        failCount += 1;
        console.log(`  提交失败: ${error.message}`);
      }

      appendJsonl(record);
      appendMarkdown(record);
      writeState({
        totalSelected: selectedStrategies.length,
        alreadySubmitted: submittedMap.size + successCount + failCount,
        pending: pendingStrategies.length,
        completedThisRun: successCount + failCount,
        successCount,
        failCount,
        lastRank: selected.rank
      });

      console.log(`  sleep ${sleepMs}ms`);
      await sleep(sleepMs);
    }
  } finally {
    await browser.close().catch(() => {});
  }

  console.log('');
  console.log('='.repeat(80));
  console.log(`完成: 成功 ${successCount} / 失败 ${failCount}`);
  console.log(`日志: ${JSONL_LOG}`);
  console.log(`汇总: ${MD_LOG}`);
  console.log('='.repeat(80));
}

main().catch((error) => {
  console.error('批量提交失败:', error);
  process.exit(1);
});
