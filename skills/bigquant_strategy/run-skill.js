#!/usr/bin/env node
/**
 * BigQuant Strategy Skill
 * 对齐 joinquant_notebook/run-skill.js 接口
 *
 * 用法:
 *   node run-skill.js --strategy <file.py> [options]
 *   node run-skill.js --cell-source "print('hello')" [options]
 *
 * 选项:
 *   --strategy <path>     策略文件路径 (.py)
 *   --cell-source <code>  内联代码字符串
 *   --start-date <date>   回测开始日期 (默认: 2023-01-01)
 *   --end-date <date>     回测结束日期 (默认: 2023-12-31)
 *   --capital <num>       初始资金 (默认: 100000)
 *   --benchmark <id>      基准指数 (默认: 000300.XSHG)
 *   --frequency <str>     day/minute (默认: day)
 *   --timeout-ms <ms>     超时毫秒 (默认: 300000)
 *   --studio-id <id>      BigQuant Studio ID
 *   --resource-spec-id    资源规格 ID (自动检测可用资源)
 */

import './load-env.js';
import { runStrategyTest } from './request/strategy-runner.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) { args[key] = true; continue; }
    args[key] = next;
    i++;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

if (args.help || (!args.strategy && !args['cell-source'])) {
  console.log(`
用法: node run-skill.js --strategy <file.py> [options]
      node run-skill.js --cell-source "print('hello')" [options]

选项:
  --strategy <path>       策略文件路径
  --cell-source <code>    内联代码
  --start-date <date>     回测开始 (默认: 2023-01-01)
  --end-date <date>       回测结束 (默认: 2023-12-31)
  --capital <num>         初始资金 (默认: 100000)
  --benchmark <id>        基准指数 (默认: 000300.XSHG)
  --frequency <str>       day/minute (默认: day)
  --timeout-ms <ms>       超时毫秒 (默认: 300000)
  --studio-id <id>        Studio ID
  --resource-spec-id <id> 资源规格 ID (自动检测)
`);
  process.exit(args.help ? 0 : 1);
}

const result = await runStrategyTest({
  strategy: args.strategy,
  cellSource: args['cell-source'],
  startDate: args['start-date'] || '2023-01-01',
  endDate: args['end-date'] || '2023-12-31',
  capital: Number(args.capital) || 100000,
  benchmark: args.benchmark || '000300.XSHG',
  frequency: args.frequency || 'day',
  timeoutMs: Number(args['timeout-ms']) || 300000,
  studioId: args['studio-id'],
  resourceSpecId: args['resource-spec-id']
});

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
