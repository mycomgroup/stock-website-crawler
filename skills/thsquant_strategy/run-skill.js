#!/usr/bin/env node
import './load-env.js';
import { runStrategyWorkflow } from './request/strategy-runner.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else args[key] = true;
    }
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

if (args.help || !args.id || !args.file) {
  console.log(`
Usage: node run-skill.js --id <algoId> --file <codePath> [options]

Options:
  --id <id>          THSQuant Algorithm ID
  --file <path>      Path to local .py strategy file
  --start <date>     Backtest start date (YYYY-MM-DD), default: 2023-01-01
  --end <date>       Backtest end date (YYYY-MM-DD), default: 2024-12-31
  --capital <num>    Initial capital, default: 100000
  --freq <freq>      DAILY | 1d | 1h | 1m, default: DAILY
  --benchmark <id>   Benchmark index, default: 000300.SH
  --headed           Run browser in headed mode for session capture
`);
  process.exit(0);
}

runStrategyWorkflow({
  algoId: args.id,
  codeFilePath: args.file,
  beginDate: args.start || '2023-01-01',
  endDate: args.end || '2024-12-31',
  capitalBase: args.capital || '100000',
  frequency: args.freq || 'DAILY',
  benchmark: args.benchmark || '000300.SH',
  headed: !!args.headed
}).then(result => {
  console.log('\n=== Backtest Summary ===');
  const s = result.summary;
  console.log(`Backtest ID:    ${s.backtestId}`);
  console.log(`Period:         ${s.period}`);
  console.log(`Total Return:   ${s.yield != null ? (s.yield * 100).toFixed(2) + '%' : 'N/A'}`);
  console.log(`Annual Return:  ${s.annualYield != null ? (s.annualYield * 100).toFixed(2) + '%' : 'N/A'}`);
  console.log(`Max Drawdown:   ${s.maxDrawdown != null ? (s.maxDrawdown * 100).toFixed(2) + '%' : 'N/A'}`);
  console.log(`Sharpe:         ${s.sharpe ?? 'N/A'}`);
  console.log(`Win Rate:       ${s.winRate != null ? (s.winRate * 100).toFixed(1) + '%' : 'N/A'}`);
  console.log(`Benchmark:      ${s.benchmarkYield != null ? (s.benchmarkYield * 100).toFixed(2) + '%' : 'N/A'}`);
  console.log(`Report:         ${result.resultPath}`);
}).catch(err => {
  console.error('\nWorkflow failed:', err.message);
  process.exit(1);
});
