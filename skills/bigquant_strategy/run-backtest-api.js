#!/usr/bin/env node
/**
 * BigQuant Strategy Runner
 *
 * Run strategies on BigQuant platform via HTTP API.
 *
 * Usage:
 *   node run-backtest-api.js --strategy path/to/strategy.py
 *   node run-backtest-api.js --strategy path/to/strategy.py --start-date 2022-01-01 --end-date 2023-12-31
 */

import './load-env.js';
import { BigQuantNotebookClient } from './request/bigquant-notebook-client.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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

async function runBacktest(args) {
  console.log('='.repeat(60));
  console.log('BigQuant Strategy Runner (API)');
  console.log('='.repeat(60));

  // Get strategy code
  let code = '';
  let strategyName = 'strategy';

  if (args.strategy) {
    const strategyPath = path.resolve(args.strategy);
    if (!fs.existsSync(strategyPath)) {
      console.error('Strategy file not found:', strategyPath);
      process.exit(1);
    }
    code = fs.readFileSync(strategyPath, 'utf8');
    strategyName = path.basename(strategyPath, '.py');
    console.log('Strategy file:', strategyPath);
  } else if (args.code) {
    code = args.code;
    strategyName = 'inline_code';
  } else {
    // Use a simple test strategy
    code = `# BigQuant Test Strategy
# Simple moving average crossover

import bigquant as bq

# Configure backtest
start_date = '${args['start-date'] || '2023-01-01'}'
end_date = '${args['end-date'] || '2023-12-31'}'

print(f"Running backtest from {start_date} to {end_date}")

# Get stock data
instruments = ['000300.XSHG']  # CSI 300 index
print(f"Instruments: {instruments}")
`;
    strategyName = 'test_strategy';
    console.log('Using default test strategy');
  }

  console.log('Strategy name:', strategyName);

  // Create notebook client
  const apiClient = new BigQuantAPIClient();

  // Get studio info
  console.log('\n[Step 1] Getting studio info...');
  const studio = await apiClient.getDefaultStudio();
  const studioId = studio.data?.id;
  console.log('Studio ID:', studioId);
  console.log('Studio status:', studio.data?.status);

  const client = new BigQuantNotebookClient({ studioId });

  // Create and run backtest
  console.log('\n[Step 2] Creating backtest task...');
  const result = await client.runBacktest(code, {
    name: strategyName,
    startDate: args['start-date'] || '2023-01-01',
    endDate: args['end-date'] || '2023-12-31',
    capital: parseInt(args.capital) || 100000,
    benchmark: args.benchmark || '000300.XSHG'
  });

  console.log('\n' + '='.repeat(60));
  console.log('Task Created Successfully');
  console.log('='.repeat(60));
  console.log('Task ID:', result.taskId);
  console.log('Taskrun ID:', result.taskrunId);
  console.log('Results saved to:', result.outputPath);
  console.log('\nWeb URL:', result.webUrl);
  console.log('\nNote: Open the Web URL in your browser to run/view the backtest');
  console.log('The task has been created and queued for execution.');
  console.log('='.repeat(60));

  return result;
}

const args = parseArgs(process.argv.slice(2));
runBacktest(args).catch(console.error);