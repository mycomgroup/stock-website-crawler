#!/usr/bin/env node
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';
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

async function runBacktest(options) {
  const { id, file, start, end, capital, freq, benchmark } = options;
  
  if (!id || !file) {
    console.error('Error: --id and --file are required');
    console.log('\nUsage: node run-skill.js --id <strategyId> --file <path> [options]');
    console.log('\nOptions:');
    console.log('  --start <date>    Start date (default: 2023-01-01)');
    console.log('  --end <date>      End date (default: 2024-12-31)');
    console.log('  --capital <num>   Initial capital (default: 100000)');
    console.log('  --freq <string>   1d, 1h, 1m (default: 1d)');
    console.log('  --benchmark <id>  Benchmark index (default: 000001.SH)');
    return null;
  }
  
  if (!fs.existsSync(file)) {
    console.error('Error: File not found:', file);
    return null;
  }
  
  const code = fs.readFileSync(file, 'utf8');
  
  console.log('='.repeat(60));
  console.log('THSQuant (同花顺量化) Backtest Runner');
  console.log('='.repeat(60));
  console.log('Strategy ID:', id);
  console.log('Strategy File:', file);
  console.log('Start Date:', start || '2023-01-01');
  console.log('End Date:', end || '2024-12-31');
  console.log('Initial Capital:', capital || '100000');
  console.log('Frequency:', freq || '1d');
  console.log('Benchmark:', benchmark || '000001.SH');
  console.log('='.repeat(60) + '\n');
  
  try {
    console.log('1. Verifying session...');
    const credentials = {
      username: process.env.THSQUANT_USERNAME,
      password: process.env.THSQUANT_PASSWORD
    };
    const cookies = await ensureTHSQuantSession(credentials);
    console.log('   Session OK (' + cookies.length + ' cookies)');
    
    const client = new THSQuantClient({ cookies });
    
    console.log('\n2. Checking login status...');
    const loginStatus = await client.checkLogin();
    
    if (loginStatus.code === -1 || loginStatus.code === 401) {
      console.error('Error: Session invalid after verification');
      return null;
    }
    console.log('   Logged in successfully');
    
    console.log('\n3. Getting strategy context...');
    const context = await client.getStrategyContext(id);
    console.log('   Strategy name:', context.name || 'N/A');
    
    console.log('\n4. Saving strategy code...');
    const saveResult = await client.saveStrategy(id, context.name || 'Strategy', code, context);
    console.log('   Save result:', saveResult?.message || 'OK');
    
    console.log('\n5. Starting backtest...');
    const backtestResult = await client.runBacktest(id, code, {
      startTime: start || '2023-01-01',
      endTime: end || '2024-12-31',
      baseCapital: capital || '100000',
      frequency: freq || '1d',
      benchmark: benchmark || '000001.SH'
    }, context);
    
    console.log('   Backtest result:', JSON.stringify(backtestResult).substring(0, 200));
    
    let backtestId = backtestResult.backtestId || backtestResult._id || backtestResult.id;
    if (typeof backtestId === 'string') {
      backtestId = backtestId.replace(/"/g, '');
    }
    
    if (backtestId) {
      console.log('\n   ✓ Backtest started! ID:', backtestId);
      
      console.log('\n6. Waiting for backtest to complete...');
      let attempts = 0;
      let result = null;
      
      while (attempts < 60) {
        await new Promise(r => setTimeout(r, 3000));
        attempts++;
        
        try {
          result = await client.getBacktestResult(backtestId);
          
          if (!result) {
            process.stdout.write(`   [${attempts}/60] Waiting for result...\r`);
            continue;
          }
          
          if (result.status === 'finished' || result.progress === 100) {
            console.log('\n   ✓ Backtest completed!');
            break;
          }
          
          if (result.status === 'error_exit' || result.status === 'failed') {
            console.log('\n   ✗ Backtest failed:', result.exception || result.message || 'Unknown error');
            break;
          }
          
          const progress = result.progress || 0;
          process.stdout.write(`   [${attempts}/60] Progress: ${progress}%\r`);
        } catch (e) {
          if (e.message && (e.message.includes('network') || e.message.includes('ECONN') || e.message.includes('timeout'))) {
            process.stdout.write(`   [${attempts}/60] Network error, retrying...\r`);
          } else {
            console.log('\n   ✗ Error:', e.message);
          }
        }
      }
      
      if (result) {
        console.log('\n7. Generating full report...');
        const report = await client.getFullReport(backtestId);
        const reportPath = client.writeArtifact(`thsquant-backtest-${backtestId}`, report);
        console.log('   Report saved:', reportPath);
        
        console.log('\n' + '='.repeat(60));
        console.log('Backtest Summary');
        console.log('='.repeat(60));
        
        if (result.summary || result.risk) {
          const summary = result.summary || {};
          const risk = result.risk || {};
          
          console.log('Total Return:', ((risk.total_returns || summary.totalReturn || 0) * 100).toFixed(2), '%');
          console.log('Annual Return:', ((risk.annual_returns || summary.annualReturn || 0) * 100).toFixed(2), '%');
          console.log('Max Drawdown:', ((risk.max_drawdown || summary.maxDrawdown || 0) * 100).toFixed(2), '%');
          console.log('Sharpe Ratio:', risk.sharpe || summary.sharpe || 'N/A');
          console.log('Win Rate:', ((risk.win_rate || summary.winRate || 0) * 100).toFixed(1), '%');
        }
        
        console.log('='.repeat(60));
      }
      
      return backtestId;
    } else {
      console.log('\n   ✗ Failed to start backtest');
      console.log('   Response:', JSON.stringify(backtestResult));
      return null;
    }
    
  } catch (e) {
    console.error('\nError:', e.message);
    console.error(e.stack);
    return null;
  }
}

const args = parseArgs(process.argv.slice(2));
runBacktest({
  id: args.id,
  file: args.file,
  start: args.start,
  end: args.end,
  capital: args.capital,
  freq: args.freq,
  benchmark: args.benchmark
});