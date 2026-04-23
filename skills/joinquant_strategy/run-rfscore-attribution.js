#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

const STRATEGIES = [
  {
    name: 'A0_Baseline_EqualWeight',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore_attribution_a0_baseline.py',
    desc: '基准: 等权持有 universe'
  },
  {
    name: 'B1_RFScore7_Only',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore_attribution_b1_rfscore7_only.py',
    desc: '因子贡献: 仅 RFScore=7'
  },
  {
    name: 'C2_RFScore7_PB10',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore_attribution_c2_rfscore7_pb10.py',
    desc: '+PB10过滤: RFScore=7 且 PB前10%'
  },
  {
    name: 'D3_FinalV2_Full',
    file: '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore7_pb10_final_v2.py',
    desc: '完整策略: +市场择时'
  }
];

const BACKTEST_CONFIG = {
  startTime: '2022-01-01',
  endTime: '2025-12-31',
  baseCapital: '100000',
  frequency: 'day'
};

async function runSingleBacktest(client, context, strategy, index) {
  console.log(`\n=== [${index + 1}/${STRATEGIES.length}] ${strategy.name} ===`);
  console.log(`描述: ${strategy.desc}`);

  const code = fs.readFileSync(strategy.file, 'utf8');

  const strategyName = `RFScore_Attr_${strategy.name}`;
  console.log(`更新策略名称: ${strategyName}`);
  await client.saveStrategy(ALGORITHM_ID, strategyName, code, context);

  console.log(`启动回测: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(ALGORITHM_ID, code, BACKTEST_CONFIG, context);

  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  console.log(`回测链接: https://www.joinquant.com/algorithm/backtest?backtestId=${backtestId}`);

  console.log('等待完成...');
  let attempts = 0;
  const maxAttempts = 90;

  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 4000));
    attempts++;

    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};

      process.stdout.write(`[${attempts}/${maxAttempts}] Status: ${bt.status}, Progress: ${bt.progress || 0}%\r`);

      if (result.status === 'error') {
        console.log('\n回测失败:', result.message);
        return { success: false, error: result.message, backtestId, name: strategy.name };
      }

      if (bt.finished_time || bt.status === 'finished') {
        console.log('\n回测完成!');

        const summary = result.data?.result?.summary || {};

        return {
          success: true,
          backtestId,
          name: strategy.name,
          desc: strategy.desc,
          summary: {
            totalReturn: summary.total_returns || 0,
            annualReturn: summary.annual_returns || 0,
            sharpe: summary.sharpe || 0,
            maxDrawdown: summary.max_drawdown || 0,
            winRate: summary.win_rate || 0,
            tradeCount: summary.trade_count || 0
          }
        };
      }

      if (bt.status === 'failed') {
        console.log('\n回测服务器失败');
        return { success: false, error: 'Server failed', backtestId, name: strategy.name };
      }
    } catch (err) {
      console.log('\n查询结果错误:', err.message);
    }
  }

  console.log('\n等待超时');
  return { success: false, error: 'Timeout', backtestId, name: strategy.name };
}

async function main() {
  console.log('='.repeat(60));
  console.log('RFScore7 PB10 归因分析 - 批量回测');
  console.log('='.repeat(60));
  console.log('\n分层策略:');
  STRATEGIES.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.name}`);
    console.log(`     ${s.desc}`);
  });

  await ensureJoinQuantSession({ headed: false, headless: true });

  const client = new JoinQuantStrategyClient();
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('\n目标策略:', context.name);

  const results = [];

  for (let i = 0; i < STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, context, STRATEGIES[i], i);
    results.push(result);

    if (result.success) {
      console.log(`\n✓ ${result.name} 完成`);
      console.log(`  累计收益: ${(result.summary.totalReturn * 100).toFixed(2)}%`);
      console.log(`  年化收益: ${(result.summary.annualReturn * 100).toFixed(2)}%`);
      console.log(`  夏普比率: ${result.summary.sharpe.toFixed(3)}`);
      console.log(`  最大回撤: ${(result.summary.maxDrawdown * 100).toFixed(2)}%`);
      console.log(`  交易次数: ${result.summary.tradeCount}`);
    } else {
      console.log(`\n✗ 失败: ${result.error}`);
    }

    await new Promise(resolve => setTimeout(resolve, 3000));
  }

  console.log('\n\n' + '='.repeat(60));
  console.log('归因分析汇总');
  console.log('='.repeat(60));

  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);

  console.log(`\n成功: ${successful.length}/${results.length}`);
  console.log(`失败: ${failed.length}/${results.length}`);

  if (successful.length > 0) {
    console.log('\n对比表格:');
    console.log('-'.repeat(100));
    console.log('Name               | TotalReturn | AnnualReturn | Sharpe | MaxDD  | Trades | 描述');
    console.log('-'.repeat(100));

    successful.sort((a, b) => (b.summary.annualReturn || 0) - (a.summary.annualReturn || 0));

    for (const s of successful) {
      const name = s.name.padEnd(19);
      const totalRet = (s.summary.totalReturn * 100).toFixed(2).padStart(11);
      const annualRet = (s.summary.annualReturn * 100).toFixed(2).padStart(12);
      const sharpe = s.summary.sharpe.toFixed(3).padStart(7);
      const maxDD = (s.summary.maxDrawdown * 100).toFixed(2).padStart(6);
      const trades = String(s.summary.tradeCount).padStart(7);
      const desc = s.desc.substring(0, 30);
      console.log(`${name} | ${totalRet}% | ${annualRet}% | ${sharpe} | ${maxDD}% | ${trades} | ${desc}`);
    }

    console.log('-'.repeat(100));

    if (successful.length >= 2) {
      const baseline = successful.find(r => r.name === 'A0_Baseline_EqualWeight');
      const rfscore7Only = successful.find(r => r.name === 'B1_RFScore7_Only');
      const rfscore7PB10 = successful.find(r => r.name === 'C2_RFScore7_PB10');
      const fullStrategy = successful.find(r => r.name === 'D3_FinalV2_Full');

      console.log('\n边际贡献分析:');
      console.log('-'.repeat(60));

      if (baseline && rfscore7Only) {
        const factorContrib = (rfscore7Only.summary.annualReturn - baseline.summary.annualReturn) * 100;
        console.log(`RFScore=7 因子贡献:    ${factorContrib > 0 ? '+' : ''}${factorContrib.toFixed(2)}% 年化`);
      }

      if (rfscore7Only && rfscore7PB10) {
        const pbContrib = (rfscore7PB10.summary.annualReturn - rfscore7Only.summary.annualReturn) * 100;
        console.log(`PB10 过滤边际贡献:  ${pbContrib > 0 ? '+' : ''}${pbContrib.toFixed(2)}% 年化`);
      }

      if (rfscore7PB10 && fullStrategy) {
        const timingContrib = (fullStrategy.summary.annualReturn - rfscore7PB10.summary.annualReturn) * 100;
        console.log(`市场择时边际贡献:  ${timingContrib > 0 ? '+' : ''}${timingContrib.toFixed(2)}% 年化`);
      }
    }
  }

  const outputPath = path.join(client.outputRoot, `rfscore-attribution-${Date.now()}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log('\n结果已保存:', outputPath);
}

main().catch(err => {
  console.error('批量回测失败:', err);
  process.exit(1);
});