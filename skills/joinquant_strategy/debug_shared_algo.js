#!/usr/bin/env node
// 调试：检查 JQ558 共享 algorithmId 下的回测列表 HTML 结构
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

await ensureJoinQuantSession({ headed: false, headless: true });
const client = new JoinQuantStrategyClient();

// JQ558 批量提交用的共享 algorithmId（从 submissions.jsonl 里看到的）
const sharedAlgoId = 'cd45eba022e60387deb91ee6f725ef50';

console.log(`拉取共享 algorithmId [${sharedAlgoId}] 的回测列表...`);
const url = `/algorithm/backtest/list?algorithmId=${sharedAlgoId}`;
const html = await client.request(url, { method: 'GET' });

const outFile = path.join(__dirname, 'data', 'debug_shared_algo.html');
fs.writeFileSync(outFile, html);
console.log(`HTML 已保存: ${outFile} (${html.length} bytes)`);

// 找关键结构
const backtestCount = html.match(/共有(\d+)个回测/);
console.log('回测数量:', backtestCount?.[1] ?? '未找到');

// 找所有包含 backtestId 的行
const lines = html.split('\n').filter(l => l.includes('backtestId') || l.includes('backtest-id') || l.includes('data-id'));
console.log('\n含 backtestId 的行 (前20):');
lines.slice(0, 20).forEach(l => console.log(l.trim()));

// 找 tr 行
const trLines = html.split('\n').filter(l => l.includes('<tr') && l.includes('data-'));
console.log('\n含 data- 属性的 <tr> 行 (前10):');
trLines.slice(0, 10).forEach(l => console.log(l.trim()));
