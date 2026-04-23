#!/usr/bin/env node
/**
 * 监控所有回测完成并自动分析结果
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 回测列表
const BACKTESTS = [
  {
    name: 'User_Attr_C_Pure_RFScore',
    backtestId: 'a223632fd3e84245a6873552b514c308',
    algorithmId: 'dacacfad48acfd35c72a4a0f6517c519',
    desc: '纯RFScore7质量因子（剥离PB过滤）',
    purpose: '验证RFScore7单独贡献'
  },
  {
    name: 'User_Attr_D_No_Risk_Control',
    backtestId: '9de98ee035a56e7a05288020cca8b591',
    algorithmId: '5c9e4225112d5504433a6231dea8e0a3',
    desc: '无动态风控（始终满仓20只）',
    purpose: '验证动态风控贡献'
  },
  {
    name: 'User_Attr_E_PB20_Loose',
    backtestId: '8c5fe72d29ed1cd3ee438d2ad4c0829a',
    algorithmId: '50a2ce8b72bc5046cd4b9495379935a6',
    desc: 'PB20%宽松版（vs PB10%严格版）',
    purpose: '验证PB严格度是否过拟合'
  }
];

async function checkBacktestStatus(client, backtest) {
  try {
    const context = await client.getStrategyContext(backtest.algorithmId);
    const result = await client.getBacktestResult(backtest.backtestId, context);
    const bt = result.data?.result?.backtest || {};
    
    if (bt.finished_time || bt.status === 'finished') {
      const summary = result.data?.result?.summary || {};
      return {
        success: true,
        finished: true,
        name: backtest.name,
        desc: backtest.desc,
        purpose: backtest.purpose,
        backtestId: backtest.backtestId,
        summary: {
          totalReturn: summary.total_returns || 0,
          annualReturn: summary.annual_returns || 0,
          sharpe: summary.sharpe || 0,
          maxDrawdown: summary.max_drawdown || 0,
          winRate: summary.win_rate || 0,
          tradeCount: summary.trade_count || 0,
          alpha: summary.alpha || 0,
          beta: summary.beta || 0,
          volatility: summary.volatility || 0,
          informationRatio: summary.information_ratio || 0
        }
      };
    }
    
    return {
      success: true,
      finished: false,
      name: backtest.name,
      status: bt.status,
      progress: bt.progress || 0
    };
  } catch (err) {
    return {
      success: false,
      finished: false,
      name: backtest.name,
      error: err.message
    };
  }
}

async function waitForAllBacktests(client) {
  console.log('等待所有回测完成...\n');
  
  let allFinished = false;
  let attempts = 0;
  const maxAttempts = 120; // 最多等待8分钟
  
  while (!allFinished && attempts < maxAttempts) {
    attempts++;
    
    const statuses = await Promise.all(
      BACKTESTS.map(bt => checkBacktestStatus(client, bt))
    );
    
    // 显示进度
    process.stdout.write(`\r[${attempts}/${maxAttempts}] `);
    statuses.forEach(s => {
      if (s.finished) {
        process.stdout.write(`[✓${s.name.substring(0, 8)}] `);
      } else {
        process.stdout.write(`[${s.progress || 0}%] `);
      }
    });
    
    allFinished = statuses.every(s => s.finished);
    
    if (allFinished) {
      console.log('\n\n所有回测已完成！');
      return statuses.filter(s => s.finished);
    }
    
    await new Promise(resolve => setTimeout(resolve, 4000));
  }
  
  console.log('\n\n等待超时，部分回测可能未完成');
  return [];
}

function printAnalysis(results) {
  console.log('\n' + '='.repeat(100));
  console.log('回测结果汇总');
  console.log('='.repeat(100));
  
  // 按年化收益排序
  results.sort((a, b) => b.summary.annualReturn - a.summary.annualReturn);
  
  console.log('\n| 策略 | 年化收益 | 累计收益 | 夏普 | 最大回撤 | 胜率 | 交易次数 |');
  console.log('|------|----------|----------|------|----------|------|----------|');
  
  results.forEach(r => {
    const annual = (r.summary.annualReturn * 100).toFixed(2);
    const total = (r.summary.totalReturn * 100).toFixed(2);
    const sharpe = r.summary.sharpe.toFixed(3);
    const maxDD = (r.summary.maxDrawdown * 100).toFixed(2);
    const winRate = (r.summary.winRate * 100).toFixed(1);
    const trades = r.summary.tradeCount;
    
    console.log(`| ${r.name.substring(0, 20).padEnd(20)} | ${annual.padStart(8)}% | ${total.padStart(8)}% | ${sharpe.padStart(6)} | ${maxDD.padStart(8)}% | ${winRate.padStart(5)}% | ${String(trades).padStart(8)} |`);
  });
  
  console.log('\n' + '='.repeat(100));
  console.log('归因分析');
  console.log('='.repeat(100));
  
  // 查找基准（假设年化收益中等的为基准参考）
  const pureRFScore = results.find(r => r.name.includes('C_Pure'));
  const noRiskControl = results.find(r => r.name.includes('D_No_Risk'));
  const pb20Loose = results.find(r => r.name.includes('E_PB20'));
  
  if (pureRFScore && noRiskControl && pb20Loose) {
    console.log('\n【核心发现】');
    
    // 分析1: RFScore单独贡献
    console.log('\n1. RFScore7质量因子单独表现:');
    console.log(`   - 年化收益: ${(pureRFScore.summary.annualReturn * 100).toFixed(2)}%`);
    console.log(`   - 最大回撤: ${(pureRFScore.summary.maxDrawdown * 100).toFixed(2)}%`);
    console.log(`   - 夏普比率: ${pureRFScore.summary.sharpe.toFixed(3)}`);
    
    // 分析2: 风控贡献
    const riskControlImpact = noRiskControl.summary.annualReturn - pureRFScore.summary.annualReturn;
    console.log('\n2. 动态风控影响:');
    console.log(`   - 无风控版本年化: ${(noRiskControl.summary.annualReturn * 100).toFixed(2)}%`);
    console.log(`   - 差异: ${riskControlImpact > 0 ? '+' : ''}${(riskControlImpact * 100).toFixed(2)}%`);
    if (Math.abs(riskControlImpact) < 0.02) {
      console.log('   → 风控对收益影响较小');
    } else if (riskControlImpact > 0) {
      console.log('   → 风控提升了收益（可能避开了下跌）');
    } else {
      console.log('   → 风控降低了收益（可能过早减仓）');
    }
    
    // 分析3: PB严格度
    const pbImpact = pb20Loose.summary.annualReturn - pureRFScore.summary.annualReturn;
    console.log('\n3. PB严格度影响:');
    console.log(`   - PB20%宽松版年化: ${(pb20Loose.summary.annualReturn * 100).toFixed(2)}%`);
    console.log(`   - 与纯RFScore差异: ${pbImpact > 0 ? '+' : ''}${(pbImpact * 100).toFixed(2)}%`);
    if (pbImpact > 0.02) {
      console.log('   → PB20%表现更好，PB10%可能过拟合');
    } else if (pbImpact < -0.02) {
      console.log('   → PB10%严格筛选有效');
    } else {
      console.log('   → PB严格度对收益影响不大');
    }
    
    // 综合结论
    console.log('\n' + '='.repeat(100));
    console.log('综合结论');
    console.log('='.repeat(100));
    
    const bestStrategy = results[0];
    console.log(`\n✓ 表现最佳: ${bestStrategy.name}`);
    console.log(`  年化收益: ${(bestStrategy.summary.annualReturn * 100).toFixed(2)}%`);
    console.log(`  风险收益比: ${bestStrategy.summary.sharpe.toFixed(3)}`);
    
    console.log('\n建议:');
    if (pureRFScore.summary.sharpe > 0.5) {
      console.log('  • RFScore7质量因子是核心收益来源');
    }
    if (Math.abs(riskControlImpact) < 0.02) {
      console.log('  • 动态风控参数可能需要优化');
    }
    if (pb20Loose.summary.annualReturn > pureRFScore.summary.annualReturn) {
      console.log('  • 考虑使用PB20%代替PB10%以增加候选股');
    }
  }
}

async function main() {
  console.log('='.repeat(100));
  console.log('监控回测完成并分析结果');
  console.log('='.repeat(100));
  
  console.log('\n监控的回测:');
  BACKTESTS.forEach((bt, i) => {
    console.log(`  ${i + 1}. ${bt.name}`);
    console.log(`     ID: ${bt.backtestId}`);
  });
  
  console.log('\n检查登录状态...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  
  const client = new JoinQuantStrategyClient();
  
  // 等待所有回测完成
  const results = await waitForAllBacktests(client);
  
  if (results.length > 0) {
    // 打印详细分析
    printAnalysis(results);
    
    // 保存结果
    const outputPath = path.join(__dirname, 'output', `analysis-${Date.now()}.json`);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    console.log(`\n详细结果已保存: ${outputPath}`);
  } else {
    console.log('\n未能获取完整结果，请稍后手动查询');
  }
}

main().catch(err => {
  console.error('监控失败:', err);
  process.exit(1);
});
