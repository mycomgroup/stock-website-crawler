#!/usr/bin/env python3
"""
RFScore 六策略快速对比 - Notebook版本
使用简化逻辑，快速获取对比结果
"""

from jqdata import *
import pandas as pd
import numpy as np
import json
from datetime import datetime

print("=" * 70)
print("RFScore 策略对比 - 快速验证")
print("=" * 70)

# 测试日期（季度调仓）
test_dates = [
    "2024-01-02",
    "2024-04-01",
    "2024-07-01",
    "2024-10-08",
    "2025-01-02",
    "2025-04-01",
    "2025-07-01",
    "2025-10-08",
    "2026-01-05",
    "2026-03-02",
]

print(f"\n测试日期: {len(test_dates)} 个调仓点")
print(f"时间范围: {test_dates[0]} 至 {test_dates[-1]}")


def get_universe(date_str):
    """获取股票池"""
    hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
    zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    threshold = pd.Timestamp(date_str) - pd.Timedelta(days=180)
    sec = sec[sec["start_date"].apply(lambda x: pd.Timestamp(x) <= threshold)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(stocks, end_date=date_str, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_market_state(date_str):
    """计算市场状态"""
    hs300 = get_index_stocks("000300.XSHG", date=date_str)
    prices = get_price(
        hs300, end_date=date_str, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
    trend = float(idx["close"].iloc[-1]) > float(idx["close"].mean())

    return breadth, trend


def calc_return(stocks, start_date, end_date):
    """计算收益"""
    if not stocks:
        return 0
    returns = []
    for s in stocks:
        try:
            p1 = get_price(
                s, end_date=start_date, count=1, fields=["close"], panel=False
            )
            p2 = get_price(s, end_date=end_date, count=1, fields=["close"], panel=False)
            if not p1.empty and not p2.empty:
                r = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                    p1["close"].iloc[-1]
                )
                returns.append(r)
        except:
            pass
    return np.mean(returns) if returns else 0


# ========== 策略1: V2原版 ==========
def strategy_v2(date_str, hold_num=20):
    """V2: PB10% + ROA排序"""
    stocks = get_universe(date_str)
    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["roa"] > 0)]
    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    picks = (
        df[df["pb_group"] <= 1]
        .sort_values(["roa", "pb_ratio"], ascending=[False, True])
        .head(hold_num)["code"]
        .tolist()
    )
    return picks


# ========== 策略2: Release V1 ==========
def strategy_release_v1(date_str, hold_num=15):
    """Release V1: PB10% + 行业上限"""
    stocks = get_universe(date_str)
    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["roa"] > 0.5)]
    if df.empty:
        return []
    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    primary = df[df["pb_group"] == 1].sort_values(
        ["roa", "pb_ratio"], ascending=[False, True]
    )

    # 行业上限30%
    industry_raw = get_industry(primary["code"].tolist(), date=date_str)
    industry_map = {
        c: industry_raw.get(c, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        for c in primary["code"].tolist()
    }
    picks = []
    industry_counts = {}
    limit_count = max(1, int(hold_num * 0.3))
    for code in primary["code"].tolist():
        if len(picks) >= hold_num:
            break
        ind = industry_map.get(code, "Unknown")
        if industry_counts.get(ind, 0) < limit_count:
            picks.append(code)
            industry_counts[ind] = industry_counts.get(ind, 0) + 1
    return picks


# ========== 策略3: 增强选股版 ==========
def strategy_enhanced(date_str, hold_num=15):
    """增强版: 综合评分 + 行业上限"""
    stocks = get_universe(date_str)
    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["roa"] > 0)]
    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # 综合评分
    df["质量分"] = 100
    df["估值分"] = (1 - df["pb_group"] / 10) * 100
    df["成长分"] = np.clip(df["roa"] * 2, 0, 100)
    df["综合分"] = df["质量分"] * 0.5 + df["估值分"] * 0.3 + df["成长分"] * 0.2

    primary = df[df["pb_group"] <= 1].sort_values(
        ["综合分", "pb_ratio"], ascending=[False, True]
    )

    # 行业上限
    industry_raw = get_industry(primary["code"].tolist(), date=date_str)
    industry_map = {
        c: industry_raw.get(c, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        for c in primary["code"].tolist()
    }
    picks = []
    industry_counts = {}
    limit_count = max(1, int(hold_num * 0.3))
    for code in primary["code"].tolist():
        if len(picks) >= hold_num:
            break
        ind = industry_map.get(code, "Unknown")
        if industry_counts.get(ind, 0) < limit_count:
            picks.append(code)
            industry_counts[ind] = industry_counts.get(ind, 0) + 1
    return picks


# ========== 运行回测 ==========
results = {
    "V2原版": {"returns": [], "desc": "PB10%+ROA排序"},
    "Release V1": {"returns": [], "desc": "PB10%+行业上限30%"},
    "增强选股版": {"returns": [], "desc": "综合评分+行业上限"},
}

print("\n开始回测...")

for i, date in enumerate(test_dates[:-1]):
    next_date = test_dates[i + 1]
    print(f"\n[{i + 1}/{len(test_dates) - 1}] {date} -> {next_date}")

    breadth, trend = calc_market_state(date)
    print(f"  广度={breadth:.2f}, 趋势={'↑' if trend else '↓'}")

    # 根据市场状态调整持仓
    if breadth < 0.15 and not trend:
        hold_num = 0
    elif breadth < 0.25 and not trend:
        hold_num = 10
    else:
        hold_num = 20

    # V2原版
    v2_picks = strategy_v2(date, hold_num) if hold_num > 0 else []
    v2_ret = calc_return(v2_picks, date, next_date)
    results["V2原版"]["returns"].append(v2_ret)
    print(f"  V2原版: {len(v2_picks)}只, 收益={v2_ret * 100:.2f}%")

    # Release V1
    r1_hold = int(hold_num * 0.75) if hold_num > 0 else 0
    r1_picks = strategy_release_v1(date, r1_hold) if r1_hold > 0 else []
    r1_ret = calc_return(r1_picks, date, next_date)
    results["Release V1"]["returns"].append(r1_ret)
    print(f"  Release V1: {len(r1_picks)}只, 收益={r1_ret * 100:.2f}%")

    # 增强选股版
    enh_hold = int(hold_num * 0.75) if hold_num > 0 else 0
    enh_picks = strategy_enhanced(date, enh_hold) if enh_hold > 0 else []
    enh_ret = calc_return(enh_picks, date, next_date)
    results["增强选股版"]["returns"].append(enh_ret)
    print(f"  增强选股版: {len(enh_picks)}只, 收益={enh_ret * 100:.2f}%")


# ========== 汇总结果 ==========
print("\n" + "=" * 70)
print("回测结果汇总")
print("=" * 70)

summary = []
for name, data in results.items():
    returns = data["returns"]
    total = np.sum(returns) * 100
    avg = np.mean(returns) * 100
    std = np.std(returns) * 100
    sharpe = (
        (np.mean(returns) / np.std(returns) * np.sqrt(4)) if np.std(returns) > 0 else 0
    )
    win = len([r for r in returns if r > 0]) / len(returns) * 100 if returns else 0

    summary.append(
        {
            "strategy": name,
            "desc": data["desc"],
            "total_return": round(total, 2),
            "avg_quarterly": round(avg, 2),
            "sharpe": round(sharpe, 2),
            "win_rate": round(win, 1),
            "max_drawdown": round(min(returns) * 100, 2) if returns else 0,
        }
    )

    print(f"\n{name} ({data['desc']})")
    print(f"  累计收益: {total:.2f}%")
    print(f"  季度平均: {avg:.2f}%")
    print(f"  夏普比率: {sharpe:.2f}")
    print(f"  胜率: {win:.1f}%")
    print(f"  最差季度: {min(returns) * 100:.2f}%" if returns else "  无交易")

print("\n" + "-" * 70)
print(f"{'策略':<20} {'累计收益':>10} {'季度平均':>10} {'夏普':>8} {'胜率':>8}")
print("-" * 70)
for s in summary:
    print(
        f"{s['strategy']:<20} {s['total_return']:>9.2f}% {s['avg_quarterly']:>9.2f}% {s['sharpe']:>8.2f} {s['win_rate']:>7.1f}%"
    )

# 保存结果
result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_comparison_final.json"
)
with open(result_file, "w") as f:
    json.dump(
        {
            "test_period": f"{test_dates[0]} to {test_dates[-1]}",
            "test_dates": test_dates,
            "summary": summary,
            "quarterly_returns": {
                k: [r * 100 for r in v["returns"]] for k, v in results.items()
            },
        },
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"\n✓ 结果已保存: {result_file}")
print("\n" + "=" * 70)
print("对比完成!")
print("=" * 70)

# 结论
print("\n=== 结论 ===")
best_return = max(summary, key=lambda x: x["total_return"])
best_sharpe = max(summary, key=lambda x: x["sharpe"])
print(f"\n收益最高: {best_return['strategy']} ({best_return['total_return']:.2f}%)")
print(f"夏普最优: {best_sharpe['strategy']} (夏普{best_sharpe['sharpe']:.2f})")
