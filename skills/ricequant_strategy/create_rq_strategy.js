#!/usr/bin/env node
/**
 * create_rq_strategy.js
 *
 * Step 1 固化脚本：登录 RiceQuant，创建专用策略，输出 strategy_id。
 *
 * 逻辑：
 *   1. 确保 RiceQuant session 有效（自动登录）
 *   2. 列出现有策略，找名字以 strategyName 开头的
 *   3. 找到则复用，没找到则用 seed 文件内容创建新策略
 *   4. 打印 strategy_id，可直接写入 seed_config.json
 *
 * Usage:
 *   node create_rq_strategy.js \
 *     --name autoresearch_rfscore7_pb10 \
 *     --file /path/to/strategy.py
 *
 * 输出（stdout JSON）：
 *   { "strategy_id": "2418671", "strategy_name": "autoresearch_rfscore7_pb10", "action": "created|reused" }
 */

import './load-env.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const strategyName = args.name;
  const strategyFile = args.file;

  if (!strategyName || !strategyFile) {
    console.error('Usage: node create_rq_strategy.js --name <strategy_name> --file <strategy.py>');
    process.exit(1);
  }

  if (!fs.existsSync(strategyFile)) {
    console.error(`Strategy file not found: ${strategyFile}`);
    process.exit(1);
  }

  const code = fs.readFileSync(strategyFile, 'utf8');

  // 1. 确保 session 有效
  console.error('[1/3] 确保 RiceQuant session...');
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD,
  };
  const cookies = await ensureRiceQuantSession(credentials);
  const client = new RiceQuantClient({ cookies });

  // 2. 查找已有同名策略
  console.error('[2/3] 查找已有策略...');
  let strategyId = null;
  let action = 'created';

  try {
    const strategies = await client.listStrategies();
    const existing = strategies.find(s => s.name === strategyName);
    if (existing) {
      strategyId = String(existing.id || existing.strategy_id);
      action = 'reused';
      console.error(`  找到已有策略: ${strategyName} (id=${strategyId})`);
    }
  } catch (e) {
    console.error(`  listStrategies 失败: ${e.message}，继续创建新策略`);
  }

  // 3. 没找到则创建
  if (!strategyId) {
    console.error(`[3/3] 创建新策略: ${strategyName}...`);
    const result = await client.createStrategy(strategyName, code);
    strategyId = String(result.strategy_id || result._id || result.id || '');
    if (!strategyId) {
      console.error('创建失败，返回结果:', JSON.stringify(result));
      process.exit(1);
    }
    console.error(`  创建成功: id=${strategyId}`);
  } else {
    console.error('[3/3] 复用已有策略，跳过创建');
  }

  // 输出结果到 stdout（供外部脚本解析）
  const output = { strategy_id: strategyId, strategy_name: strategyName, action };
  console.log(JSON.stringify(output, null, 2));
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
