#!/usr/bin/env node
/**
 * 查询同花顺 SuperMind 策略回测结果
 *
 * 用法：
 *   # 列出策略所有回测（摘要）
 *   node fetch-backtest-results.js --algo-id <id> --list
 *
 *   # 最近一次完整结果
 *   node fetch-backtest-results.js --algo-id <id> --latest
 *
 *   # 指定 backtestId 查完整结果
 *   node fetch-backtest-results.js --backtest-id <id>
 *
 *   # 保存结果到文件
 *   node fetch-backtest-results.js --algo-id <id> --latest --save
 */
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';

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
    const id = b.backtest_id || b._id || b.id;
    const status = b.status || 'unknown';
    const created = b.created_time || b.create_time || b.modified || '';
    const start = b.begin_date || b.start_date || '';
    const end   = b.end_date || '';
    console.log(`[${i + 1}] ID: ${id}`);
    console.log(`    状态: ${status}  创建: ${created}`);
    console.log(`    区间: ${start} ~ ${end}`);
    console.log('');
  });
}

function printPerf(perf, backtestId) {
  console.log(`\n回测 ID: ${backtestId}`);
  if (!perf) { console.log('暂无绩效数据'); return; }
  const pct = v => v != null ? (Number(v) * 100).toFixed(2) + '%' : 'N/A';
  console.log('总收益:  ', pct(perf.yield));
  console.log('年化收益:', pct(perf.annual_yield));
  console.log('基准收益:', pct(perf.benchmark_yield));
  console.log('最大回撤:', pct(perf.max_drawdown));
  console.log('夏普比率:', perf.sharpe_ratio ?? 'N/A');
  console.log('Alpha:   ', perf.alpha ?? 'N/A');
  console.log('Beta:    ', perf.beta ?? 'N/A');
  console.log('胜率:    ', pct(perf.win_rate));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const algoId     = args['algo-id'];
  const backtestId = args['backtest-id'];
  const { list, latest, save } = args;

  if (!algoId && !backtestId) {
    console.error('Error: 需要 --algo-id 或 --backtest-id');
    console.log('\n示例:');
    console.log('  node fetch-backtest-results.js --algo-id <id> --list');
    console.log('  node fetch-backtest-results.js --algo-id <id> --latest');
    console.log('  node fetch-backtest-results.js --backtest-id <id>');
    process.exit(1);
  }

  const credentials = {
    username: process.env.THSQUANT_USERNAME,
    password: process.env.THSQUANT_PASSWORD
  };
  const cookies = await ensureTHSQuantSession(credentials);
  const client = new THSQuantClient({ cookies });

  const login = await client.checkLogin();
  if (!login.logged) { console.error('Error: 会话无效'); process.exit(1); }
  console.log('已登录 user_id:', login.userId);

  let data;

  if (backtestId) {
    // 直接查指定回测
    console.log(`\n查询回测 ${backtestId}...`);
    const report = await client.getFullReport(backtestId);
    const perf = report.detail?.performance || report.performance || {};
    printPerf(perf, backtestId);
    data = report;
  } else if (list) {
    // 列出所有回测
    const backtests = await client.listBacktests(algoId, 1, 50);
    printList(backtests);
    data = backtests;
  } else if (latest) {
    // 最近一次完整结果
    const bt = await client.getLatestBacktest(algoId);
    if (!bt) { console.log('没有找到回测记录'); return; }
    const btId = bt.backtest_id || bt._id || bt.id;
    console.log(`\n最近回测 ID: ${btId}`);
    const report = await client.getFullReport(btId);
    const perf = report.detail?.performance || report.performance || {};
    printPerf(perf, btId);
    data = { backtest: bt, backtestId: btId, report };
  } else {
    // 默认：列表 + 最近结果
    const backtests = await client.listBacktests(algoId, 1, 50);
    printList(backtests);
    if (backtests.length > 0) {
      const bt = backtests[0];
      const btId = bt.backtest_id || bt._id || bt.id;
      const report = await client.getFullReport(btId);
      const perf = report.detail?.performance || report.performance || {};
      console.log('--- 最近一次回测结果 ---');
      printPerf(perf, btId);
      data = { list: backtests, latest: { backtestId: btId, report } };
    }
  }

  if (save && data) {
    const tag = algoId ? `algo-${algoId}` : `backtest-${backtestId}`;
    const filePath = client.writeArtifact(`ths-backtest-query-${tag}`, data);
    console.log('\n结果已保存:', filePath);
  }
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
