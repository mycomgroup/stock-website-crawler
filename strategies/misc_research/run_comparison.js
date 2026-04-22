#!/usr/bin/env node
/**
 * 运行策略对比 - 原始策略 vs 增强策略
 * 
 * 参数：
 * - 原始策略：rfscore7_pb10_final.py
 * - 增强策略：rfscore7_pb10_enhanced_standalone.py
 * - 回测时间：2021-01-01 至 2025-03-28
 * - 初始资金：100000
 */

import { runStrategyWorkflow } from '../skills/joinquant_strategy/request/strategy-runner.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 使用已有的策略 ID（会被覆盖）
const STRATEGY_ID = 'cdd3824af440103aa29fa3a06f60815d'; // 这是一个简单的策略-195

const BASE_DIR = path.resolve(__dirname, '..');
const ORIGINAL_STRATEGY = path.join(BASE_DIR, 'strategies/rfscore7_pb10_final.py');
const ENHANCED_STRATEGY = path.join(BASE_DIR, 'strategies/enhanced/rfscore7_pb10_enhanced_standalone.py');

const BACKTEST_CONFIG = {
  startTime: '2021-01-01',
  endTime: '2025-03-27',  // 回测结束日期需要在过去
  baseCapital: '100000',
  frequency: 'day'
};

async function runBacktest(strategyFile, strategyName) {
  console.log(`\n${'='.repeat(70)}`);
  console.log(`运行策略: ${strategyName}`);
  console.log(`文件: ${strategyFile}`);
  console.log(`${'='.repeat(70)}\n`);

  if (!fs.existsSync(strategyFile)) {
    throw new Error(`策略文件不存在: ${strategyFile}`);
  }

  const result = await runStrategyWorkflow({
    algorithmId: STRATEGY_ID,
    codeFilePath: strategyFile,
    ...BACKTEST_CONFIG
  });

  return result;
}

async function main() {
  try {
    // 1. 运行原始策略
    console.log('开始运行原始策略...');
    const originalResult = await runBacktest(ORIGINAL_STRATEGY, '原始策略 (RFScore PB10)');
    
    console.log('\n原始策略回测完成！');
    console.log(`Backtest ID: ${originalResult.backtestId}`);
    console.log(`结果文件: ${originalResult.resultPath}`);

    // 保存原始策略结果
    const originalResultFile = path.join(BASE_DIR, 'strategies/enhanced', 'original_backtest_result.json');
    fs.writeFileSync(originalResultFile, JSON.stringify(originalResult, null, 2));
    console.log(`原始策略结果已保存: ${originalResultFile}`);

    // 等待 10 秒，避免连续请求
    console.log('\n等待 10 秒后运行增强策略...');
    await new Promise(resolve => setTimeout(resolve, 10000));

    // 2. 运行增强策略
    console.log('开始运行增强策略...');
    const enhancedResult = await runBacktest(ENHANCED_STRATEGY, '增强策略 (RFScore PB10 Enhanced)');
    
    console.log('\n增强策略回测完成！');
    console.log(`Backtest ID: ${enhancedResult.backtestId}`);
    console.log(`结果文件: ${enhancedResult.resultPath}`);

    // 保存增强策略结果
    const enhancedResultFile = path.join(BASE_DIR, 'strategies/enhanced', 'enhanced_backtest_result.json');
    fs.writeFileSync(enhancedResultFile, JSON.stringify(enhancedResult, null, 2));
    console.log(`增强策略结果已保存: ${enhancedResultFile}`);

    // 3. 对比结果
    console.log('\n' + '='.repeat(70));
    console.log('策略对比结果');
    console.log('='.repeat(70));

    compareResults(originalResult.summary, enhancedResult.summary);

    // 4. 更新 backtest_comparison.py
    console.log('\n更新 backtest_comparison.py...');
    updateComparisonFile(originalResult.summary, enhancedResult.summary);

    console.log('\n完成！');

  } catch (error) {
    console.error('运行失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

function compareResults(original, enhanced) {
  const metrics = [
    ['总收益', 'totalReturn', '%'],
    ['年化收益', 'annualReturn', '%'],
    ['最大回撤', 'maxDrawdown', '%'],
    ['夏普比率', 'sharpe', ''],
    ['胜率', 'winRate', '%'],
    ['交易次数', 'tradeCount', '']
  ];

  console.log('\n指标对比:');
  console.log('-'.repeat(70));
  console.log(`${'指标'.padEnd(15)} | ${'原始策略'.padEnd(15)} | ${'增强策略'.padEnd(15)} | ${'差异'.padEnd(15)}`);
  console.log('-'.repeat(70));

  for (const [name, key, unit] of metrics) {
    const origValue = original[key] || 0;
    const enhValue = enhanced[key] || 0;
    const diff = enhValue - origValue;

    console.log(
      `${name.padEnd(15)} | ` +
      `${(typeof origValue === 'number' ? origValue.toFixed(2) : origValue).toString().padEnd(15)}${unit} | ` +
      `${(typeof enhValue === 'number' ? enhValue.toFixed(2) : enhValue).toString().padEnd(15)}${unit} | ` +
      `${(typeof diff === 'number' ? diff.toFixed(2) : diff).toString().padEnd(15)}${unit}`
    );
  }
}

function updateComparisonFile(originalSummary, enhancedSummary) {
  const comparisonFile = path.join(BASE_DIR, 'strategies/enhanced/backtest_comparison.py');
  
  const now = new Date().toISOString().split('T')[0];
  
  const updatedContent = `"""
回测对比脚本 - 原始策略 vs 增强策略

实际回测结果（运行日期: ${now}）

回测参数：
- 时间范围：2021-01-01 至 2025-03-28
- 初始资金：100000
- 频率：日线
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime


class BacktestResult:
    def __init__(self, name, data):
        self.name = name
        self.total_return = data.get("totalReturn", 0)
        self.annual_return = data.get("annualReturn", 0)
        self.max_drawdown = data.get("maxDrawdown", 0)
        self.sharpe = data.get("sharpe", 0)
        self.calmar = data.get("calmar", 0)
        self.win_rate = data.get("winRate", 0)
        self.trade_count = data.get("tradeCount", 0)
        self.alpha = data.get("alpha", 0)
        self.beta = data.get("beta", 0)

    def to_dict(self):
        return {
            "策略名称": self.name,
            "总收益": f"{self.total_return:.2f}%",
            "年化收益": f"{self.annual_return:.2f}%",
            "最大回撤": f"{self.max_drawdown:.2f}%",
            "夏普比率": f"{self.sharpe:.2f}",
            "胜率": f"{self.win_rate:.1f}%",
            "交易次数": self.trade_count,
            "Alpha": f"{self.alpha:.2f}",
            "Beta": f"{self.beta:.2f}",
        }


# 实际回测结果
ACTUAL_RESULTS = {
    "original": {
        "totalReturn": ${originalSummary.totalReturn || 0},
        "annualReturn": ${originalSummary.annualReturn || 0},
        "maxDrawdown": ${originalSummary.maxDrawdown || 0},
        "sharpe": ${originalSummary.sharpe || 0},
        "calmar": ${originalSummary.calmar || 0},
        "winRate": ${originalSummary.winRate || 0},
        "tradeCount": ${originalSummary.tradeCount || 0},
        "alpha": ${originalSummary.alpha || 0},
        "beta": ${originalSummary.beta || 0},
    },
    "enhanced": {
        "totalReturn": ${enhancedSummary.totalReturn || 0},
        "annualReturn": ${enhancedSummary.annualReturn || 0},
        "maxDrawdown": ${enhancedSummary.maxDrawdown || 0},
        "sharpe": ${enhancedSummary.sharpe || 0},
        "calmar": ${enhancedSummary.calmar || 0},
        "winRate": ${enhancedSummary.winRate || 0},
        "tradeCount": ${enhancedSummary.tradeCount || 0},
        "alpha": ${enhancedSummary.alpha || 0},
        "beta": ${enhancedSummary.beta || 0},
    },
}


def main():
    print("=" * 70)
    print("原始策略 vs 增强策略（实际回测数据）")
    print("时间范围：2021-01-01 至 2025-03-28")
    print("=" * 70)

    original = BacktestResult("原始策略 (RFScore PB10)", ACTUAL_RESULTS["original"])
    enhanced = BacktestResult("增强策略 (RFScore PB10 Enhanced)", ACTUAL_RESULTS["enhanced"])

    results = [original.to_dict(), enhanced.to_dict()]
    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # 对比分析
    print("\n" + "=" * 70)
    print("对比分析")
    print("=" * 70)

    print(f"\n收益提升: {enhanced.total_return - original.total_return:.2f}%")
    print(f"年化收益提升: {enhanced.annual_return - original.annual_return:.2f}%")
    print(f"回撤改善: {original.max_drawdown - enhanced.max_drawdown:.2f}%")
    print(f"夏普提升: {enhanced.sharpe - original.sharpe:.2f}")

    if enhanced.annual_return > original.annual_return and enhanced.max_drawdown < original.max_drawdown:
        print("\n结论: 增强策略优于原始策略 ✓")
    elif enhanced.sharpe > original.sharpe:
        print("\n结论: 增强策略夏普比率更高，风险调整后收益更好 ✓")
    else:
        print("\n结论: 增强策略需要进一步优化")

    print("\n" + "=" * 70)
    print("增强策略特性")
    print("=" * 70)

    print("""
    1. 情绪开关（SentimentSwitch）
       - 涨停数 >= 15 + 连板 >= 2 才开仓
       - 情绪状态分5档，影响仓位比例

    2. 四档仓位（FourTierPosition）
       - 15只（正常） -> 12只（防守） -> 10只（底部） -> 0只（极端）
       - 基于 breadth（广度）和 trend（趋势）

    3. 风控模块（RiskControl）
       - 时间止损：10:30 检查，亏损则卖出
       - 跳空止损：跌破成本 4%
       - 周亏损 > 8% -> 强制休息 3 天
       - 月亏损 > 15% -> 强制休息 5 天
    """)


if __name__ == "__main__":
    main()
`;

  fs.writeFileSync(comparisonFile, updatedContent);
  console.log(`已更新: ${comparisonFile}`);
}

main();