#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { JoinQuantStrategyClient, loadJson } from './request/joinquant-strategy-client.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const SOURCE_DIR = path.resolve(REPO_ROOT, '聚宽有价值策略558');
const DATE_TAG = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const RUN_DIR = path.resolve(__dirname, 'data', `jq558_batch_${DATE_TAG}`);
const JSONL_LOG = path.join(RUN_DIR, 'submissions.jsonl');
const MD_LOG = path.join(RUN_DIR, 'submissions.md');
const STATE_FILE = path.join(RUN_DIR, 'state.json');
const LIST_URL = 'https://www.joinquant.com/algorithm/index/list';
const NEW_STOCK_STRATEGY_URL = 'https://www.joinquant.com/algorithm/index/new?restore=0&type=stock&baseCapital=100000';

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

function ensureRunFiles() {
  fs.mkdirSync(RUN_DIR, { recursive: true });
  if (!fs.existsSync(JSONL_LOG)) fs.writeFileSync(JSONL_LOG, '', 'utf8');
  if (!fs.existsSync(MD_LOG)) {
    fs.writeFileSync(
      MD_LOG,
      [
        '# JoinQuant 批量提交记录',
        `> 目录: ${SOURCE_DIR}`,
        `> 最近1年回测区间: 2025-04-03 至 2026-04-03`,
        '',
        '| # | 文件 | 策略名 | AlgorithmID | BacktestID | 状态 |',
        '|---|------|--------|-------------|------------|------|'
      ].join('\n'),
      'utf8'
    );
  }
}

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
  return files.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN'));
}

function readSubmittedMap() {
  const submitted = new Map();
  if (!fs.existsSync(JSONL_LOG)) return submitted;
  const lines = fs.readFileSync(JSONL_LOG, 'utf8').split('\n').filter(Boolean);
  for (const line of lines) {
    try {
      const item = JSON.parse(line);
      submitted.set(item.file, item);
    } catch {
      // Ignore malformed lines and continue.
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
    record.relativePath.replace(/\|/g, '/'),
    record.strategyName.replace(/\|/g, '/'),
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
    ...extra
  };
  fs.writeFileSync(STATE_FILE, JSON.stringify(payload, null, 2), 'utf8');
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function makeStrategyName(relativePath, index) {
  const base = relativePath
    .replace(/\.(txt|py)$/i, '')
    .replace(/[\\/]/g, '_')
    .replace(/[^\p{L}\p{N}_-]+/gu, '_')
    .replace(/_+/g, '_')
    .replace(/^_+|_+$/g, '');
  const prefix = `JQ558_${String(index).padStart(4, '0')}_`;
  return `${prefix}${base}`.slice(0, 80);
}

async function launchBrowserWithSession(headed = false) {
  const sessionPayload = loadJson(SESSION_FILE);
  if (!sessionPayload.cookies || sessionPayload.cookies.length === 0) {
    throw new Error(`No cookies found in session file: ${SESSION_FILE}`);
  }
  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext();
  await context.addCookies(sessionPayload.cookies);
  const page = await context.newPage();
  return { browser, context, page };
}

async function clickFirstVisible(page, selectors) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    try {
      if (await locator.count()) {
        await locator.click({ timeout: 5000 });
        return selector;
      }
    } catch {
      // Try next selector.
    }
  }
  return null;
}

async function createNewStrategy(page, browserContext, debugPrefix) {
  // Direct entry discovered from the live JoinQuant strategy list page:
  // /algorithm/index/new?restore=0&type=stock&baseCapital=100000
  await page.goto(NEW_STOCK_STRATEGY_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});

  if (page.url().includes('/login/')) {
    throw new Error('JoinQuant session is not logged in when opening new stock strategy page');
  }

  let targetPage = page;
  let clickedSelector = 'direct:new_stock_strategy_url';
  let match = targetPage.url().match(/algorithmId=([^&]+)/);

  if (!match) {
    // Fallback: open strategy list, click "新建策略" dropdown, then click "股票策略".
    await page.goto(LIST_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});

    const popupPromise = browserContext.waitForEvent('page', { timeout: 3000 }).catch(() => null);
    const openDropdown = await clickFirstVisible(page, [
      '#new-algo-button',
      'button:has-text("新建策略")',
      'a:has-text("新建策略")',
      'text=新建策略'
    ]);

    if (!openDropdown) {
      const htmlFile = path.join(RUN_DIR, `${debugPrefix}_list_page.html`);
      const pngFile = path.join(RUN_DIR, `${debugPrefix}_list_page.png`);
      fs.writeFileSync(htmlFile, await page.content(), 'utf8');
      await page.screenshot({ path: pngFile, fullPage: true }).catch(() => {});
      throw new Error(`Unable to find "新建策略" dropdown on list page. Debug saved to ${htmlFile}`);
    }

    const stockLink = page.locator('#tacticsList a[href*="/algorithm/index/new?"][href*="type=stock"]').first();
    await stockLink.waitFor({ state: 'visible', timeout: 10000 });
    await stockLink.click({ timeout: 10000 });

    const popup = await popupPromise;
    targetPage = popup || page;
    clickedSelector = 'fallback:#tacticsList stock link';
    await targetPage.waitForLoadState('domcontentloaded', { timeout: 30000 });
    await targetPage.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    match = targetPage.url().match(/algorithmId=([^&]+)/);
  }

  if (!match) {
    const htmlFile = path.join(RUN_DIR, `${debugPrefix}_edit_page.html`);
    fs.writeFileSync(htmlFile, await targetPage.content(), 'utf8');
    const pngFile = path.join(RUN_DIR, `${debugPrefix}_edit_page.png`);
    await targetPage.screenshot({ path: pngFile, fullPage: true }).catch(() => {});
    throw new Error(`Failed to parse algorithmId from URL: ${targetPage.url()}`);
  }

  return {
    algorithmId: match[1],
    targetPage,
    clickedSelector
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const startDate = args.start || '2025-04-03';
  const endDate = args.end || '2026-04-03';
  const capital = args.capital || '100000';
  const frequency = args.freq || 'day';
  const sleepMs = Number(args.sleepMs || args.sleep || 5000);
  const limit = args.limit ? Number(args.limit) : null;
  const headed = Boolean(args.headed);
  const resume = !args.noResume;

  ensureRunFiles();

  const allFiles = walkStrategyFiles(SOURCE_DIR);
  const submittedMap = readSubmittedMap();
  const pendingFiles = resume
    ? allFiles.filter((file) => !submittedMap.has(file))
    : allFiles;
  const finalFiles = limit ? pendingFiles.slice(0, limit) : pendingFiles;

  writeState({
    totalFiles: allFiles.length,
    alreadySubmitted: submittedMap.size,
    pending: pendingFiles.length,
    selectedThisRun: finalFiles.length,
    startDate,
    endDate,
    capital,
    frequency,
    sleepMs
  });

  console.log('='.repeat(80));
  console.log('JoinQuant 批量新建策略并异步提交回测');
  console.log(`源目录: ${SOURCE_DIR}`);
  console.log(`总文件数: ${allFiles.length}`);
  console.log(`已提交(日志存在): ${submittedMap.size}`);
  console.log(`本次待提交: ${finalFiles.length}`);
  console.log(`回测区间: ${startDate} -> ${endDate}`);
  console.log(`初始资金: ${capital}`);
  console.log(`频率: ${frequency}`);
  console.log(`每次间隔: ${sleepMs}ms`);
  console.log(`日志目录: ${RUN_DIR}`);
  console.log('='.repeat(80));

  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const { browser, context, page } = await launchBrowserWithSession(headed);

  let successCount = 0;
  let failCount = 0;

  try {
    for (let i = 0; i < finalFiles.length; i += 1) {
      const file = finalFiles[i];
      const absoluteIndex = allFiles.indexOf(file) + 1;
      const relativePath = path.relative(REPO_ROOT, file);
      const strategyName = makeStrategyName(relativePath, absoluteIndex);
      const debugPrefix = `item_${String(absoluteIndex).padStart(4, '0')}`;
      const code = fs.readFileSync(file, 'utf8');

      console.log('');
      console.log(`[${i + 1}/${finalFiles.length}] ${relativePath}`);

      const record = {
        index: absoluteIndex,
        file,
        relativePath,
        strategyName,
        startDate,
        endDate,
        capital,
        frequency,
        submittedAt: new Date().toISOString()
      };

      try {
        const created = await createNewStrategy(page, context, debugPrefix);
        record.algorithmId = created.algorithmId;
        record.createSelector = created.clickedSelector;
        console.log(`  新建成功: algorithmId=${created.algorithmId}`);

        const strategyContext = await client.getStrategyContext(created.algorithmId);
        await client.saveStrategy(created.algorithmId, strategyName, code, strategyContext);
        console.log(`  已保存代码: ${strategyName}`);

        const buildResult = await client.runBacktest(created.algorithmId, code, {
          startTime: startDate,
          endTime: endDate,
          baseCapital: capital,
          frequency
        }, {
          ...strategyContext,
          name: strategyName
        });

        record.backtestId = buildResult.backtestId;
        record.status = 'submitted';
        record.backtestUrl = `https://www.joinquant.com/algorithm/backtest?backtestId=${buildResult.backtestId}`;
        successCount += 1;
        console.log(`  回测已提交: backtestId=${buildResult.backtestId}`);

        if (created.targetPage !== page) {
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
        totalFiles: allFiles.length,
        alreadySubmitted: submittedMap.size + successCount + failCount,
        selectedThisRun: finalFiles.length,
        completedThisRun: successCount + failCount,
        successCount,
        failCount,
        lastFile: relativePath
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
