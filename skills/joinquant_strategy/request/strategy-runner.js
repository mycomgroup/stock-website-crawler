#!/usr/bin/env node
import fs from 'node:fs';
import { JoinQuantStrategyClient } from './joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './ensure-session.js';

export async function runStrategyWorkflow(options = {}) {
  const {
    algorithmId,
    codeFilePath,
    startTime,
    endTime,
    baseCapital,
    frequency = 'day'
  } = options;

  if (!algorithmId) throw new Error('Missing algorithmId');
  if (!codeFilePath || !fs.existsSync(codeFilePath)) throw new Error(`Strategy file not found: ${codeFilePath}`);

  const code = fs.readFileSync(codeFilePath, 'utf8');

  // 1. Ensure session
  await ensureJoinQuantSession({ algorithmId, ...options });

  const client = new JoinQuantStrategyClient(options);

  // 2. Get context (CSRF token)
  console.log(`Fetching context for strategy ${algorithmId}...`);
  const context = await client.getStrategyContext(algorithmId);
  console.log(`Target strategy name: ${context.name}`);

  // 3. Save/Sync code
  console.log('Syncing local code to JoinQuant...');
  await client.saveStrategy(algorithmId, context.name, code, context);

  // 4. Run Backtest
  console.log(`Starting backtest from ${startTime} to ${endTime}...`);
  const buildResult = await client.runBacktest(algorithmId, code, {
    startTime,
    endTime,
    baseCapital,
    frequency
  }, context);

  const backtestId = buildResult.backtestId;
  console.log(`Backtest started! ID: ${backtestId}`);

// 5. Poll for results
  console.log('Waiting for backtest to complete...');
  let status = 'running';
  
  while (status === 'running' || status === 'waiting') {
    await new Promise(resolve => setTimeout(resolve, 5000));
    const result = await client.getBacktestResult(backtestId, context);
    
    const bt = result.data?.result?.backtest || result.data?.backtest || {};
    const summary = result.data?.result?.summary || {};
    process.stdout.write(`[Status: ${bt.status}, Progress: ${bt.progress || 0}%]`);
    
    if (result.status === 'error' || result.data?.status === 'error' || bt.status === 'error') {
        const errorMsg = result.message || result.data?.message || result.error || 'Unknown backtest error';
        throw new Error(`Backtest failed: ${errorMsg}`);
    }
    
    // The exact response structure from /algorithm/backtest/result?ajax=1:
    // It returns data about the backtest. If finished, it might have a 'finished' flag or a specific status.
    // Let's assume for now we look for 'finished_time' or similar.
    if (bt.finished_time || bt.status === 'finished') {
        status = 'finished';
    }
  else if (result.data?.backtest?.status === 'failed') {
        status = 'failed';
        throw new Error('Backtest failed on server.');
    }
    
    process.stdout.write('.');
  }
  console.log('\nBacktest completed!');

  // 6. Fetch Full Report
  console.log('Fetching detailed report (trades, positions, logs)...');
  const fullReport = await client.getFullReport(backtestId, context);

  // 7. Save results artifact
  const resultPath = client.writeArtifact(`backtest-full-${backtestId}`, fullReport);
  console.log(`Detailed report saved to: ${resultPath}`);

  return {
    backtestId,
    resultPath,
    summary: fullReport.summary
  };
}
