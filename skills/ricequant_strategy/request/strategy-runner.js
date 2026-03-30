#!/usr/bin/env node
import fs from 'node:fs';
import { RiceQuantClient } from './ricequant-client.js';
import { ensureRiceQuantSession } from './ensure-session.js';

export async function runStrategyWorkflow(options = {}) {
  const {
    strategyId,
    codeFilePath,
    startTime,
    endTime,
    baseCapital,
    frequency = 'day',
    benchmark = '000300.XSHG'
  } = options;

  if (!strategyId) throw new Error('Missing strategyId');
  if (!codeFilePath || !fs.existsSync(codeFilePath)) {
    throw new Error(`Strategy file not found: ${codeFilePath}`);
  }

  const code = fs.readFileSync(codeFilePath, 'utf8');

  // 1. 确保会话
  console.log('Ensuring RiceQuant session...');
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  };
  await ensureRiceQuantSession(credentials);

  const client = new RiceQuantClient(options);

  // 2. 获取策略上下文
  console.log(`Fetching context for strategy ${strategyId}...`);
  const context = await client.getStrategyContext(strategyId);
  console.log(`Target strategy: ${context.name || strategyId}`);

  // 3. 同步代码
  console.log('Syncing local code to RiceQuant...');
  await client.saveStrategy(strategyId, context.name || 'Strategy', code, context);
  console.log('Code synced successfully');

  // 4. 运行回测
  console.log(`Starting backtest from ${startTime} to ${endTime}...`);
  const backtestResult = await client.runBacktest(strategyId, code, {
    startTime,
    endTime,
    baseCapital,
    frequency,
    benchmark
  }, context);

  const backtestId = backtestResult.backtestId || backtestResult.id;
  console.log(`Backtest started! ID: ${backtestId}`);

  // 5. 轮询等待回测完成
  console.log('Waiting for backtest to complete...');
  let isComplete = false;
  let attempts = 0;
  const maxAttempts = 60; // 最多等待5分钟
  
  while (!isComplete && attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 5000)); // 每5秒检查一次
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId);
      const status = result.status || result.backtest?.status;
      const progress = result.progress || result.backtest?.progress || 0;
      
      process.stdout.write(`\r[Status: ${status || 'running'}, Progress: ${progress}%] Attempt ${attempts}/${maxAttempts}`);
      
      if (status === 'finished' || status === 'completed' || status === 'success') {
        isComplete = true;
        console.log('\nBacktest completed!');
      } else if (status === 'failed' || status === 'error') {
        throw new Error(`Backtest failed: ${result.message || JSON.stringify(result)}`);
      }
    } catch (error) {
      if (attempts >= maxAttempts) {
        throw new Error(`Backtest timeout after ${maxAttempts} attempts: ${error.message}`);
      }
      // 继续等待
    }
  }

  if (!isComplete) {
    throw new Error('Backtest did not complete within timeout period');
  }

  // 6. 获取完整报告
  console.log('Fetching detailed report...');
  const fullReport = await client.getFullReport(backtestId, context);

  // 7. 保存结果
  const resultPath = client.writeArtifact(`backtest-full-${backtestId}`, fullReport);
  console.log(`Detailed report saved to: ${resultPath}`);

  return {
    backtestId,
    resultPath,
    summary: fullReport.summary
  };
}
