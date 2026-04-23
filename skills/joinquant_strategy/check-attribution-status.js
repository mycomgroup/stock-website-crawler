#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const BACKTEST_IDS = [
  { id: '4d2d8f6fdbd31d4d8ccd1aa72e29cd5f', name: 'A0_Baseline' },
  { id: 'd3b179837cb20e586ee6c21a8ebc6ea2', name: 'B1_RFScore7_Only' },
];

async function main() {
  console.log('检查归因分析回测状态');
  console.log('='.repeat(60));

  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);

  for (const { id, name } of BACKTEST_IDS) {
    console.log(`\n${name}: ${id}`);
    console.log(`链接: https://www.joinquant.com/algorithm/backtest?backtestId=${id}`);

    try {
      const result = await client.getBacktestResult(id, context);

      if (result.data?.result?.summary) {
        const s = result.data.result.summary;
        console.log(`✓ 已完成!`);
        console.log(`  累计收益: ${(s.total_returns * 100).toFixed(2)}%`);
        console.log(`  年化收益: ${(s.annual_returns * 100).toFixed(2)}%`);
        console.log(`  夏普比率: ${s.sharpe?.toFixed(3)}`);
        console.log(`  最大回撤: ${(s.max_drawdown * 100).toFixed(2)}%`);
        console.log(`  交易次数: ${s.trade_count}`);
      } else {
        console.log(`状态: ${result.data?.result?.backtest?.status || 'unknown'}`);
        console.log(`进度: ${result.data?.result?.backtest?.progress || 0}%`);
      }
    } catch (err) {
      console.log(`失败: ${err.message}`);
    }
  }
}

main().catch(console.error);