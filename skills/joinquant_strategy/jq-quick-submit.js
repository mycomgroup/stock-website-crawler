#!/usr/bin/env node
/**
 * jq-quick-submit.js - 快速提交策略，不等待回测完成
 * 
 * 只负责：
 * 1. 确保 session 有效
 * 2. 上传策略代码
 * 3. 启动回测
 * 4. 返回 backtestId
 * 
 * 不等待回测完成！
 */

import './load-env.js';
import fs from 'fs';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { parseArgs } from './utils/cli.js';

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { id, file, start, end, capital, freq } = args;

  if (!id || !file) {
    console.error('Usage: node jq-quick-submit.js --id <algorithmId> --file <path> [options]');
    process.exit(1);
  }

  if (!fs.existsSync(file)) {
    console.error('Error: File not found:', file);
    process.exit(1);
  }

  const code = fs.readFileSync(file, 'utf8');

  try {
    // 1. 确保 session 有效
    console.error('[1/4] Verifying session...');
    await ensureJoinQuantSession({ headed: false, headless: true });
    const client = new JoinQuantStrategyClient();
    
    // 2. 获取策略上下文
    console.error('[2/4] Getting strategy context...');
    const context = await client.getStrategyContext(id);
    console.error(`   Strategy: ${context.name}`);
    
    // 3. 保存策略代码
    console.error('[3/4] Uploading strategy code...');
    await client.saveStrategy(id, context.name, code, context);
    console.error('   Code uploaded');
    
    // 4. 启动回测
    console.error('[4/4] Starting backtest...');
    const buildResult = await client.runBacktest(id, code, {
      startTime: start || '2023-01-01',
      endTime: end || '2023-12-31',
      baseCapital: capital || '100000',
      frequency: freq || 'day'
    }, context);
    
    const backtestId = buildResult.backtestId;
    if (backtestId) {
      console.error(`   ✓ Backtest started! ID: ${backtestId}`);
      // 输出 JSON 到 stdout，供 Python 解析
      console.log(JSON.stringify({
        backtest_id: backtestId,
        backtestId: backtestId,
        status: "submitted"
      }, null, 2));
    } else {
      console.error('   ✗ Failed to start backtest');
      console.log(JSON.stringify({
        status: "error",
        message: "Failed to start backtest"
      }, null, 2));
      process.exit(1);
    }
  } catch (e) {
    console.error('Error:', e.message);
    console.log(JSON.stringify({
      status: "error",
      message: e.message
    }, null, 2));
    process.exit(1);
  }
}

main();
