#!/usr/bin/env node
import fs from 'node:fs';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/exit_rules_comparison.py';
const STRATEGY_NAME = 'exit_rules_comparison_05v2';

const BACKTEST_CONFIG = {
  startTime: '2022-01-01',
  endTime: '2024-12-31',
  baseCapital: '100000',
  frequency: 'day'
};

async function findOrCreateStrategy(client, strategyName) {
  console.log('正在查找可用策略...');
  const strategies = await client.listStrategies();
  
  if (strategies.length === 0) {
    throw new Error('没有找到任何策略，请先在JoinQuant创建一个策略');
  }
  
  console.log(`找到 ${strategies.length} 个策略：`);
  strategies.forEach((s, i) => console.log(`  ${i + 1}. ${s.name} (${s.id})`));
  
  // 查找同名策略
  const existingStrategy = strategies.find(s => s.name === strategyName);
  if (existingStrategy) {
    console.log(`\n找到现有策略: ${strategyName} (${existingStrategy.id})`);
    return existingStrategy.id;
  }
  
  // 使用第一个策略作为基础
  const baseStrategy = strategies[0];
  console.log(`\n使用第一个策略作为基础: ${baseStrategy.name} (${baseStrategy.id})`);
  return baseStrategy.id;
}

async function runBacktest(client, algorithmId, code, context) {
  console.log('\n=== 保存策略代码 ===');
  await client.saveStrategy(algorithmId, STRATEGY_NAME, code, context);
  console.log('策略代码已保存');
  
  console.log('\n=== 启动回测 ===');
  console.log(`时间段: ${BACKTEST_CONFIG.startTime} 至 ${BACKTEST_CONFIG.endTime}`);
  const buildResult = await client.runBacktest(algorithmId, code, BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log(`回测已启动, ID: ${backtestId}`);
  
  console.log('\n=== 等待回测完成 ===');
  let attempts = 0;
  const maxAttempts = 60;
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;
    
    try {
      const result = await client.getBacktestResult(backtestId, context);
      const bt = result.data?.result?.backtest || {};
      
      process.stdout.write(`\r[${attempts}/${maxAttempts}] 状态: ${bt.status || 'unknown'}, 进度: ${bt.progress || 0}%`);
      
      if (result.status === 'error') {
        console.log('\n回测失败:', result.message);
        return { success: false, error: result.message, backtestId };
      }
      
      if (bt.finished_time || bt.status === 'finished') {
        console.log('\n\n回测完成！');
        return { success: true, backtestId, result };
      }
      
      if (bt.status === 'failed') {
        console.log('\n回测在服务器端失败');
        return { success: false, error: 'Server failed', backtestId };
      }
    } catch (err) {
      console.log('\n轮询结果时出错:', err.message);
    }
  }
  
  console.log('\n等待回测超时');
  return { success: false, error: 'Timeout', backtestId };
}

async function printResults(client, backtestId) {
  console.log('\n=== 获取回测结果 ===');
  
  const stats = await client.getBacktestStats(backtestId);
  const summary = stats.data || {};
  
  console.log('\n=== 回测统计结果 ===');
  console.log(`总收益率: ${(summary.total_returns || 0).toFixed(2)}%`);
  console.log(`年化收益率: ${(summary.annual_returns || 0).toFixed(2)}%`);
  console.log(`夏普比率: ${(summary.sharpe || 0).toFixed(2)}`);
  console.log(`最大回撤: ${(summary.max_drawdown || 0).toFixed(2)}%`);
  console.log(`胜率: ${(summary.win_rate || 0).toFixed(2)}%`);
  console.log(`交易次数: ${summary.trade_count || 0}`);
  
  const log = await client.getLog(backtestId);
  const logData = log.data || log;
  
  if (logData.records && logData.records.length > 0) {
    console.log('\n=== 策略日志 ===');
    const lastRecords = logData.records.slice(-20);
    lastRecords.forEach(record => {
      console.log(`[${record.time}] ${record.msg}`);
    });
  }
  
  return { summary, log: logData };
}

async function main() {
  console.log('=== JoinQuant 策略回测脚本 ===');
  console.log(`策略文件: ${STRATEGY_FILE}`);
  console.log(`策略名称: ${STRATEGY_NAME}`);
  
  // 1. 确保有有效的session
  console.log('\n=== 检查Session ===');
  const sessionResult = await ensureJoinQuantSession({ headed: true });
  console.log('Session状态:', sessionResult.refreshed ? '已刷新' : '有效');
  
  // 2. 初始化客户端
  const client = new JoinQuantStrategyClient();
  
  // 3. 查找或获取策略ID
  const algorithmId = await findOrCreateStrategy(client, STRATEGY_NAME);
  
  // 4. 获取策略上下文（token等）
  console.log('\n=== 获取策略上下文 ===');
  const context = await client.getStrategyContext(algorithmId);
  console.log('策略名称:', context.name);
  console.log('用户ID:', context.userId);
  
  // 5. 读取策略代码
  const code = fs.readFileSync(STRATEGY_FILE, 'utf8');
  console.log(`代码长度: ${code.length} 字符`);
  
  // 6. 运行回测
  const backtestResult = await runBacktest(client, algorithmId, code, context);
  
  // 7. 打印结果
  if (backtestResult.success) {
    await printResults(client, backtestResult.backtestId);
    console.log('\n✓ 回测成功完成');
  } else {
    console.log('\n✗ 回测失败:', backtestResult.error);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('\n脚本执行失败:', err.message);
  console.error(err.stack);
  process.exit(1);
});
