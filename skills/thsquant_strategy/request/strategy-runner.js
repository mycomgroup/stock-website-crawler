import fs from 'node:fs';
import { THSQuantClient } from './thsquant-client.js';
import { ensureTHSQuantSession } from '../browser/session-manager.js';

/**
 * 完整的 THSQuant 策略回测工作流
 * 对标 joinquant_strategy/request/strategy-runner.js
 */
export async function runStrategyWorkflow(options = {}) {
  const {
    algoId,
    codeFilePath,
    beginDate = '2023-01-01',
    endDate = '2024-12-31',
    capitalBase = '100000',
    frequency = 'DAILY',
    benchmark = '000300.SH',
    headed = false
  } = options;

  if (!algoId) throw new Error('Missing algoId');
  if (!codeFilePath || !fs.existsSync(codeFilePath)) {
    throw new Error(`Strategy file not found: ${codeFilePath}`);
  }

  const code = fs.readFileSync(codeFilePath, 'utf8');

  // 1. 确保 session 有效
  console.log('1. Ensuring session...');
  const credentials = {
    username: process.env.THSQUANT_USERNAME,
    password: process.env.THSQUANT_PASSWORD
  };
  const cookies = await ensureTHSQuantSession(credentials);
  const client = new THSQuantClient({ cookies });

  // 2. 验证登录
  console.log('2. Checking login...');
  const login = await client.checkLogin();
  if (!login.logged) throw new Error('Not logged in. Session may have expired.');
  console.log(`   Logged in as user_id=${login.userId}`);

  // 3. 获取策略信息
  console.log(`3. Fetching strategy info (${algoId})...`);
  const strategyInfo = await client.getStrategyInfo(algoId);
  console.log(`   Strategy: ${strategyInfo.algo_name}`);

  // 4. 保存策略代码
  console.log('4. Saving strategy code...');
  const saveResult = await client.saveStrategy(algoId, strategyInfo.algo_name, code);
  if (!saveResult.success) {
    console.warn(`   Warning: save returned ${saveResult.message}`);
  } else {
    console.log('   Code saved.');
  }

  // 5. 运行回测
  console.log(`5. Starting backtest (${beginDate} ~ ${endDate})...`);
  const runResult = await client.runBacktest(algoId, { beginDate, endDate, capitalBase, frequency, benchmark });
  const backtestId = runResult.backtestId;
  console.log(`   Backtest started! ID: ${backtestId}`);

  // 6. 等待完成
  console.log('6. Waiting for backtest to complete...');
  const waitResult = await client.waitForBacktest(backtestId, {
    maxWait: 300000,
    interval: 3000,
    onProgress: ({ status, progress }) => {
      process.stdout.write(`\r   Status: ${status || 'running'} (${Math.round((progress || 0) * 100)}%)`);
    }
  });
  console.log('');

  if (!waitResult.success) {
    throw new Error(`Backtest failed: ${waitResult.error}`);
  }
  console.log('   Backtest completed!');

  // 7. 获取完整报告
  console.log('7. Fetching full report...');
  const report = await client.getFullReport(backtestId);

  // 8. 保存结果
  const resultPath = client.writeArtifact(`thsquant-backtest-${backtestId}`, report);
  console.log(`   Report saved: ${resultPath}`);

  // 打印摘要
  const perf = report.detail?.performance || report.performance || {};
  const summary = {
    backtestId,
    algoId,
    period: `${beginDate} ~ ${endDate}`,
    yield: perf.yield,
    annualYield: perf.annual_yield,
    maxDrawdown: perf.max_drawdown,
    sharpe: perf.sharpe_ratio || report.performance?.sharpe_ratio,
    winRate: perf.win_rate,
    benchmarkYield: perf.benchmark_yield
  };

  return { backtestId, resultPath, summary };
}
