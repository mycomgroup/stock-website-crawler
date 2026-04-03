#!/usr/bin/env node
import './load-env.js';
import { runStrategyTest } from './request/strategy-runner.js';

const result = await runStrategyTest({
  strategy: process.argv[2] || 'examples/probe_dai_more.py',
  timeoutMs: 120000
});

const logs = result.logs || [];
const output = logs
  .filter(l => !l.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (?:任务运行|任务运行状态|\[info\s*\]|\[warn\s*\]|\[error\s*\])/))
  .join('\n');

console.log(output || result.textOutput || '(no output)');
