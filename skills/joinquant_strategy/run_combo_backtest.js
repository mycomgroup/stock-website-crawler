#!/usr/bin/env node
/**
 * 运行 RFScore + 红利小盘 组合策略回测
 * 使用已有的策略ID,更新代码并运行回测
 */

import { runStrategyWorkflow } from './request/strategy-runner.js';

const COMBO_STRATEGY = {
  id: 'fd941eee6ddb80f86fe8ce9fa9349073', // 使用已有策略ID
  file: '../../strategies/combo_rfscore_dividend_60_40.py',
  name: 'RFScore + 红利小盘 60/40 组合',
  backtest: {
    start: '2020-01-01',
    end: '2025-12-31',
    capital: '1000000', // 100万
    frequency: 'day'
  }
};

console.log('========================================');
console.log('RFScore + 红利小盘 组合策略回测');
console.log('========================================');
console.log(`策略名称: ${COMBO_STRATEGY.name}`);
console.log(`策略ID: ${COMBO_STRATEGY.id}`);
console.log(`回测区间: ${COMBO_STRATEGY.backtest.start} ~ ${COMBO_STRATEGY.backtest.end}`);
console.log(`初始资金: ${COMBO_STRATEGY.backtest.capital}`);
console.log('========================================\n');

runStrategyWorkflow({
  algorithmId: COMBO_STRATEGY.id,
  codeFilePath: COMBO_STRATEGY.file,
  startTime: COMBO_STRATEGY.backtest.start,
  endTime: COMBO_STRATEGY.backtest.end,
  baseCapital: COMBO_STRATEGY.backtest.capital,
  frequency: COMBO_STRATEGY.backtest.frequency
}).then(result => {
  console.log('\n========================================');
  console.log('✅ 回测完成!');
  console.log('========================================');
  console.log('Backtest ID:', result.backtestId);
  console.log('结果文件:', result.resultPath);
  console.log('\n关键指标:');
  console.log('年化收益:', result.summary?.annual_returns || 'N/A');
  console.log('最大回撤:', result.summary?.max_drawdown || 'N/A');
  console.log('夏普比率:', result.summary?.sharpe || 'N/A');
  console.log('========================================');
}).catch(err => {
  console.error('\n========================================');
  console.error('❌ 回测失败');
  console.error('========================================');
  console.error('错误信息:', err.message);
  console.error('\n可能的原因:');
  console.error('1. Session过期,需要重新抓取');
  console.error('2. 策略代码有语法错误');
  console.error('3. API调用超时');
  console.error('\n建议操作:');
  console.error('node browser/capture-joinquant-session.js --headed');
  console.error('========================================');
  process.exit(1);
});