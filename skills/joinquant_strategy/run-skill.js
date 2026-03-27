#!/usr/bin/env node
import { runStrategyWorkflow } from './request/strategy-runner.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

if (args.help || !args.id || !args.file) {
  console.log(`
Usage: node run-skill.js --id <algorithmId> --file <codePath> [options]

Options:
  --id <id>          The JoinQuant Algorithm ID (from the URL)
  --file <path>      Path to the local .txt or .py strategy file
  --start <date>     Backtest start date (YYYY-MM-DD), default: 2023-01-01
  --end <date>       Backtest end date (YYYY-MM-DD), default: 2023-12-31
  --capital <num>    Initial capital, default: 100000
  --freq <frequency> day or minute, default: day
  --headed           Run browser in headed mode for session capture
`);
  process.exit(0);
}

runStrategyWorkflow({
  algorithmId: args.id,
  codeFilePath: args.file,
  startTime: args.start || '2023-01-01',
  endTime: args.end || '2023-12-31',
  baseCapital: args.capital || '100000',
  frequency: args.freq || 'day',
  headed: args.headed
}).then(result => {
  console.log('Success!', result.summary);
}).catch(err => {
  console.error('Workflow failed:', err.message);
  process.exit(1);
});
