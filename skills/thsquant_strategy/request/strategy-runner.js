import fs from 'node:fs';
import path from 'node:path';
import { THSQuantClient } from './thsquant-client.js';
import { ensureTHSQuantSession } from '../browser/session-manager.js';

/**
 * 完整的 THSQuant 策略回测工作流
 * 对标 joinquant_strategy/request/strategy-runner.js
 *
 * 设计原则:
 * - 每次提交创建新策略，历史策略不删除
 * - 策略名包含业务含义：{name}_{YYYYMMDD}_{beginDate}~{endDate}
 * - 结果数据尽量丰富
 */
export async function runStrategyWorkflow(options = {}) {
  const {
    algoId,           // 如果提供则更新已有策略；否则创建新策略
    strategyName,     // 业务名称，如 "rfscore7_pb10_v1"
    codeFilePath,
    beginDate = '2023-01-01',
    endDate = '2024-12-31',
    capitalBase = '100000',
    frequency = 'DAILY',
    benchmark = '000300.SH',
    headed = false,
    createNew = true  // 默认每次创建新策略
  } = options;

  if (!codeFilePath || !fs.existsSync(codeFilePath)) {
    throw new Error(`Strategy file not found: ${codeFilePath}`);
  }

  const code = fs.readFileSync(codeFilePath, 'utf8');

  // 生成带业务含义的策略名
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const baseName = strategyName || path.basename(codeFilePath, path.extname(codeFilePath));
  const fullName = `${baseName}_${today}_${beginDate.replace(/-/g, '')}~${endDate.replace(/-/g, '')}`;

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

  let targetAlgoId = algoId;

  if (createNew || !algoId) {
    // 3. 创建新策略（保留历史）
    console.log(`3. Creating new strategy: "${fullName}"...`);
    const created = await client.createStrategy(fullName, code);
    if (!created.success) throw new Error(`Failed to create strategy: ${created.message}`);
    targetAlgoId = created.algoId;
    console.log(`   Created strategy ID: ${targetAlgoId}`);
  } else {
    // 3. 更新已有策略代码
    console.log(`3. Updating strategy ${algoId}...`);
    const info = await client.getStrategyInfo(algoId);
    console.log(`   Strategy: ${info.algo_name}`);
    const saved = await client.saveStrategy(algoId, info.algo_name, code);
    if (!saved.success) console.warn(`   Warning: save returned ${saved.message}`);
    else console.log('   Code saved.');
    targetAlgoId = algoId;
  }

  // 4. 运行回测
  console.log(`4. Starting backtest (${beginDate} ~ ${endDate}, capital=${capitalBase}, freq=${frequency})...`);
  const runResult = await client.runBacktest(targetAlgoId, { beginDate, endDate, capitalBase, frequency, benchmark });
  const backtestId = runResult.backtestId;
  console.log(`   Backtest started! ID: ${backtestId}`);

  // 5. 等待完成
  console.log('5. Waiting for backtest to complete...');
  const waitResult = await client.waitForBacktest(backtestId, {
    maxWait: 300000,
    interval: 3000,
    onProgress: ({ status, progress }) => {
      process.stdout.write(`\r   Status: ${status || 'running'} (${Math.round((progress || 0) * 100)}%)`);
    }
  });  console.log('');

  if (!waitResult.success) {
    throw new Error(`Backtest failed: ${waitResult.error}`);
  }
  console.log('   Backtest completed!');

  // 6. 获取完整报告（丰富数据）
  console.log('6. Fetching full report...');
  const report = await client.getFullReport(backtestId);

  // 7. 构建结构化摘要
  const perf = report.detail?.performance || {};
  const perfFull = report.performance || {};

  const summary = {
    // 基本信息
    backtestId,
    algoId: targetAlgoId,
    strategyName: fullName,
    period: `${beginDate} ~ ${endDate}`,
    capitalBase: Number(capitalBase),
    frequency,
    benchmark,
    runAt: new Date().toISOString(),

    // 收益指标
    totalReturn: perf.yield,
    annualReturn: perf.annual_yield,
    benchmarkReturn: perf.benchmark_yield,
    benchmarkAnnualReturn: perf.benchmark_annual_yield,
    excessReturn: perf.yield != null && perf.benchmark_yield != null
      ? perf.yield - perf.benchmark_yield : null,

    // 风险指标
    maxDrawdown: perf.max_drawdown,
    drawdownDate: perf.drawdown_most,
    volatility: perf.volatility,
    downsideRisk: perf.downside_risk,
    trackingError: perf.tracking_error,

    // 风险调整收益
    sharpe: perfFull.sharpe_ratio || perf.sharpe_ratio,
    sortino: perfFull.sortino,
    alpha: perf.alpha || perfFull.alpha,
    beta: perf.beta || perfFull.beta,
    informationRatio: perf.information_ratio,

    // 交易统计
    winRate: perf.win_rate,
    benchmarkWinRate: perf.benchmark_win_rate,
    tradeWinRate: perf.trade_winrate,
    tradeCount: report.tradeLog?.length || 0,
    logCount: report.backtestLog?.length || 0,
  };

  // 8. 保存结果
  const resultPath = client.writeArtifact(`thsquant-${baseName}-${backtestId}`, {
    summary,
    detail: report.detail,
    performance: report.performance,
    tradeLog: report.tradeLog,
    backtestLog: report.backtestLog,
    dailyGains: report.dailyGains,
    specificInfo: report.specificInfo
  });
  console.log(`   Report saved: ${resultPath}`);

  return { backtestId, algoId: targetAlgoId, resultPath, summary };
}
