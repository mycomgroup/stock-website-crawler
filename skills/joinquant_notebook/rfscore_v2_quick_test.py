#!/usr/bin/env python3
"""
RFScore v2.0 快速验证测试 - Notebook格式
测试2024年1-6月的选股和调仓逻辑
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress

print("=" * 80)
print("RFScore v2.0 快速验证测试")
print("测试区间: 2024-01 至 2024-06")
print("=" * 80)

# ============================================================================
# RFScore因子定义
# ============================================================================


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

        def sign(ser):
            return ser.apply(lambda x: np.where(x > 0, 1, 0))

        # 确保所有指标都是DataFrame格式
        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
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


# ============================================================================
# 辅助函数
# ============================================================================


def get_universe(watch_date):
    """获取基础股票池"""
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    cutoff_date = (pd.Timestamp(watch_date) - pd.Timedelta(days=180)).date()
    sec = sec[sec["start_date"].apply(lambda x: x <= cutoff_date)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_rfscore_table(stocks, watch_date):
    """计算RFScore表"""
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(
        stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    return df


def calculate_breadth(watch_date):
    """计算市场宽度"""
    try:
        hs300 = get_index_stocks("000300.XSHG", date=watch_date)
        prices = get_price(
            hs300, end_date=watch_date, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        breadth = float((close.iloc[-1] > close.mean()).mean())
        return breadth
    except:
        return 0.5


def get_state(breadth):
    """根据宽度判断状态"""
    if breadth < 0.15:
        return "极弱停手", 0, 0.0
    elif breadth < 0.25:
        return "底部防守", 10, 0.5
    elif breadth < 0.35:
        return "震荡平衡", 15, 0.75
    elif breadth >= 0.40:
        return "强趋势", 20, 1.0
    else:
        return "趋势正常", 15, 0.75


# ============================================================================
# 主测试流程
# ============================================================================

print("\n【测试1】获取股票池")
print("-" * 60)

test_date = "2024-01-02"
try:
    stocks = get_universe(test_date)
    print(f"  测试日期: {test_date}")
    print(f"  股票池数量: {len(stocks)}")
    print(f"  前5只: {stocks[:5]}")
except Exception as e:
    print(f"  错误: {e}")
    import traceback

    traceback.print_exc()

print("\n【测试2】计算RFScore因子")
print("-" * 60)

try:
    test_stocks = stocks[:100]  # 只测试前100只
    factor_df = calc_rfscore_table(test_stocks, test_date)

    print(f"  计算股票数: {len(test_stocks)}")
    print(f"  有效因子数: {len(factor_df)}")

    if len(factor_df) > 0:
        # 显示RFScore分布
        score_dist = factor_df["RFScore"].value_counts().sort_index(ascending=False)
        print(f"\n  RFScore分布:")
        for score, count in score_dist.items():
            bar = "█" * count
            print(f"    {score}分: {count}只 {bar}")

        # 显示前10只
        top10 = factor_df.sort_values("RFScore", ascending=False).head(10)
        print(f"\n  Top 10 候选股:")
        for code, row in top10.iterrows():
            print(
                f"    {code}: RFScore={row['RFScore']}, PB={row['pb_ratio']:.2f}, pb_group={row['pb_group']}"
            )
except Exception as e:
    print(f"  错误: {e}")
    import traceback

    traceback.print_exc()

print("\n【测试3】市场宽度计算")
print("-" * 60)

test_dates = [
    "2024-01-02",
    "2024-02-01",
    "2024-03-01",
    "2024-04-01",
    "2024-05-06",
    "2024-06-03",
]

print(
    f"\n  {'日期':<15} {'市场宽度':>10} {'状态':>15} {'建议持仓':>10} {'仓位比例':>10}"
)
print(f"  {'-' * 15} {'-' * 10} {'-' * 15} {'-' * 10} {'-' * 10}")

for date in test_dates:
    try:
        breadth = calculate_breadth(date)
        state, hold_num, ratio = get_state(breadth)
        print(f"  {date:<15} {breadth:>9.1%} {state:>15} {hold_num:>8}只 {ratio:>9.0%}")
    except Exception as e:
        print(f"  {date:<15} {'错误':>10}")

print("\n【测试4】完整调仓流程模拟")
print("-" * 60)

for date in test_dates:
    try:
        breadth = calculate_breadth(date)
        state, hold_num, ratio = get_state(breadth)

        stocks = get_universe(date)
        factor_df = calc_rfscore_table(stocks[:500], date)  # 限制500只加速

        # 选股
        primary = factor_df[
            (factor_df["RFScore"] == 7) & (factor_df["pb_group"] <= 1)
        ].copy()
        primary = primary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = primary.index.tolist()

        if len(picks) < hold_num:
            secondary = factor_df[
                (factor_df["RFScore"] >= 6) & (factor_df["pb_group"] <= 2)
            ].copy()
            secondary = secondary.sort_values(
                ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                ascending=[False, False, False, False, False, True],
            )
            for code in secondary.index.tolist():
                if code not in picks:
                    picks.append(code)
                if len(picks) >= hold_num:
                    break

        print(f"\n  {date} - {state}")
        print(f"    市场宽度: {breadth:.1%}")
        print(f"    建议持仓: {hold_num}只 (仓位{ratio:.0%})")
        print(f"    实际选出: {len(picks)}只")
        if picks:
            print(f"    前3只: {picks[:3]}")
    except Exception as e:
        print(f"\n  {date} - 错误: {e}")

print("\n" + "=" * 80)
print("测试完成!")
print("=" * 80)
