#!/usr/bin/env python3
"""
RFScore PB10 策略对比 - Notebook 简化版本

手动回测，模拟关键调仓日期
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("RFScore PB10 策略对比 - Notebook 简化版")
print("回测时间：2021-01-01 至 2025-03-28")
print("初始资金：100000")
print("=" * 70)


# RFScore 因子定义
def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1

        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01

        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)

        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1

        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicators = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


# 选股函数
def select_stocks(date_str, hold_num=20, pb_group=1):
    """选股：RFScore=7 + PB最低10%"""
    print(f"  选股日期: {date_str}, 目标持仓: {hold_num}")

    # 股票池
    hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
    zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    # 过滤
    sec = get_all_securities(types=["stock"], date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    # 确保日期类型一致
    threshold_date = pd.Timestamp(date_str) - pd.Timedelta(days=180)
    sec = sec[sec["start_date"] <= threshold_date]
    stocks = sec.index.tolist()

    # ST
    is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 停牌
    paused = get_price(stocks, end_date=date_str, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    print(f"  可用股票: {len(stocks)}")

    # 计算因子
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date_str, end_date=date_str)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    # PB 分组
    val = get_valuation(stocks, end_date=date_str, fields=["pb_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")
    df = df.join(val, how="left")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # RFScore=7 + PB最低10%
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= pb_group)]
    primary = primary.sort_values(
        ["ROA", "OCFOA", "pb_ratio"], ascending=[False, False, True]
    )

    picks = primary.index.tolist()

    # 补充
    if len(picks) < hold_num:
        secondary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 2)]
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "pb_ratio"], ascending=[False, False, True]
        )
        for s in secondary.index.tolist():
            if s not in picks:
                picks.append(s)
            if len(picks) >= hold_num:
                break

    print(f"  选中股票: {len(picks)}")
    return picks[:hold_num]


# 计算市场状态
def calc_breadth(date_str):
    """计算广度"""
    hs300 = get_index_stocks("000300.XSHG", date=date_str)
    prices = get_price(
        hs300, end_date=date_str, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())
    return breadth


def calc_trend(date_str):
    """计算趋势"""
    idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
    return float(idx["close"].iloc[-1]) > float(idx["close"].mean())


# 计算情绪
def calc_sentiment(date_str):
    """计算情绪指标"""
    all_stocks = get_all_securities("stock", date=date_str).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    sample = all_stocks[:500]
    df = get_price(
        sample,
        end_date=date_str,
        count=1,
        fields=["close", "high_limit", "low_limit"],
        panel=False,
    )
    df = df.dropna()

    hl_count = len(df[df["close"] == df["high_limit"]])
    ll_count = len(df[df["close"] == df["low_limit"]])

    score = 50
    if hl_count > 80:
        score += 20
    elif hl_count > 50:
        score += 10
    elif hl_count < 15:
        score -= 15

    if hl_count / max(ll_count, 1) > 5:
        score += 15

    return max(0, min(100, score))


# 简化回测：只计算几个关键月份的收益
print("\n" + "=" * 70)
print("简化回测：每月调仓")
print("=" * 70)

# 选择几个代表性日期测试
test_dates = [
    "2021-01-04",
    "2021-04-01",
    "2021-07-01",
    "2021-10-08",
    "2022-01-04",
    "2022-04-01",
    "2022-07-01",
    "2022-10-10",
    "2023-01-03",
    "2023-04-03",
    "2023-07-03",
    "2023-10-09",
    "2024-01-02",
    "2024-04-01",
    "2024-07-01",
    "2024-10-08",
    "2025-01-02",
    "2025-03-03",
]

print(f"\n测试日期数: {len(test_dates)}")

# 原始策略：固定持仓数
original_returns = []
for date in test_dates:
    print(f"\n原始策略测试: {date}")

    # 选股
    stocks = select_stocks(date, hold_num=20, pb_group=1)

    if len(stocks) == 0:
        original_returns.append(0)
        continue

    # 计算下个月的收益
    next_month_end = get_trade_days(date, "2025-03-28")
    if len(next_month_end) < 20:
        original_returns.append(0)
        continue

    next_date = next_month_end[min(20, len(next_month_end) - 1)]

    # 计算收益
    returns = []
    for stock in stocks:
        try:
            p1 = get_price(stock, end_date=date, count=1, fields=["close"], panel=False)
            p2 = get_price(
                stock, end_date=next_date, count=1, fields=["close"], panel=False
            )

            if p1.empty or p2.empty:
                continue

            ret = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                p1["close"].iloc[-1]
            )
            returns.append(ret)
        except:
            continue

    if returns:
        avg_return = np.mean(returns)
        original_returns.append(avg_return)
        print(f"  平均收益: {avg_return * 100:.2f}%")
    else:
        original_returns.append(0)

print("\n" + "=" * 70)
print("原始策略结果")
print("=" * 70)

total_return_orig = np.sum(original_returns) * 100
avg_monthly_return_orig = np.mean(original_returns) * 100
print(f"累计收益: {total_return_orig:.2f}%")
print(f"月均收益: {avg_monthly_return_orig:.2f}%")

# 增强策略：情绪+仓位调整
enhanced_returns = []
for date in test_dates:
    print(f"\n增强策略测试: {date}")

    # 计算市场状态
    breadth = calc_breadth(date)
    trend_on = calc_trend(date)
    sentiment_score = calc_sentiment(date)

    print(f"  广度: {breadth:.2f}, 趋势: {trend_on}, 情绪: {sentiment_score}")

    # 决定持仓数
    if breadth < 0.15 and not trend_on:
        hold_num = 0  # 清仓
        position_ratio = 0
    elif breadth < 0.25 and not trend_on:
        hold_num = 10  # 减仓
        position_ratio = 0.5
    elif sentiment_score < 30:
        hold_num = 0
        position_ratio = 0
    elif sentiment_score < 45:
        hold_num = 8
        position_ratio = 0.3
    else:
        hold_num = 15
        position_ratio = 1.0

    print(f"  持仓数: {hold_num}, 仓位比例: {position_ratio}")

    if hold_num == 0:
        enhanced_returns.append(0)
        continue

    # 选股
    stocks = select_stocks(date, hold_num=hold_num, pb_group=1)

    if len(stocks) == 0:
        enhanced_returns.append(0)
        continue

    # 计算收益
    next_month_end = get_trade_days(date, "2025-03-28")
    if len(next_month_end) < 20:
        enhanced_returns.append(0)
        continue

    next_date = next_month_end[min(20, len(next_month_end) - 1)]

    returns = []
    for stock in stocks:
        try:
            p1 = get_price(stock, end_date=date, count=1, fields=["close"], panel=False)
            p2 = get_price(
                stock, end_date=next_date, count=1, fields=["close"], panel=False
            )

            if p1.empty or p2.empty:
                continue

            ret = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                p1["close"].iloc[-1]
            )
            returns.append(ret)
        except:
            continue

    if returns:
        avg_return = np.mean(returns) * position_ratio  # 仓位调整
        enhanced_returns.append(avg_return)
        print(f"  平均收益(调整后): {avg_return * 100:.2f}%")
    else:
        enhanced_returns.append(0)

print("\n" + "=" * 70)
print("增强策略结果")
print("=" * 70)

total_return_enh = np.sum(enhanced_returns) * 100
avg_monthly_return_enh = np.mean(enhanced_returns) * 100
print(f"累计收益: {total_return_enh:.2f}%")
print(f"月均收益: {avg_monthly_return_enh:.2f}%")

# 对比
print("\n" + "=" * 70)
print("策略对比")
print("=" * 70)

print(f"\n{'指标':<20} {'原始策略':<20} {'增强策略':<20} {'差异':<15}")
print("-" * 70)
print(
    f"{'累计收益':<20} {total_return_orig:.2f}%{'':<12} {total_return_enh:.2f}%{'':<12} {total_return_enh - total_return_orig:.2f}%"
)
print(
    f"{'月均收益':<20} {avg_monthly_return_orig:.2f}%{'':<12} {avg_monthly_return_enh:.2f}%{'':<12} {avg_monthly_return_enh - avg_monthly_return_orig:.2f}%"
)

# 更新对比文件
import json

result_data = {
    "test_period": "2021-01-01 to 2025-03-28",
    "initial_capital": 100000,
    "test_dates": test_dates,
    "original": {
        "total_return": total_return_orig,
        "avg_monthly_return": avg_monthly_return_orig,
        "monthly_returns": [r * 100 for r in original_returns],
    },
    "enhanced": {
        "total_return": total_return_enh,
        "avg_monthly_return": avg_monthly_return_enh,
        "monthly_returns": [r * 100 for r in enhanced_returns],
    },
    "comparison": {
        "return_diff": total_return_enh - total_return_orig,
        "monthly_return_diff": avg_monthly_return_enh - avg_monthly_return_orig,
    },
}

result_file = "/Users/fengzhi/Downloads/git/testlixingren/strategies/enhanced/notebook_comparison_result.json"
with open(result_file, "w") as f:
    json.dump(result_data, f, indent=2)

print(f"\n结果已保存: {result_file}")

print("\n" + "=" * 70)
print("完成!")
print("=" * 70)
print("\n注意: 这是简化版本，实际回测需要完整的策略框架。")
print("建议: 使用策略编辑器运行完整回测（注意时间限制）。")
