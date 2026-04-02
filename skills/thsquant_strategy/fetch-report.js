#!/usr/bin/env node
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';

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

async function fetchReport(options) {
  const { id, full } = options;
  
  if (!id) {
    console.error('Error: --id is required');
    console.log('\nUsage: node fetch-report.js --id <backtestId> [--full]');
    return null;
  }
  
  try {
    const credentials = {
      username: process.env.THSQUANT_USERNAME,
      password: process.env.THSQUANT_PASSWORD
    };
    const cookies = await ensureTHSQuantSession(credentials);
    
    const client = new THSQuantClient({ cookies });
    
    console.log('Fetching backtest report...');
    const report = await client.getFullReport(id);
    
    if (full) {
      const reportPath = client.writeArtifact(`thsquant-report-${id}-full`, report);
      console.log('Full report saved to:', reportPath);
    } else {
      console.log('\n' + '='.repeat(60));
      console.log('Backtest Summary');
      console.log('='.repeat(60));
      
      const summary = report.summary || {};
      const risk = report.risk || {};
      
      console.log('Backtest ID:', id);
      console.log('Total Return:', ((risk.total_returns || summary.totalReturn || 0) * 100).toFixed(2), '%');
      console.log('Annual Return:', ((risk.annual_returns || summary.annualReturn || 0) * 100).toFixed(2), '%');
      console.log('Max Drawdown:', ((risk.max_drawdown || summary.maxDrawdown || 0) * 100).toFixed(2), '%');
      console.log('Sharpe Ratio:', risk.sharpe || summary.sharpe || 'N/A');
      console.log('Win Rate:', ((risk.win_rate || summary.winRate || 0) * 100).toFixed(1), '%');
      console.log('='.repeat(60));
    }
    
    return report;
    
  } catch (e) {
    console.error('Error:', e.message);
    return null;
  }
}

const args = parseArgs(process.argv.slice(2));
fetchReport({ id: args.id, full: args.full });