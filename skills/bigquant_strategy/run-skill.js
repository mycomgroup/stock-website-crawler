#!/usr/bin/env node
/**
 * BigQuant Strategy Skill - 纯 HTTP 实现
 *
 * 用法:
 *   node run-skill.js --file <strategy.py> [options]
 *   node run-skill.js --id <studioId> --file <strategy.py>
 *
 * 选项:
 *   --file <path>      策略文件路径 (必填)
 *   --id <studioId>    BigQuant Studio ID (可选，默认从 .env 读取)
 *   --start <date>     回测开始日期 (默认: 2023-01-01)
 *   --end <date>       回测结束日期 (默认: 2023-12-31)
 *   --capital <num>    初始资金 (默认: 100000)
 *   --freq <string>    频率 day/minute (默认: day)
 *   --benchmark <id>   基准指数 (默认: 000300.XSHG)
 */

import './load-env.js';
import { runStrategyWorkflow } from './request/strategy-runner.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) { args[key] = value; i++; }
      else args[key] = true;
    }
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

if (args.help || !args.file) {
  console.log(`
用法: node run-skill.js --file <strategy.py> [options]

选项:
  --file <path>      策略文件路径 (必填)
  --id <studioId>    BigQuant Studio ID
  --start <date>     回测开始日期 (默认: 2023-01-01)
  --end <date>       回测结束日期 (默认: 2023-12-31)
  --capital <num>    初始资金 (默认: 100000)
  --freq <string>    day 或 minute (默认: day)
  --benchmark <id>   基准指数 (默认: 000300.XSHG)
`);
  process.exit(args.help ? 0 : 1);
}

runStrategyWorkflow({
  strategyId: args.id,
  codeFilePath: args.file,
  startTime: args.start || '2023-01-01',
  endTime: args.end || '2023-12-31',
  baseCapital: args.capital || '100000',
  frequency: args.freq || 'day',
  benchmark: args.benchmark || '000300.XSHG'
}).then(result => {
  if (result.success) {
    console.log('\n✓ 完成! 结果:', result.outputPath);
  } else {
    console.log('\n⚠ 任务已提交，请查看 Web URL:', result.webUrl);
  }
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});
