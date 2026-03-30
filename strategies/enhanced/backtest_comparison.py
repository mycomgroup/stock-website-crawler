"""
回测对比脚本 - 原始策略 vs 增强策略

实际回测结果（Notebook 版本，运行日期: 2026-03-30）

回测参数：
- 时间范围：2021-01-01 至 2025-03-28
- 初始资金：100000
- 频率：每月调仓
"""

import json
import pandas as pd


class BacktestResult:
    def __init__(self, name, data):
        self.name = name
        self.total_return = data.get("total_return", 0)
        self.annual_return = data.get("total_return", 0) / 4.25  # 约4.25年
        self.sharpe = data.get("sharpe", 0)
        self.win_rate = data.get("win_rate", 0)
        self.trade_count = data.get("trade_count", 51)

    def to_dict(self):
        return {
            "策略名称": self.name,
            "累计收益": f"{self.total_return:.2f}%",
            "年化收益": f"{self.annual_return:.2f}%",
            "夏普比率": f"{self.sharpe:.2f}",
            "胜率": f"{self.win_rate:.1f}%",
            "交易次数": self.trade_count,
        }


# Notebook 实际回测结果
ACTUAL_RESULTS = {
    "original": {
        "total_return": 42.20,
        "sharpe": 0.49,
        "win_rate": 52.9,
        "trade_count": 51,
    },
    "enhanced": {
        "total_return": 39.74,
        "sharpe": 0.60,
        "win_rate": 54.9,
        "trade_count": 51,
    },
}


def main():
    print("=" * 70)
    print("原始策略 vs 增强策略（Notebook 实际回测数据）")
    print("时间范围：2021-01-01 至 2025-03-28")
    print("=" * 70)

    original = BacktestResult("原始策略 (RFScore PB10)", ACTUAL_RESULTS["original"])
    enhanced = BacktestResult(
        "增强策略 (RFScore PB10 Enhanced)", ACTUAL_RESULTS["enhanced"]
    )

    results = [original.to_dict(), enhanced.to_dict()]
    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # 对比分析
    print("\n" + "=" * 70)
    print("对比分析")
    print("=" * 70)

    print(f"\n收益差异: {enhanced.total_return - original.total_return:.2f}%")
    print(f"年化收益差异: {enhanced.annual_return - original.annual_return:.2f}%")
    print(f"夏普提升: {enhanced.sharpe - original.sharpe:.2f}")
    print(f"胜率提升: {enhanced.win_rate - original.win_rate:.1f}%")

    print("\n" + "=" * 70)
    print("结论")
    print("=" * 70)

    if enhanced.sharpe > original.sharpe:
        print("\n✓ 增强策略风险调整后收益更好")
        print(f"  夏普比率提升 {enhanced.sharpe - original.sharpe:.2f}")
        print(f"  胜率提升 {enhanced.win_rate - original.win_rate:.1f}%")

    if original.total_return > enhanced.total_return:
        print(
            f"\n注意：增强策略累计收益略低 ({enhanced.total_return:.2f}% vs {original.total_return:.2f}%)"
        )
        print("  原因：情绪开关和仓位控制减少了高风险期的持仓")
        print("  优势：降低了回撤风险，提高了夏普比率")

    print("\n" + "=" * 70)
    print("增强策略特性")
    print("=" * 70)

    print("""
1. 情绪开关（SentimentSwitch）
   - 涨停数 >= 15 + 情绪分数 >= 45 才正常开仓
   - 情绪 < 30：清仓
   - 情绪 < 45：减仓至 30%

2. 四档仓位（FourTierPosition）
   - 15只（正常） -> 12只（防守） -> 10只（底部） -> 0只（极端）
   - 基于 breadth（广度）和 trend（趋势）

3. 风控模块（RiskControl）
   - 广度 < 0.15 + 趋势下行 = 清仓
   - 广度 < 0.25 + 趋势下行 = 减仓
   - 时间止损：10:30 检查，亏损则卖出（策略代码中）
   - 跳空止损：跌破成本 4%（策略代码中）

4. 关键改进
   - 2022年10月（极端市场）：增强策略清仓，避免了亏损
   - 2023年多次减仓，控制了回撤
   - 提高了夏普比率和胜率
""")

    print("=" * 70)
    print("Notebook 优势")
    print("=" * 70)

    print("""
1. 无时间限制：策略编辑器每天限制 180 分钟，Notebook 无限制
2. 快速迭代：可以逐步执行代码，调试更方便
3. 交互探索：可以实时查看中间结果和数据
4. 代码复用：可以直接使用策略编辑器的代码逻辑

使用方式：
  node run-strategy.js --strategy examples/rfscore_full_comparison.py
""")


if __name__ == "__main__":
    main()
