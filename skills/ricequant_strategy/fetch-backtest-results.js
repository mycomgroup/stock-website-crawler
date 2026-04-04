#!/usr/bin/env node
/**
 * 查询 RiceQuant 策略回测结果
 *
 * 用法：
 *   # 查看策略所有回测列表（摘要）
 *   node fetch-backtest-results.js --strategy-id <id> --list
 *
 *   # 查看最近一次回测的完整结果
 *   node fetch-backtest-results.js --strategy-id <id> --latest
 *
 *   # 查看指定 backtestId 的完整结果
 *   node fetch-backtest-results.js --backtest-id <id>
 *
 *   # 保存结果到文件（任意模式均可加）
 *   node fetch-backtest-results.js --strategy-id <id> --latest --save
 */
import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else args[key] = true;
    }
  }
  return args;
}

function formatSummary(result, risk) {
  const r = result?.summary || result?.risk || risk || {};
  return {
    totalReturn:  ((r.total_returns  ?? r.totalReturn  ?? 0) * 100).toFixed(2) + '%',
    annualReturn: ((r.annual_returns ?? r.annualReturn ?? 0) * 100).toFixed(2) + '%',
    maxDrawdown:  ((r.max_drawdown   ?? r.maxDrawdown  ?? 0) * 100).toFixed(2) + '%',
    sharpe:       r.sharpe ?? 'N/A',
    winRate:      ((r.win_rate ?? r.winRate ?? 0) * 100).toFixed(1) + '%',
  };
}

function printList(backtests) {
  console.log(`\n共 ${backtests.length} 条回测记录：\n`);
  backtests.forEach((b, i) => {
    const id = b._id || b.backtest_id || b.id;
    const status = b.status || 'unknown';
    const created = b.created_at || b.createdAt || '';
    const start = b.config?.start_date || b.start_date || '';
    const end   = b.config?.end_date   || b.end_date   || '';
    console.log(`[${i + 1}] ID: ${id}`);
    console.log(`    状态: ${status}  创建: ${created}`);
    console.log(`    区间: ${start} ~ ${end}`);
    console.log('');
  });
}

function printResult({ backtestId, result, risk }) {
  console.log(`\n回测 ID: ${backtestId}`);
  console.log('状态:', result?.status || 'N/A');
  const s = formatSummary(result, risk);
  console.log('总收益:', s.totalReturn);
  console.log('年化收益:', s.annualReturn);
  console.log('最大回撤:', s.maxDrawdown);
  console.log('夏普比率:', s.sharpe);
  console.log('胜率:', s.winRate);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { 'strategy-id': strategyId, 'backtest-id': backtestId, list, latest, save } = args;

  if (!strategyId && !backtestId) {
    console.error('Error: 需要 --strategy-id 或 --backtest-id');
    console.log('\n示例:');
    console.log('  node fetch-backtest-results.js --strategy-id <id> --list');
    console.log('  node fetch-backtest-results.js --strategy-id <id> --latest');
    console.log('  node fetch-backtest-results.js --backtest-id <id>');
    process.exit(1);
  }

  // 建立会话
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  };
  const cookies = await ensureRiceQuantSession(credentials);
  const client = new RiceQuantClient({ cookies });

  // 验证登录
  const loginStatus = await client.checkLogin();
  if (loginStatus.code !== 0) {
    console.error('Error: 会话无效，请重新登录');
    process.exit(1);
  }
  console.log('已登录:', loginStatus.fullname || loginStatus.phone);

  let data;

  if (backtestId) {
    // 直接查指定回测
    data = await client.getBacktestResultById(backtestId);
    printResult(data);
  } else if (list) {
    // 列出所有回测
    const backtests = await client.listStrategyBacktests(strategyId);
    printList(backtests);
    data = backtests;
  } else if (latest) {
    // 最近一次完整结果
    data = await client.getLatestBacktestResult(strategyId);
    printResult(data);
  } else {
    // 默认：列表 + 最近结果
    const backtests = await client.listStrategyBacktests(strategyId);
    printList(backtests);
    if (backtests.length > 0) {
      const latestId = backtests[0]._id || backtests[0].backtest_id || backtests[0].id;
      data = await client.getBacktestResultById(latestId);
      console.log('\n--- 最近一次回测结果 ---');
      printResult(data);
    }
    data = { list: backtests };
  }

  if (save && data) {
    const tag = strategyId ? `strategy-${strategyId}` : `backtest-${backtestId}`;
    const filePath = client.writeArtifact(`rq-backtest-query-${tag}`, data);
    console.log('\n结果已保存:', filePath);
  }
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
