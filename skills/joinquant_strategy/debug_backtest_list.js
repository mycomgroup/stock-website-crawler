#!/usr/bin/env node
// 调试：拿第一个策略的回测列表页 HTML，存到文件看结构
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

await ensureJoinQuantSession({ headed: false, headless: true });
const client = new JoinQuantStrategyClient();

const strategies = await client.listStrategies();
console.log(`策略数: ${strategies.length}`);
console.log('前3个:', strategies.slice(0, 3));

if (strategies.length === 0) process.exit(1);

// 取第一个策略，直接拿原始 HTML
const strat = strategies[0];
console.log(`\n拉取策略 [${strat.id}] ${strat.name} 的回测列表...`);

const url = `/algorithm/backtest/list?algorithmId=${strat.id}`;
const html = await client.request(url, { method: 'GET' });

const outFile = path.join(__dirname, 'data', 'debug_backtest_list.html');
fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, html);
console.log(`HTML 已保存: ${outFile} (${html.length} bytes)`);

// 打印前 3000 字符看结构
console.log('\n--- HTML 前 3000 字符 ---');
console.log(html.slice(0, 3000));
