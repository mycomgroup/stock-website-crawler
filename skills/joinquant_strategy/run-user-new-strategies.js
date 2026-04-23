#!/usr/bin/env node
/**
 * 运行用户新建策略的回测
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 用户新建的策略列表
const USER_STRATEGIES = [
  {
    name: 'User_Attr_C_Pure_RFScore',
    algorithmId: 'dacacfad48acfd35c72a4a0f6517c519',
    desc: '纯RFScore7质量因子（剥离PB过滤）',
    purpose: '验证RFScore7单独贡献'
  },
  {
    name: 'User_Attr_D_No_Risk_Control',
    algorithmId: '5c9e4225112d5504433a6231dea8e0a3',
    desc: '无动态风控（始终满仓20只）',
    purpose: '验证动态风控贡献'
  },
  {
    name: 'User_Attr_E_PB20_Loose',
    algorithmId: '50a2ce8b72bc5046cd4b9495379935a6',
    desc: 'PB20%宽松版（vs PB10%严格版）',
    purpose: '验证PB严格度是否过拟合'
  }
];

const BACKTEST_CONFIG = {
  startTime: '2020-01-01',
  endTime: '2025-12-31',
  baseCapital: '1000000',
  frequency: 'day'
};

async function runSingleBacktest(client, strategy, index) {
  console.log(`\n=== [${index + 1}/${USER_STRATEGIES.length}] ${strategy.name} ===`);
  console.log(`描述: ${strategy.desc}`);
  console.log(`目的: ${strategy.purpose}`);
  console.log(`策略ID: ${strategy.algorithmId}`);

  // 获取策略上下文
  const context = await client.getStrategyContext(strategy.algorithmId);
  console.log(`策略名称: ${context.name}`);

  // 读取策略代码
  const codeFile = path.join(__dirname, strategy.name.replace('User_Attr_', 'attribution_').toLowerCase() + '.py');
  let code;
  
  // 尝试找到对应的代码文件
  const possibleFiles = [
    path.join(__dirname, 'attribution_c_pure_rfscore.py'),
    path.join(__dirname, 'attribution_d_no_risk_control.py'),
    path.join(__dirname, 'attribution_e_pb20_loose.py')
  ];
  
  if (index === 0) code = fs.readFileSync(possibleFiles[0], 'utf8');
  else if (index === 1) code = fs.readFileSync(possibleFiles[1], 'utf8');
  else code = fs.readFileSync(possibleFiles[2], 'utf8');

  // 启动回测
  console.log(`\n启动回测: ${BACKTEST_CONFIG.startTime} ~ ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(strategy.algorithmId, code, BACKTEST_CONFIG, context);

  const backtestId = buildResult.backtestId;
  console.log(`回测ID: ${backtestId}`);
  console.log(`回测链接: https://www.joinquant.com/algorithm/backtest?backtestId=${backtestId}`);

  // 等待回测完成
  console.log('等待回测完成...');
  let attempts = 0;
  const maxAttempts = 90;

  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 4000));
    attempts++;

    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};

      process.stdout.write(`[${attempts}/${maxAttempts}] 状态: ${bt.status}, 进度: ${bt.progress || 0}%\r`);

      if (result.status === 'error') {
        console.log('\n✗ 回测失败:', result.message);
        return { 
          success: false, 
          error: result.message, 
          backtestId, 
          name: strategy.name,
          desc: strategy.desc 
        };
      }

      if (bt.finished_time || bt.status === 'finished') {
        console.log('\n✓ 回测完成!');

        const summary = result.data?.result?.summary || {};

        return {
          success: true,
          backtestId,
          name: strategy.name,
          desc: strategy.desc,
          purpose: strategy.purpose,
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
        console.log('\n✗ 回测服务器失败');
        return { 
          success: false, 
          error: 'Server failed', 
          backtestId, 
          name: strategy.name,
          desc: strategy.desc 
        };
      }
    } catch (err) {
      console.log('\n查询结果错误:', err.message);
    }
  }

  console.log('\n等待超时');
  return { 
    success: false, 
    error: 'Timeout', 
    backtestId, 
    name: strategy.name,
    desc: strategy.desc 
  };
}

async function main() {
  console.log('='.repeat(70));
  console.log('用户新建策略 - 批量回测');
  console.log('='.repeat(70));
  console.log('\n回测策略:');
  USER_STRATEGIES.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.name}`);
    console.log(`     ID: ${s.algorithmId}`);
    console.log(`     描述: ${s.desc}`);
    console.log(`     目的: ${s.purpose}`);
  });

  // 确保聚宽Session有效
  console.log('\n检查聚宽登录状态...');
  await ensureJoinQuantSession({ headed: false, headless: true });

  // 创建客户端
  const client = new JoinQuantStrategyClient();

  // 运行所有回测
  const results = [];

  for (let i = 0; i < USER_STRATEGIES.length; i++) {
    const result = await runSingleBacktest(client, USER_STRATEGIES[i], i);
    results.push(result);

    if (result.success) {
      console.log(`\n✓ ${result.name} 完成`);
      console.log(`  累计收益: ${(result.summary.totalReturn * 100).toFixed(2)}%`);
      console.log(`  年化收益: ${(result.summary.annualReturn * 100).toFixed(2)}%`);
      console.log(`  夏普比率: ${result.summary.sharpe.toFixed(3)}`);
      console.log(`  最大回撤: ${(result.summary.maxDrawdown * 100).toFixed(2)}%`);
      console.log(`  交易次数: ${result.summary.tradeCount}`);
    } else {
      console.log(`\n✗ ${result.name} 失败: ${result.error}`);
    }

    // 间隔3秒再提交下一个
    if (i < USER_STRATEGIES.length - 1) {
      console.log('\n等待3秒后提交下一个...');
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
  }

  // 汇总结果
  console.log('\n\n' + '='.repeat(70));
  console.log('回测结果汇总');
  console.log('='.repeat(70));

  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);

  console.log(`\n成功: ${successful.length}/${results.length}`);
  console.log(`失败: ${failed.length}/${results.length}`);

  if (successful.length > 0) {
    console.log('\n对比表格:');
    console.log('-'.repeat(100));
    console.log('名称                    | 累计收益 | 年化收益 | 夏普 | 最大回撤 | 交易次数 | 验证目的');
    console.log('-'.repeat(100));

    // 按年化收益排序
    successful.sort((a, b) => (b.summary.annualReturn || 0) - (a.summary.annualReturn || 0));

    for (const s of successful) {
      const name = s.name.padEnd(24);
      const totalRet = (s.summary.totalReturn * 100).toFixed(2).padStart(8);
      const annualRet = (s.summary.annualReturn * 100).toFixed(2).padStart(8);
      const sharpe = s.summary.sharpe.toFixed(3).padStart(6);
      const maxDD = (s.summary.maxDrawdown * 100).toFixed(2).padStart(8);
      const trades = String(s.summary.tradeCount).padStart(8);
      const purpose = s.purpose.substring(0, 20);
      console.log(`${name}| ${totalRet}% | ${annualRet}% | ${sharpe} | ${maxDD}% | ${trades} | ${purpose}`);
    }

    console.log('-'.repeat(100));
  }

  // 保存结果到文件
  const outputPath = path.join(__dirname, 'output', `user-new-strategies-${Date.now()}.json`);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`\n结果已保存: ${outputPath}`);

  // 打印对比分析
  console.log('\n' + '='.repeat(70));
  console.log('归因分析指南');
  console.log('='.repeat(70));
  console.log('\n请结合基准策略对比:');
  console.log('  1. v1_rfscore7_offensive.py (原始基准)');
  console.log('  2. rfscore7_pb10_final_v2.py (PB10%严格版)');
  console.log('\n分析维度:');
  console.log('  - 纯RFScore vs 基准: RFScore7单独贡献');
  console.log('  - 无风控 vs 有风控: 动态风控贡献');
  console.log('  - PB20% vs PB10%: PB严格度影响');
}

main().catch(err => {
  console.error('批量回测失败:', err);
  process.exit(1);
});
