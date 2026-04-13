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
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { createNewStockStrategy, launchBrowserWithSession } from './utils/browser-session.js';
import { parseArgs } from './utils/cli.js';

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
  const { browser, context, page } = await launchBrowserWithSession({
    browserArgs: ['--disable-blink-features=AutomationControlled'],
    contextOptions: {
      userAgent:
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      viewport: { width: 1280, height: 720 }
    }
  });

  try {
    console.error('[3/3] Creating new strategy...');
    const created = await createNewStockStrategy({
      page,
      browserContext: context
    });
    const algorithmId = created.algorithmId;
    console.error(`  ✓ Created strategy: algorithmId=${algorithmId}`);

    if (code) {
      try {
        const client = new JoinQuantStrategyClient();
        const jqContext = await client.getStrategyContext(algorithmId);
        await client.saveStrategy(algorithmId, strategyName, code, jqContext);
        console.error(`  ✓ Code uploaded: ${strategyName}`);
      } catch (e) {
        console.error(`  ⚠ Code upload failed: ${e.message}`);
      }
    }

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
