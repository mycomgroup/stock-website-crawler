#!/usr/bin/env node
import fs from 'node:fs';
import { GuornStrategyClient } from './guorn-strategy-client.js';
import { ensureGuornSession } from './ensure-session.js';

export async function runStrategyWorkflow(options = {}) {
  const {
    strategyConfig,
    backtestConfig,
    headed
  } = options;

  // 1. Ensure session
  await ensureGuornSession({ ...options });

  const client = new GuornStrategyClient(options);

  // 2. Get user profile
  console.log('Fetching user profile...');
  const profile = await client.getUserProfile();
  console.log(`User: ${profile.data?.username || 'Unknown'}`);

  // 3. Save strategy if config provided (requires browser)
  let strategyId = backtestConfig?.strategyId;
  
  if (strategyConfig && !strategyId) {
    console.log('Note: Strategy save requires browser interaction.');
    console.log('Please create the strategy manually and provide the strategy ID.');
    throw new Error('Strategy ID required for backtest. Create strategy manually and use --id option.');
  }

  // 4. Run backtest
  if (!backtestConfig) {
    throw new Error('Missing backtestConfig');
  }

  console.log(`Starting backtest from ${backtestConfig.startTime} to ${backtestConfig.endTime}...`);
  const backtestResult = await client.runBacktest({
    ...backtestConfig,
    strategyId
  });

  if (backtestResult.status !== 'ok') {
    throw new Error(`Failed to start backtest: ${JSON.stringify(backtestResult)}`);
  }

  const backtestId = backtestResult.data?.backtestId;
  console.log(`Backtest started! ID: ${backtestId}`);

  // 5. Poll for results
  console.log('Waiting for backtest to complete...');
  let status = 'running';
  let finalResult = null;
  
  while (status === 'running' || status === 'waiting') {
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    try {
      const result = await client.getBacktestResult(backtestId);
      
      if (result.status === 'error') {
        throw new Error(`Backtest failed: ${result.message || JSON.stringify(result)}`);
      }
      
      const bt = result.data || {};
      process.stdout.write(`[Status: ${bt.status || 'running'}]`);
      
      if (bt.status === 'completed' || bt.finished) {
        status = 'finished';
        finalResult = result;
      } else if (bt.status === 'failed') {
        status = 'failed';
        throw new Error('Backtest failed on server.');
      }
    } catch (e) {
      if (e.message.includes('Backtest failed')) {
        throw e;
      }
      // Network error, retry
      process.stdout.write('.');
    }
  }
  console.log('\nBacktest completed!');

  // 6. Save results artifact
  const resultPath = client.writeArtifact(`backtest-${backtestId}`, finalResult);
  console.log(`Detailed report saved to: ${resultPath}`);

  return {
    backtestId,
    resultPath,
    summary: finalResult?.data || finalResult
  };
}

export async function runRealtimeSelection(options = {}) {
  const {
    strategyConfig,
    headed
  } = options;

  // 1. Ensure session
  await ensureGuornSession({ ...options });

  const client = new GuornStrategyClient(options);

  // 2. Get realtime selection
  console.log('Running realtime selection...');
  const result = await client.getRealtimeSelection(strategyConfig);

  if (result.status !== 'ok') {
    throw new Error(`Realtime selection failed: ${JSON.stringify(result)}`);
  }

  // 3. Save results
  const resultPath = client.writeArtifact('realtime-selection', result);
  console.log(`Selection result saved to: ${resultPath}`);

  return {
    resultPath,
    stocks: result.data?.stocks || []
  };
}

export async function runHistoricalSelection(options = {}) {
  const {
    strategyConfig,
    date,
    headed
  } = options;

  // 1. Ensure session
  await ensureGuornSession({ ...options });

  const client = new GuornStrategyClient(options);

  // 2. Get historical selection
  console.log(`Running historical selection for ${date}...`);
  const result = await client.getHistoricalSelection({
    ...strategyConfig,
    date
  });

  if (result.status !== 'ok') {
    throw new Error(`Historical selection failed: ${JSON.stringify(result)}`);
  }

  // 3. Save results
  const resultPath = client.writeArtifact(`historical-selection-${date}`, result);
  console.log(`Selection result saved to: ${resultPath}`);

  return {
    resultPath,
    date,
    stocks: result.data?.stocks || []
  };
}
