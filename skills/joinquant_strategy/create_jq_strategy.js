#!/usr/bin/env node
/**
 * create_jq_strategy.js
 *
 * 自动在 JoinQuant 创建新策略，返回 algorithmId。
 * 
 * 使用浏览器自动化：
 *   1. 打开新建策略页面
 *   2. 从 URL 提取 algorithmId
 *   3. 可选：上传初始代码
 *
 * Usage:
 *   node create_jq_strategy.js --name <strategy_name> [--file <strategy.py>]
 *
 * 输出（stdout JSON）：
 *   { "strategy_id": "...", "algorithmId": "...", "strategy_name": "...", "action": "created" }
 */

import './load-env.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { SESSION_FILE } from './paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const NEW_STOCK_STRATEGY_URL = 'https://www.joinquant.com/algorithm/index/new?restore=0&type=stock&baseCapital=100000';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const val = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      args[key] = val;
    }
  }
  return args;
}

async function launchBrowserWithSession(headed = false) {
  const sessionPayload = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = sessionPayload.cookies || [];
  
  const browser = await chromium.launch({ 
    headless: !headed,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 720 }
  });
  
  await context.addCookies(cookies);
  const page = await context.newPage();
  
  return { browser, context, page };
}

async function createNewStrategy(page, strategyName, code = null) {
  // 1. 打开新建策略页面
  await page.goto(NEW_STOCK_STRATEGY_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
  
  // 检查是否登录
  if (page.url().includes('/login/')) {
    throw new Error('JoinQuant session expired or not logged in');
  }
  
  // 2. 从 URL 提取 algorithmId
  const url = page.url();
  const match = url.match(/algorithmId=([^&]+)/);
  
  if (!match) {
    throw new Error(`Failed to parse algorithmId from URL: ${url}`);
  }
  
  const algorithmId = match[1];
  console.error(`  ✓ Created strategy: algorithmId=${algorithmId}`);
  
  // 3. 如果提供了代码，保存到策略
  if (code) {
    try {
      const client = new JoinQuantStrategyClient();
      const context = await client.getStrategyContext(algorithmId);
      await client.saveStrategy(algorithmId, strategyName, code, context);
      console.error(`  ✓ Code uploaded: ${strategyName}`);
    } catch (e) {
      console.error(`  ⚠ Code upload failed: ${e.message}`);
    }
  }
  
  return algorithmId;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const strategyName = args.name;
  const strategyFile = args.file;

  if (!strategyName) {
    console.error('Usage: node create_jq_strategy.js --name <strategy_name> [--file <strategy.py>]');
    process.exit(1);
  }

  if (strategyFile && !fs.existsSync(strategyFile)) {
    console.error(`Strategy file not found: ${strategyFile}`);
    process.exit(1);
  }

  const code = strategyFile ? fs.readFileSync(strategyFile, 'utf8') : null;

  console.error('[1/3] Ensuring JoinQuant session...');
  await ensureJoinQuantSession({ headed: false, headless: true });

  console.error('[2/3] Launching browser...');
  const { browser, page } = await launchBrowserWithSession(false);

  try {
    console.error('[3/3] Creating new strategy...');
    const algorithmId = await createNewStrategy(page, strategyName, code);

    // 输出 JSON 到 stdout
    const output = {
      strategy_id: algorithmId,
      algorithmId: algorithmId,
      strategy_name: strategyName,
      action: "created"
    };
    console.log(JSON.stringify(output, null, 2));

  } finally {
    await browser.close();
  }
}

main().catch(e => {
  console.error('Error:', e.message);
  console.log(JSON.stringify({
    status: "error",
    message: e.message
  }, null, 2));
  process.exit(1);
});