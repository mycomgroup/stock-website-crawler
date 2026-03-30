#!/usr/bin/env node
import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';

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

function formatPercent(value) {
  if (value === null || value === undefined) return 'N/A';
  return `${(value * 100).toFixed(2)}%`;
}

function formatNumber(value) {
  if (value === null || value === undefined) return 'N/A';
  return value.toFixed(4);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const backtestId = args.id || args.backtestId;
  const strategyId = args.strategy || args.strategyId;
  const saveFull = args.full || args.save;

  if (!backtestId) {
    console.error('Usage: node fetch-report.js --id <backtestId> [--strategy <strategyId>] [--full]');
    process.exit(1);
  }

  try {
    console.log('Verifying RiceQuant session...');
    const credentials = {
      username: process.env.RICEQUANT_USERNAME,
      password: process.env.RICEQUANT_PASSWORD
    };
    const cookies = await ensureRiceQuantSession(credentials);

    const client = new RiceQuantClient({ cookies });

    let context = {};
    if (strategyId) {
      console.log(`Fetching context for strategy ${strategyId}...`);
      try {
        context = await client.getStrategyContext(strategyId);
      } catch (e) {
        console.log('Warning: Could not fetch strategy context:', e.message);
      }
    }

    console.log(`Fetching report for backtest ${backtestId}...`);
    const report = await client.getFullReport(backtestId, context);

    console.log('\n' + '='.repeat(60));
    console.log('BACKTEST SUMMARY');
    console.log('='.repeat(60));
    
    console.log('\nBasic Info:');
    console.log(`  Backtest ID: ${report.backtestId}`);
    console.log(`  Status: ${report.backtestInfo?.status}`);
    console.log(`  Title: ${report.backtestInfo?.title}`);
    console.log(`  Created: ${report.backtestInfo?.create_at}`);
    console.log(`  Completed: ${report.backtestInfo?.end_at}`);

    if (report.risk) {
      console.log('\nRisk Metrics:');
      console.log(`  Sharpe Ratio: ${formatNumber(report.risk.sharpe)}`);
      console.log(`  Sortino Ratio: ${formatNumber(report.risk.sortino)}`);
      console.log(`  Max Drawdown: ${formatPercent(report.risk.max_drawdown)}`);
      console.log(`  Annual Volatility: ${formatPercent(report.risk.annual_volatility)}`);
      console.log(`  Alpha: ${formatNumber(report.risk.alpha)}`);
      console.log(`  Beta: ${formatNumber(report.risk.beta)}`);
      console.log(`  Information Ratio: ${formatNumber(report.risk.information_ratio)}`);
      console.log(`  Annual Tracking Error: ${formatPercent(report.risk.annual_tracking_error)}`);
      console.log(`  Annual Downside Risk: ${formatPercent(report.risk.annual_downside_risk)}`);
    }

    if (report.calculatedReturn) {
      console.log('\nPosition Summary:');
      console.log(`  Trading Days: ${report.positions?.length || 0}`);
      console.log(`  First Date: ${report.positions?.[0]?.trading_date}`);
      console.log(`  Last Date: ${report.positions?.[report.positions.length - 1]?.trading_date}`);
      console.log(`  Initial Market Value: ${(report.calculatedReturn.firstMarketValue / 10000).toFixed(2)}万`);
      console.log(`  Final Market Value: ${(report.calculatedReturn.lastMarketValue / 10000).toFixed(2)}万`);
      console.log(`  Estimated Return: ${formatPercent(report.calculatedReturn.estimatedReturn)}`);
    }

    console.log('\n' + '='.repeat(60));

    if (saveFull) {
      const resultPath = client.writeArtifact(`backtest-full-${backtestId}`, report);
      console.log(`\nFull report saved to: ${resultPath}`);
    }

  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();