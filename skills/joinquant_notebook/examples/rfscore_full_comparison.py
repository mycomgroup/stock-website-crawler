#!/usr/bin/env python3
"""
RFScore PB10 策略对比 - Notebook 完整版

使用 get_fundamentals 代替 jqfactor，避免日期类型问题
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 70)
print("RFScore PB10 策略对比 - Notebook 完整版")
print("回测时间：2021-01-01 至 2025-03-28")
print("初始资金：100000")
print("=" * 70)


# 选股函数（简化版）
def select_stocks(date_str, hold_num=20):
    """选股：ROA > 0 + PB 最低 10%"""
    # 股票池
    hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
    zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    # 过滤新股
    sec = get_all_securities(types=["stock"], date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    # 180天前
    from datetime import datetime, timedelta

    threshold = (
        datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=180)
    ).strftime("%Y-%m-%d")
    sec = sec[sec["start_date"].apply(lambda x: str(x) <= threshold)]
    stocks = sec.index.tolist()

    # ST
    is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 停牌
    paused = get_price(stocks, end_date=date_str, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    # 基本面数据
    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )

    df = get_fundamentals(q, date=date_str)
    df = df.dropna()

    # PB 分组
    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # 选股：ROA > 0 + PB 最低 10%
    primary = df[(df["pb_group"] == 1) & (df["roa"] > 0)]
    primary = primary.sort_values("roa", ascending=False)

    picks = primary["code"].head(hold_num).tolist()

    return picks


# 计算市场状态
def calc_market_state(date_str):
    """计算广度和趋势"""
    hs300 = get_index_stocks("000300.XSHG", date=date_str)
    prices = get_price(
        hs300, end_date=date_str, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
    trend_on = float(idx["close"].iloc[-1]) > float(idx["close"].mean())

    return breadth, trend_on


# 计算情绪
def calc_sentiment(date_str):
    """计算情绪"""
    all_stocks = get_all_securities("stock", date=date_str).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    sample = all_stocks[:500]
    df = get_price(
        sample, end_date=date_str, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()

    hl_count = len(df[df["close"] == df["high_limit"]])

    score = 50
    if hl_count > 80:
        score += 20
    elif hl_count > 50:
        score += 10
    elif hl_count < 15:
        score -= 15

    return max(0, min(100, score)), hl_count


# 计算收益
def calc_returns(stocks, start_date, end_date):
    """计算股票池收益"""
    if len(stocks) == 0:
        return 0

    returns = []
    for stock in stocks:
        try:
            p1 = get_price(
                stock, end_date=start_date, count=1, fields=["close"], panel=False
            )
            p2 = get_price(
                stock, end_date=end_date, count=1, fields=["close"], panel=False
            )

            if not p1.empty and not p2.empty:
                ret = (
                    float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])
                ) / float(p1["close"].iloc[-1])
                returns.append(ret)
        except:
            pass

    return np.mean(returns) if returns else 0


# 测试日期（每月第一个交易日）
test_dates = [
    "2021-01-04",
    "2021-02-01",
    "2021-03-01",
    "2021-04-01",
    "2021-05-06",
    "2021-06-01",
    "2021-07-01",
    "2021-08-02",
    "2021-09-01",
    "2021-10-08",
    "2021-11-01",
    "2021-12-01",
    "2022-01-04",
    "2022-02-07",
    "2022-03-01",
    "2022-04-01",
    "2022-05-05",
    "2022-06-01",
    "2022-07-01",
    "2022-08-01",
    "2022-09-01",
    "2022-10-10",
    "2022-11-01",
    "2022-12-01",
    "2023-01-03",
    "2023-02-01",
    "2023-03-01",
    "2023-04-03",
    "2023-05-04",
    "2023-06-01",
    "2023-07-03",
    "2023-08-01",
    "2023-09-01",
    "2023-10-09",
    "2023-11-01",
    "2023-12-01",
    "2024-01-02",
    "2024-02-01",
    "2024-03-01",
    "2024-04-01",
    "2024-05-06",
    "2024-06-03",
    "2024-07-01",
    "2024-08-01",
    "2024-09-02",
    "2024-10-08",
    "2024-11-01",
    "2024-12-02",
    "2025-01-02",
    "2025-02-05",
    "2025-03-03",
]

print(f"\n测试月份数: {len(test_dates)}")

# 原始策略回测
print("\n" + "=" * 70)
print("原始策略回测")
print("=" * 70)

original_returns = []
for i, date in enumerate(test_dates):
    print(f"\n[{i + 1}/{len(test_dates)}] {date}")

    # 选股
    stocks = select_stocks(date, hold_num=20)
    print(f"  选中: {len(stocks)} 只")

    if len(stocks) == 0:
        original_returns.append(0)
        continue

    # 下月收益
    next_dates = get_trade_days(date, "2025-03-28")
    if len(next_dates) < 20:
        original_returns.append(0)
        continue

    next_date = str(next_dates[min(20, len(next_dates) - 1)])
    avg_ret = calc_returns(stocks, date, next_date)
    original_returns.append(avg_ret)
    print(f"  收益: {avg_ret * 100:.2f}%")

# 增强策略回测
print("\n" + "=" * 70)
print("增强策略回测")
print("=" * 70)

enhanced_returns = []
for i, date in enumerate(test_dates):
    print(f"\n[{i + 1}/{len(test_dates)}] {date}")

    # 市场状态
    breadth, trend_on = calc_market_state(date)
    sentiment, hl_count = calc_sentiment(date)

    print(
        f"  广度: {breadth:.2f}, 趋势: {trend_on}, 情绪: {sentiment}, 涨停: {hl_count}"
    )

    # 仓位决策
    if breadth < 0.15 and not trend_on:
        hold_num, position_ratio = 0, 0
        print(f"  决策: 清仓（极端）")
    elif breadth < 0.25 and not trend_on:
        hold_num, position_ratio = 10, 0.5
        print(f"  决策: 减仓（底部）")
    elif sentiment < 30:
        hold_num, position_ratio = 0, 0
        print(f"  决策: 清仓（情绪差）")
    elif sentiment < 45:
        hold_num, position_ratio = 8, 0.3
        print(f"  决策: 减仓（情绪弱）")
    else:
        hold_num, position_ratio = 15, 1.0
        print(f"  决策: 正常")

    if hold_num == 0:
        enhanced_returns.append(0)
        continue

    # 选股
    stocks = select_stocks(date, hold_num=hold_num)
    print(f"  选中: {len(stocks)} 只")

    if len(stocks) == 0:
        enhanced_returns.append(0)
        continue

    # 收益
    next_dates = get_trade_days(date, "2025-03-28")
    if len(next_dates) < 20:
        enhanced_returns.append(0)
        continue

    next_date = str(next_dates[min(20, len(next_dates) - 1)])
    avg_ret = calc_returns(stocks, date, next_date) * position_ratio
    enhanced_returns.append(avg_ret)
    print(f"  收益(调整后): {avg_ret * 100:.2f}%")

# 结果对比
print("\n" + "=" * 70)
print("策略对比结果")
print("=" * 70)

total_orig = np.sum(original_returns) * 100
total_enh = np.sum(enhanced_returns) * 100
avg_orig = np.mean(original_returns) * 100
avg_enh = np.mean(enhanced_returns) * 100

# 夏普比率（简化）
sharpe_orig = (
    np.mean(original_returns) / np.std(original_returns) * np.sqrt(12)
    if np.std(original_returns) > 0
    else 0
)
sharpe_enh = (
    np.mean(enhanced_returns) / np.std(enhanced_returns) * np.sqrt(12)
    if np.std(enhanced_returns) > 0
    else 0
)

# 胜率
win_orig = len([r for r in original_returns if r > 0]) / len(original_returns) * 100
win_enh = len([r for r in enhanced_returns if r > 0]) / len(enhanced_returns) * 100

print(f"\n{'指标':<20} {'原始策略':<20} {'增强策略':<20} {'差异':<15}")
print("-" * 70)
print(
    f"{'累计收益':<20} {total_orig:.2f}%{'':<12} {total_enh:.2f}%{'':<12} {total_enh - total_orig:.2f}%"
)
print(
    f"{'月均收益':<20} {avg_orig:.2f}%{'':<12} {avg_enh:.2f}%{'':<12} {avg_enh - avg_orig:.2f}%"
)
print(
    f"{'夏普比率':<20} {sharpe_orig:.2f}{'':<15} {sharpe_enh:.2f}{'':<15} {sharpe_enh - sharpe_orig:.2f}"
)
print(
    f"{'胜率':<20} {win_orig:.1f}%{'':<13} {win_enh:.1f}%{'':<13} {win_enh - win_orig:.1f}%"
)

# 结论
if total_enh > total_orig and sharpe_enh > sharpe_orig:
    print("\n结论: 增强策略优于原始策略 ✓")
elif total_enh > total_orig:
    print("\n结论: 增强策略收益更高 ✓")
elif sharpe_enh > sharpe_orig:
    print("\n结论: 增强策略风险调整后收益更好 ✓")
else:
    print("\n结论: 策略需要进一步优化")

# 保存结果
result_data = {
    "test_period": "2021-01-01 to 2025-03-28",
    "initial_capital": 100000,
    "test_dates": test_dates,
    "original": {
        "total_return": total_orig,
        "avg_monthly_return": avg_orig,
        "sharpe": sharpe_orig,
        "win_rate": win_orig,
        "monthly_returns": [r * 100 for r in original_returns],
    },
    "enhanced": {
        "total_return": total_enh,
        "avg_monthly_return": avg_enh,
        "sharpe": sharpe_enh,
        "win_rate": win_enh,
        "monthly_returns": [r * 100 for r in enhanced_returns],
    },
    "comparison": {
        "return_diff": total_enh - total_orig,
        "sharpe_diff": sharpe_enh - sharpe_orig,
    },
}

result_file = "/Users/fengzhi/Downloads/git/testlixingren/strategies/enhanced/notebook_comparison_result.json"
with open(result_file, "w") as f:
    json.dump(result_data, f, indent=2)

print(f"\n结果已保存: {result_file}")

print("\n" + "=" * 70)
print("完成!")
print("=" * 70)
