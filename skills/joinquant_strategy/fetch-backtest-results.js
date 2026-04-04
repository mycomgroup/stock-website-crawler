#!/usr/bin/env node
/**
 * 查询聚宽策略回测结果
 *
 * 用法：
 *   # 列出策略所有回测（摘要）
 *   node fetch-backtest-results.js --algorithm-id <id> --list
 *
 *   # 最近一次完整结果
 *   node fetch-backtest-results.js --algorithm-id <id> --latest
 *
 *   # 指定 backtestId 查完整结果
 *   node fetch-backtest-results.js --backtest-id <id> --algorithm-id <id>
 *
 *   # 保存结果到文件
 *   node fetch-backtest-results.js --algorithm-id <id> --latest --save
 */
import './load-env.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

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

function printList(backtests) {
  console.log(`\n共 ${backtests.length} 条回测记录：\n`);
  backtests.forEach((b, i) => {
    console.log(`[${i + 1}] ID: ${b.id || b.backtestId}`);
    console.log(`    名称: ${b.name || 'N/A'}  时间: ${b.time || 'N/A'}  状态: ${b.state || 'N/A'}`);
    console.log('');
  });
}

function printSummary(summary, backtestId) {
  console.log(`\n回测 ID: ${backtestId}`);
  if (!summary || Object.keys(summary).length === 0) {
    console.log('暂无摘要数据');
    return;
  }
  const pct = v => v != null ? (v * 100).toFixed(2) + '%' : 'N/A';
  console.log('年化收益:', pct(summary.annualized_returns));
  console.log('总收益:  ', pct(summary.total_returns));
  console.log('夏普比率:', summary.sharpe?.toFixed(3) ?? 'N/A');
  console.log('最大回撤:', pct(summary.max_drawdown));
  console.log('Alpha:   ', pct(summary.alpha));
  console.log('Beta:    ', summary.beta?.toFixed(3) ?? 'N/A');
  console.log('胜率:    ', pct(summary.win_rate));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const algorithmId = args['algorithm-id'];
  const backtestId  = args['backtest-id'];
  const { list, latest, save } = args;

  if (!algorithmId) {
    console.error('Error: 需要 --algorithm-id');
    console.log('\n示例:');
    console.log('  node fetch-backtest-results.js --algorithm-id <id> --list');
    console.log('  node fetch-backtest-results.js --algorithm-id <id> --latest');
    console.log('  node fetch-backtest-results.js --algorithm-id <id> --backtest-id <btId>');
    process.exit(1);
  }

  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();

  // 获取 context（含 CSRF token，后续查询需要）
  console.log('获取策略上下文...');
  const context = await client.getStrategyContext(algorithmId);
  console.log('策略名称:', context.name);

  let data;

  if (backtestId) {
    // 直接查指定回测
    console.log(`\n查询回测 ${backtestId}...`);
    const result = await client.getBacktestResult(backtestId, context);
    const summary = result.data?.result?.summary || {};
    printSummary(summary, backtestId);
    data = { backtestId, result };
  } else if (list) {
    // 列出所有回测
    const backtests = await client.getBacktests(algorithmId);
    printList(backtests);
    data = backtests;
  } else if (latest) {
    // 最近一次完整结果
    const backtests = await client.getBacktests(algorithmId);
    if (!backtests.length) { console.log('没有找到回测记录'); return; }
    const bt = backtests[0];
    const btId = bt.id || bt.backtestId;
    console.log(`\n最近回测 ID: ${btId}  时间: ${bt.time}`);
    const result = await client.getBacktestResult(btId, context);
    const summary = result.data?.result?.summary || {};
    printSummary(summary, btId);
    data = { backtest: bt, backtestId: btId, result };
  } else {
    // 默认：列表 + 最近结果
    const backtests = await client.getBacktests(algorithmId);
    printList(backtests);
    if (backtests.length > 0) {
      const bt = backtests[0];
      const btId = bt.id || bt.backtestId;
      const result = await client.getBacktestResult(btId, context);
      const summary = result.data?.result?.summary || {};
      console.log('--- 最近一次回测结果 ---');
      printSummary(summary, btId);
      data = { list: backtests, latest: { backtestId: btId, result } };
    }
  }

  if (save && data) {
    const filePath = client.writeArtifact(`jq-backtest-query-${algorithmId}`, data);
    console.log('\n结果已保存:', filePath);
  }
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
