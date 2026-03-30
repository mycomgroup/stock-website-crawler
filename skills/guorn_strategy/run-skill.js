#!/usr/bin/env node
import fs from 'node:fs';
import { runStrategyWorkflow, runRealtimeSelection, runHistoricalSelection } from './request/strategy-runner.js';

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

if (args.help) {
  console.log(`
Usage: node run-skill.js [options]

Commands:
  backtest              Run strategy backtest (default)
  realtime              Run realtime stock selection
  history               Run historical stock selection

Options:
  --config <path>       Path to strategy config JSON file
  --id <strategyId>     Existing strategy ID
  --start <date>        Backtest start date (YYYY-MM-DD), default: 2020-01-01
  --end <date>          Backtest end date (YYYY-MM-DD), default: 2024-01-01
  --benchmark <name>    Benchmark index (hs300, zz500, zz1000), default: hs300
  --cost <rate>         Transaction cost (single side), default: 0.002
  --date <date>         Date for historical selection (YYYY-MM-DD)
  --headed              Run browser in headed mode for session capture
  --force-refresh       Force refresh session

Examples:
  # Run backtest with config file
  node run-skill.js --config strategy.json --start 2020-01-01 --end 2024-01-01

  # Run backtest with existing strategy
  node run-skill.js --id abc123 --start 2020-01-01 --end 2024-01-01

  # Run realtime selection
  node run-skill.js realtime --config strategy.json

  # Run historical selection
  node run-skill.js history --config strategy.json --date 2024-01-01
`);
  process.exit(0);
}

async function main() {
  const command = args._?.[0] || 'backtest';
  
  // Load strategy config from file if provided
  let strategyConfig = null;
  if (args.config) {
    if (!fs.existsSync(args.config)) {
      console.error(`Config file not found: ${args.config}`);
      process.exit(1);
    }
    strategyConfig = JSON.parse(fs.readFileSync(args.config, 'utf8'));
  }

  const backtestConfig = {
    strategyId: args.id,
    startTime: args.start || '2020-01-01',
    endTime: args.end || '2024-01-01',
    benchmark: args.benchmark || 'hs300',
    transactionCost: args.cost || '0.002'
  };

  try {
    let result;
    
    switch (command) {
      case 'backtest':
        result = await runStrategyWorkflow({
          strategyConfig,
          backtestConfig,
          headed: args.headed,
          forceRefresh: args['force-refresh']
        });
        console.log('\nBacktest Result:');
        console.log(JSON.stringify(result.summary, null, 2));
        break;
        
      case 'realtime':
        if (!strategyConfig) {
          console.error('Strategy config required for realtime selection');
          process.exit(1);
        }
        result = await runRealtimeSelection({
          strategyConfig,
          headed: args.headed,
          forceRefresh: args['force-refresh']
        });
        console.log('\nRealtime Selection:');
        console.log(`Found ${result.stocks.length} stocks`);
        break;
        
      case 'history':
        if (!strategyConfig) {
          console.error('Strategy config required for historical selection');
          process.exit(1);
        }
        if (!args.date) {
          console.error('Date required for historical selection');
          process.exit(1);
        }
        result = await runHistoricalSelection({
          strategyConfig,
          date: args.date,
          headed: args.headed,
          forceRefresh: args['force-refresh']
        });
        console.log('\nHistorical Selection:');
        console.log(`Date: ${result.date}`);
        console.log(`Found ${result.stocks.length} stocks`);
        break;
        
      default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
