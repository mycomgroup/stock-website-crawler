#!/usr/bin/env node
import fs from 'node:fs';
import { runStrategyWorkflow, runRealtimeSelection, runHistoricalSelection } from './request/strategy-runner.js';
import { GuornStrategyClient, FACTOR_IDS } from './request/guorn-strategy-client.js';

function parseArgs(argv) {
  const args = { _: [] };
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
    } else {
      args._.push(arg);
    }
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

if (args.help) {
  console.log(`
Usage: node run-skill.js [command] [options]

Commands:
  backtest              Run strategy backtest (default)
  realtime              Run realtime stock selection
  history               Run historical stock selection
  factors               List available factor IDs from /stock/meta

Options:
  --config <path>       Path to strategy config JSON file
  --start <date>        Backtest start date (YYYY-MM-DD)
  --end <date>          Backtest end date (YYYY-MM-DD)
  --benchmark <name>    Benchmark: hs300 (default), zz500, zz1000
  --cost <rate>         Transaction cost (single side), default: 0.002
  --count <n>           Max stock count, default: 10
  --period <n>          Rebalance period (trading days), default: 20
  --rank <factorId>     Rank factor ID (from 'factors' command)
  --date <date>         Date for historical selection (YYYY-MM-DD)
  --headed              Run browser in headed mode
  --force-refresh       Force refresh session

Notes:
  - Level-1 accounts: backtest window limited to ~1 year
  - Factor IDs format: "0.M.股票每日指标_<name>.0"
  - Known factors: ROA="${FACTOR_IDS.ROA}"

Examples:
  # List available factors
  node run-skill.js factors

  # Run backtest (last year, ROA factor)
  node run-skill.js --start 2025-04-01 --end 2026-04-01 --rank "${FACTOR_IDS.ROA}"

  # Run backtest with config file
  node run-skill.js --config strategy.json --start 2025-04-01 --end 2026-04-01

  # Run realtime selection
  node run-skill.js realtime --config strategy.json

  # Run historical selection
  node run-skill.js history --config strategy.json --date 2025-01-01
`);
  process.exit(0);
}

async function main() {
  const command = args._[0] || 'backtest';

  // Load strategy config from file if provided
  let strategyConfig = null;
  if (args.config) {
    if (!fs.existsSync(args.config)) {
      console.error(`Config file not found: ${args.config}`);
      process.exit(1);
    }
    strategyConfig = JSON.parse(fs.readFileSync(args.config, 'utf8'));
  }

  try {
    let result;

    switch (command) {
      case 'factors': {
        const client = new GuornStrategyClient();
        const meta = await client.getStockMeta();
        // Flatten all measures
        const measures = [];
        function collectMeasures(node) {
          if (!node) return;
          if (node.id && node.name) measures.push({ id: node.id, name: node.name });
          if (node.values) node.values.forEach(collectMeasures);
        }
        if (meta.data?.measures) meta.data.measures.forEach(collectMeasures);
        console.log(`\nAvailable factors (${measures.length} total):\n`);
        measures.forEach(m => console.log(`  ${m.id.padEnd(50)} ${m.name}`));
        break;
      }

      case 'backtest': {
        // Build strategy config from CLI args or file
        const cfg = strategyConfig || {};

        // Add rank factor from --rank arg
        if (args.rank) {
          cfg.ranks = [{ id: args.rank, weight: 1.0, asc: false, industry: 0 }];
        }
        if (args.count) cfg.count = String(args.count);
        if (args.period) cfg.period = Number(args.period);

        const backtestConfig = {
          startTime: args.start,
          endTime: args.end,
          benchmark: args.benchmark || 'hs300',
          transactionCost: args.cost ? Number(args.cost) : 0.002
        };

        result = await runStrategyWorkflow({
          strategyConfig: cfg,
          backtestConfig,
          headed: args.headed,
          forceRefresh: args['force-refresh']
        });

        console.log('\nBacktest Result:');
        console.log(`  Annual Return:    ${result.summary.annualReturn}`);
        console.log(`  Win Rate:         ${result.summary.winRate}`);
        console.log(`  Info Ratio:       ${result.summary.informationRatio?.toFixed(3)}`);
        console.log(`  Avg Holding Days: ${result.summary.avgHoldingDays}`);
        console.log(`  Sell Count:       ${result.summary.sellCount}`);
        console.log(`\nFull result: ${result.resultPath}`);
        break;
      }

      case 'realtime': {
        if (!strategyConfig) {
          console.error('Strategy config required for realtime selection (--config)');
          process.exit(1);
        }
        result = await runRealtimeSelection({
          strategyConfig,
          headed: args.headed,
          forceRefresh: args['force-refresh']
        });
        console.log(`\nRealtime Selection: ${result.stocks.length} stocks`);
        console.log(`Result: ${result.resultPath}`);
        break;
      }

      case 'history': {
        if (!strategyConfig) {
          console.error('Strategy config required for historical selection (--config)');
          process.exit(1);
        }
        if (!args.date) {
          console.error('--date required for historical selection');
          process.exit(1);
        }
        result = await runHistoricalSelection({
          strategyConfig,
          date: args.date,
          headed: args.headed,
          forceRefresh: args['force-refresh']
        });
        console.log(`\nHistorical Selection (${result.date}): ${result.stocks.length} stocks`);
        console.log(`Result: ${result.resultPath}`);
        break;
      }

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
