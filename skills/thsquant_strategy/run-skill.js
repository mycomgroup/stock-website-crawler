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

if (args.help || !args.file) {
  console.log(`
Usage: node run-skill.js --file <codePath> [options]

Options:
  --file <path>      Path to local .py strategy file (required)
  --name <name>      Business name for the strategy, e.g. "rfscore7_pb10_v1"
                     Default: filename without extension
  --id <algoId>      Reuse existing strategy ID instead of creating new one
  --start <date>     Backtest start date (YYYY-MM-DD), default: 2023-01-01
  --end <date>       Backtest end date (YYYY-MM-DD), default: 2024-12-31
  --capital <num>    Initial capital, default: 100000
  --freq <freq>      DAILY | 1d | 1h | 1m, default: DAILY
  --benchmark <id>   Benchmark index, default: 000300.SH
  --headed           Run browser in headed mode for session capture

Examples:
  # Create new strategy each run (default, preserves history)
  node run-skill.js --file strategies/rfscore7_pb10.py --name rfscore7_pb10_v1

  # Reuse existing strategy ID
  node run-skill.js --file strategies/rfscore7_pb10.py --id 67c935e607887b957629ad72
`);
  process.exit(0);
}

runStrategyWorkflow({
  algoId: args.id,
  strategyName: args.name,
  codeFilePath: args.file,
  beginDate: args.start || '2023-01-01',
  endDate: args.end || '2024-12-31',
  capitalBase: args.capital || '100000',
  frequency: args.freq || 'DAILY',
  benchmark: args.benchmark || '000300.SH',
  createNew: !args.id,
  headed: !!args.headed
}).then(result => {
  const s = result.summary;
  const pct = v => v != null ? (v * 100).toFixed(2) + '%' : 'N/A';
  const num = v => v != null ? Number(v).toFixed(4) : 'N/A';

  console.log('\n' + '='.repeat(55));
  console.log('Backtest Summary');
  console.log('='.repeat(55));
  console.log(`Strategy:       ${s.strategyName}`);
  console.log(`Backtest ID:    ${s.backtestId}`);
  console.log(`Period:         ${s.period}`);
  console.log(`Capital:        ${s.capitalBase.toLocaleString()}`);
  console.log(`Frequency:      ${s.frequency}`);
  console.log(`Benchmark:      ${s.benchmark}`);
  console.log('─'.repeat(55));
  console.log(`Total Return:   ${pct(s.totalReturn)}   (Benchmark: ${pct(s.benchmarkReturn)})`);
  console.log(`Annual Return:  ${pct(s.annualReturn)}   (Excess: ${pct(s.excessReturn)})`);
  console.log(`Max Drawdown:   ${pct(s.maxDrawdown)}   (on ${s.drawdownDate || 'N/A'})`);
  console.log(`Volatility:     ${pct(s.volatility)}`);
  console.log('─'.repeat(55));
  console.log(`Sharpe:         ${num(s.sharpe)}`);
  console.log(`Sortino:        ${num(s.sortino)}`);
  console.log(`Alpha:          ${num(s.alpha)}`);
  console.log(`Beta:           ${num(s.beta)}`);
  console.log(`Info Ratio:     ${num(s.informationRatio)}`);
  console.log('─'.repeat(55));
  console.log(`Win Rate:       ${pct(s.winRate)}`);
  console.log(`Trade Win Rate: ${pct(s.tradeWinRate)}`);
  console.log(`Trade Count:    ${s.tradeCount}`);
  console.log('─'.repeat(55));
  console.log(`Report:         ${result.resultPath}`);
  console.log('='.repeat(55));
}).catch(err => {
  console.error('\nWorkflow failed:', err.message);
  process.exit(1);
});
