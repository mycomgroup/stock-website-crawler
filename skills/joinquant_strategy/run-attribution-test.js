#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 四个对比版本
const STRATEGIES = [
  {
    name: 'A_原版_Release_V1',
    file: path.join(__dirname, '../../strategies/rfscore_offensive/rfscore7_pb10_release_v1.py'),
    description: '原版：RFScore7 + PB筛选 + 市场状态风控 + 行业分散',
  },
  {
    name: 'B_纯PB低估值',
    file: path.join(__dirname, 'attribution_b_pure_pb.py'),
    description: '剥离RFScore7，仅保留PB最低10%选股',
  },
  {
    name: 'C_纯RFScore7',
    file: path.join(__dirname, 'attribution_c_pure_rfscore.py'),
    description: '剥离PB筛选，仅按RFScore7打分排序',
  },
  {
    name: 'D_无市场状态风控',
    file: path.join(__dirname, 'attribution_d_no_market_state.py'),
    description: '移除市场状态判断，始终满仓',
  },
];

const BACKTEST_CONFIG = {
  startTime: '2022-01-01',
  endTime: '2025-01-01',
  baseCapital: '1000000',
  frequency: 'day'
};

async function runBacktestForStrategy(client, strategy, algorithmId) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`策略: ${strategy.name}`);
  console.log(`说明: ${strategy.description}`);
  console.log('='.repeat(60));

  const context = await client.getStrategyContext(algorithmId);

  const code = fs.readFileSync(strategy.file, 'utf8');
  const strategyName = `RFScore7_Attribution_${strategy.name}`;
  console.log(`上传策略: ${strategyName}`);
  await client.saveStrategy(algorithmId, strategyName, code, context);

  console.log(`运行回测: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(algorithmId, '', BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);

  console.log('等待回测完成...');
  let retries = 0;
  const maxRetries = 180;

  while (retries < maxRetries) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    const result = await client.getBacktestResult(backtestId, context);

    if (result && result.data && result.data.state === '2') {
      console.log('✓ 回测完成！');
      const stats = await client.getBacktestStats(backtestId, context);
      return { backtestId, stats: stats.data || {} };
    }

    retries++;
    if (retries % 30 === 0) {
      console.log(`  等待中... ${Math.floor(retries * 2 / 60)}分钟`);
    }
  }

  console.log('⚠ 回测超时，获取当前状态...');
  const log = await client.getLog(backtestId);
  return { log, timeout: true };
}

async function main() {
  console.log('RFScore7 因子剥离验证 - 四版本对比');
  console.log('='.repeat(60));
  console.log(`回测区间: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  console.log(`初始资金: ${BACKTEST_CONFIG.baseCapital}`);
  console.log(`\n验证目标:`);
  console.log(`  A vs B: RFScore7是否有增量贡献？`);
  console.log(`  A vs C: PB筛选是否必要？`);
  console.log(`  A vs D: 市场状态风控是否有效？`);

  console.log('\n[准备] 确保 Session 有效...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();

  // 使用同一个algorithmId上传不同版本
  const algorithmId = process.env.ALGORITHM_ID || '801d56e162b037ed1a6e0ba5d26ff092';
  console.log(`使用 Algorithm ID: ${algorithmId}`);

  const results = {};

  for (const strategy of STRATEGIES) {
    try {
      const result = await runBacktestForStrategy(client, strategy, algorithmId);
      results[strategy.name] = {
        description: strategy.description,
        result: result,
      };

      if (result.stats) {
        const s = result.stats;
        console.log('\n回测结果:');
        console.log(`  年化收益: ${(s.annual_algo_return * 100).toFixed(2)}%`);
        console.log(`  累计收益: ${(s.algorithm_return * 100).toFixed(2)}%`);
        console.log(`  夏普比率: ${s.sharpe.toFixed(3)}`);
        console.log(`  最大回撤: ${(s.max_drawdown * 100).toFixed(2)}%`);
        console.log(`  Alpha: ${(s.alpha * 100).toFixed(2)}%`);
        console.log(`  Beta: ${s.beta.toFixed(3)}`);
        console.log(`  胜率: ${(s.win_ratio * 100).toFixed(2)}%`);
      }
    } catch (error) {
      console.error(`策略 ${strategy.name} 执行失败:`, error.message);
      results[strategy.name] = { error: error.message };
    }
  }

  // 生成对比报告
  console.log('\n' + '='.repeat(60));
  console.log('因子剥离验证 - 对比汇总');
  console.log('='.repeat(60));

  const summary = {
    timestamp: new Date().toISOString(),
    backtestConfig: BACKTEST_CONFIG,
    strategies: {},
  };

  for (const [name, data] of Object.entries(results)) {
    if (data.error) {
      summary.strategies[name] = { error: data.error };
      continue;
    }
    const s = data.result.stats;
    if (!s) continue;
    summary.strategies[name] = {
      description: data.description,
      annualized_returns: s.annual_algo_return,
      total_returns: s.algorithm_return,
      sharpe: s.sharpe,
      max_drawdown: s.max_drawdown,
      alpha: s.alpha,
      beta: s.beta,
      win_rate: s.win_ratio,
    };
  }

  // 保存结果
  const outputDir = path.join(__dirname, 'data', `attribution_${Date.now()}`);
  fs.mkdirSync(outputDir, { recursive: true });

  const summaryFile = path.join(outputDir, 'summary.json');
  fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2));
  console.log(`\n完整结果已保存: ${summaryFile}`);

  // 生成Markdown报告
  const mdReport = generateMarkdownReport(summary);
  const mdFile = path.join(outputDir, 'report.md');
  fs.writeFileSync(mdFile, mdReport);
  console.log(`对比报告已保存: ${mdFile}`);
}

function generateMarkdownReport(summary) {
  const strategies = summary.strategies;
  const names = Object.keys(strategies);

  let md = `# RFScore7 因子剥离验证报告\n\n`;
  md += `> 回测区间: ${summary.backtestConfig.startTime} ~ ${summary.backtestConfig.endTime}\n`;
  md += `> 初始资金: ${summary.backtestConfig.baseCapital}\n\n`;

  md += `## 对比结果\n\n`;
  md += `| 策略 | 年化收益 | 累计收益 | 夏普 | 最大回撤 | Alpha | Beta | 胜率 |\n`;
  md += `|------|---------|---------|------|---------|-------|------|------|\n`;

  for (const name of names) {
    const s = strategies[name];
    if (s.error) {
      md += `| ${name} | ERROR: ${s.error} |\n`;
      continue;
    }
    md += `| ${name} | ${(s.annualized_returns * 100).toFixed(2)}% | ${(s.total_returns * 100).toFixed(2)}% | ${s.sharpe.toFixed(3)} | ${(s.max_drawdown * 100).toFixed(2)}% | ${(s.alpha * 100).toFixed(2)}% | ${s.beta.toFixed(3)} | ${(s.win_rate * 100).toFixed(2)}% |\n`;
  }

  md += `\n## 结论分析\n\n`;

  const a = strategies['A_原版_Release_V1'];
  const b = strategies['B_纯PB低估值'];
  const c = strategies['C_纯RFScore7'];
  const d = strategies['D_无市场状态风控'];

  if (a && b && !a.error && !b.error) {
    const diff = a.annualized_returns - b.annualized_returns;
    md += `### RFScore7 增量贡献 (A vs B)\n\n`;
    md += diff > 0.02
      ? `A比B年化高 ${(diff * 100).toFixed(2)}%，说明 **RFScore7有显著增量贡献**。\n\n`
      : diff > -0.02
        ? `A与B年化差异仅 ${(diff * 100).toFixed(2)}%，说明 **RFScore7贡献有限，PB是核心因子**。\n\n`
        : `A比B年化低 ${(Math.abs(diff) * 100).toFixed(2)}%，说明 **RFScore7可能拖累了收益**。\n\n`;
  }

  if (a && c && !a.error && !c.error) {
    const diff = a.annualized_returns - c.annualized_returns;
    md += `### PB筛选必要性 (A vs C)\n\n`;
    md += diff > 0.02
      ? `A比C年化高 ${(diff * 100).toFixed(2)}%，说明 **PB筛选是必要的**。\n\n`
      : `A与C年化差异仅 ${(diff * 100).toFixed(2)}%，说明 **PB筛选不是关键**。\n\n`;
  }

  if (a && d && !a.error && !d.error) {
    const sharpeDiff = a.sharpe - d.sharpe;
    const ddDiff = a.max_drawdown - d.max_drawdown;
    md += `### 市场状态风控有效性 (A vs D)\n\n`;
    md += `夏普差异: ${sharpeDiff.toFixed(3)} (A ${sharpeDiff > 0 ? '更优' : '更差'})\n`;
    md += `最大回撤差异: ${(ddDiff * 100).toFixed(2)}% (A ${ddDiff < 0 ? '回撤更小' : '回撤更大'})\n\n`;
    md += sharpeDiff > 0.1
      ? `结论: **市场状态风控有效提升了风险调整后收益**。\n\n`
      : `结论: **市场状态风控效果不明显**。\n\n`;
  }

  return md;
}

main().catch(console.error);
