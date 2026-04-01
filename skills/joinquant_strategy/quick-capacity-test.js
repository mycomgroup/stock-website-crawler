#!/usr/bin/env node
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import fs from 'node:fs';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGY_CODE = `
from jqdata import *

SLIPPAGE_BPS = 0
CAPITAL_LIMIT = 0

def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    
    if SLIPPAGE_BPS > 0:
        set_slippage(FixedSlippage(SLIPPAGE_BPS / 10000))
    
    set_benchmark("000300.XSHG")
    g.trades = 0
    g.pnl_list = []
    
    run_daily(select, "09:00")
    run_daily(buy, "09:31")
    run_daily(sell, "14:50")


def select(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")
    
    stocks = get_all_securities("stock", prev_date).index.tolist()
    stocks = [s for s in stocks if s[0] not in "483" and s[:2] != "68"]
    
    df = get_price(stocks, end_date=prev_date, count=1,
                   fields=["close", "high_limit"], panel=False)
    df = df.dropna()
    hl = df[df["close"] == df["high_limit"]]
    g.target = list(hl["code"])[:15]


def buy(context):
    if not g.target:
        return
    
    current_data = get_current_data()
    buy_list = []
    
    for s in g.target:
        cd = current_data.get(s)
        if cd is None or cd.paused or cd.is_st:
            continue
        
        open_pct = (cd.day_open - cd.pre_close) / cd.pre_close * 100
        if -1.5 <= open_pct <= 1.5:
            buy_list.append(s)
    
    if buy_list:
        cash = context.portfolio.available_cash / min(len(buy_list), 3)
        for s in buy_list[:3]:
            if CAPITAL_LIMIT > 0 and cash > CAPITAL_LIMIT:
                cash = CAPITAL_LIMIT
            order_value(s, cash)
            g.trades += 1


def sell(context):
    for s in list(context.portfolio.positions):
        if context.portfolio.positions[s].closeable_amount > 0:
            order_target(s, 0)
`;

async function runTest(client, context, testName, params) {
  console.log(`\n=== ${testName} ===`);
  
  const code = STRATEGY_CODE
    .replace(/SLIPPAGE_BPS = \d+/, `SLIPPAGE_BPS = ${params.slippage}`)
    .replace(/CAPITAL_LIMIT = \d+/, `CAPITAL_LIMIT = ${params.capitalLimit}`);
  
  const strategyName = `容量滑点测试_${testName}`;
  
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);
  
  const config = {
    startTime: '2024-11-01',
    endTime: '2024-11-30',
    baseCapital: params.capital,
    frequency: 'day'
  };
  
  console.log(`Capital: ${params.capital}, Slippage: ${params.slippage}bps`);
  
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, config, context);
  const backtestId = buildResult.backtestId;
  
  console.log(`Backtest ID: ${backtestId}`);
  
  let attempts = 0;
  const maxAttempts = 40;
  
  while (attempts < maxAttempts) {
    await new Promise(r => setTimeout(r, 3000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};
      
      if (result.status === 'error') {
        return { error: result.message };
      }
      
      if (bt.finished_time || bt.status === 'finished') {
        const summary = result.data?.result?.summary || {};
        console.log(`✓ Annual: ${summary.annual_returns?.toFixed(2)}%, Trades: ${summary.trade_count}`);
        return {
          success: true,
          testName,
          params,
          summary: {
            annualReturn: summary.annual_returns || 0,
            totalReturn: summary.total_returns || 0,
            maxDrawdown: summary.max_drawdown || 0,
            tradeCount: summary.trade_count || 0,
            winRate: summary.win_rate || 0
          }
        };
      }
      
      if (bt.status === 'failed') {
        return { error: 'Server failed' };
      }
      
      if (attempts % 5 === 0) {
        console.log(`[${attempts}/${maxAttempts}] waiting...`);
      }
    } catch (e) {
      if (attempts % 5 === 0) {
        console.log(`Error: ${e.message.slice(0, 30)}`);
      }
    }
  }
  
  return { error: 'Timeout' };
}

async function main() {
  console.log('=== 容量滑点测试（单月快速版） ===');
  
  await ensureJoinQuantSession({ algorithmId: ALGORITHM_ID });
  
  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  
  const results = [];
  
  // 容量测试 - 只测3个关键规模
  const capacityTests = [
    { name: '容量10万', params: { capital: '100000', slippage: 0, capitalLimit: 0 } },
    { name: '容量100万', params: { capital: '1000000', slippage: 0, capitalLimit: 0 } },
    { name: '容量500万', params: { capital: '5000000', slippage: 0, capitalLimit: 500000 } }
  ];
  
  // 滑点测试 - 只测3个关键滑点
  const slippageTests = [
    { name: '滑点0bps', params: { capital: '1000000', slippage: 0, capitalLimit: 0 } },
    { name: '滑点20bps', params: { capital: '1000000', slippage: 20, capitalLimit: 0 } },
    { name: '滑点50bps', params: { capital: '1000000', slippage: 50, capitalLimit: 0 } }
  ];
  
  for (const test of [...capacityTests, ...slippageTests]) {
    const result = await runTest(client, context, test.name, test.params);
    results.push(result);
    await new Promise(r => setTimeout(r, 2000));
  }
  
  console.log('\n=== 结果汇总 ===');
  
  const successful = results.filter(r => r.success);
  
  if (successful.length > 0) {
    console.log('\n容量测试:');
    successful.filter(r => r.testName.includes('容量')).forEach(r => {
      console.log(`${r.params.capital}: 年化${r.summary.annualReturn.toFixed(2)}%, 交易${r.summary.tradeCount}次`);
    });
    
    console.log('\n滑点测试:');
    successful.filter(r => r.testName.includes('滑点')).forEach(r => {
      console.log(`${r.params.slippage}bps: 年化${r.summary.annualReturn.toFixed(2)}%`);
    });
  } else {
    console.log('无成功回测');
  }
  
  fs.writeFileSync(
    '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/data/quick_results.json',
    JSON.stringify(results, null, 2)
  );
  
  return results;
}

main().catch(e => {
  console.error('Failed:', e);
  process.exit(1);
});