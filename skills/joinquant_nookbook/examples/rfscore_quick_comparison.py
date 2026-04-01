#!/usr/bin/env python3
"""
RFScore 四策略快速对比验证

对比版本：
1. rfscore7_pb10_final_v2.py (V2原版)
2. rfscore7_pb10_enhanced_selection.py (增强选股版)
3. rfscore7_pb10_multi_signal_risk_control.py (多信号风控版)
4. rfscore_defensive_dynamic_hedge.py (动态对冲版)

测试时间：2024-01-01, 2024-06-01, 2025-01-01
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 70)
print("RFScore 四策略快速对比验证")
print("=" * 70)


def get_universe(date_str):
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


def calc_breadth(date_str):
    hs300 = get_index_stocks("000300.XSHG", date=date_str)
    prices = get_price(
        hs300, end_date=date_str, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    return float((close.iloc[-1] > close.mean()).mean())


def calc_trend(date_str):
    idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
    return float(idx["close"].iloc[-1]) > float(idx["close"].mean())


def select_stocks_v2(date_str, hold_num=20):
    """V2原版: PB10% + ROA排序"""
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


def select_stocks_enhanced(date_str, hold_num=15):
    """增强选股版: 综合评分 + 行业上限"""
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
    df["综合分"] = 100 - df["pb_group"] * 10 + df["roa"] * 2
    primary = df[df["pb_group"] <= 1].sort_values(
        ["综合分", "pb_ratio"], ascending=[False, True]
    )

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


def calc_return(stocks, start, end):
    if not stocks:
        return 0
    returns = []
    for s in stocks:
        try:
            p1 = get_price(s, end_date=start, count=1, fields=["close"], panel=False)
            p2 = get_price(s, end_date=end, count=1, fields=["close"], panel=False)
            if not p1.empty and not p2.empty:
                r = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                    p1["close"].iloc[-1]
                )
                returns.append(r)
        except:
            pass
    return np.mean(returns) if returns else 0


test_dates = [
    ("2024-01-01", "2024-03-01"),
    ("2024-06-01", "2024-09-01"),
    ("2025-01-01", "2025-03-01"),
]

print(f"\n测试日期: {[d[0] for d in test_dates]}")

results = {
    "V2原版": {"returns": [], "desc": "PB10%+ROA排序"},
    "增强选股版": {"returns": [], "desc": "综合评分+行业上限"},
}

for start_date, end_date in test_dates:
    print(f"\n{'=' * 70}")
    print(f"测试日期: {start_date} -> {end_date}")
    print("=" * 70)

    breadth = calc_breadth(start_date)
    trend = calc_trend(start_date)
    print(f"市场状态: 广度={breadth:.3f}, 趋势={'↑' if trend else '↓'}")

    # V2原版
    v2_hold = 20 if breadth >= 0.25 or trend else (10 if breadth >= 0.15 else 0)
    v2_picks = select_stocks_v2(start_date, v2_hold) if v2_hold > 0 else []
    v2_ret = calc_return(v2_picks, start_date, end_date)
    results["V2原版"]["returns"].append(v2_ret)
    print(f"\nV2原版: 持仓={len(v2_picks)}, 收益={v2_ret * 100:.2f}%")

    # 增强选股版
    enh_hold = 15 if breadth >= 0.25 or trend else (7 if breadth >= 0.15 else 0)
    enh_picks = select_stocks_enhanced(start_date, enh_hold) if enh_hold > 0 else []
    enh_ret = calc_return(enh_picks, start_date, end_date)
    results["增强选股版"]["returns"].append(enh_ret)
    print(f"增强选股版: 持仓={len(enh_picks)}, 收益={enh_ret * 100:.2f}%")


print("\n" + "=" * 70)
print("结果汇总")
print("=" * 70)

summary = []
for name, data in results.items():
    returns = data["returns"]
    total = np.sum(returns) * 100
    avg = np.mean(returns) * 100
    std = np.std(returns) * 100
    sharpe = (
        np.mean(returns) / np.std(returns) * np.sqrt(12) if np.std(returns) > 0 else 0
    )
    win = len([r for r in returns if r > 0]) / len(returns) * 100 if returns else 0
    summary.append(
        {
            "name": name,
            "desc": data["desc"],
            "total_return": round(total, 2),
            "avg_return": round(avg, 2),
            "sharpe": round(sharpe, 2),
            "win_rate": round(win, 1),
        }
    )
    print(f"\n{name} ({data['desc']})")
    print(f"  累计收益: {total:.2f}%")
    print(f"  平均收益: {avg:.2f}%")
    print(f"  夏普比率: {sharpe:.2f}")
    print(f"  胜率: {win:.1f}%")

print("\n" + "-" * 70)
print(f"{'策略':<20} {'累计收益':>10} {'平均收益':>10} {'夏普':>8} {'胜率':>8}")
print("-" * 70)
for s in summary:
    print(
        f"{s['name']:<20} {s['total_return']:>9.2f}% {s['avg_return']:>9.2f}% {s['sharpe']:>8.2f} {s['win_rate']:>7.1f}%"
    )

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_quick_comparison.json"
)
with open(result_file, "w") as f:
    json.dump(
        {
            "test_period": "2024-01-01 to 2025-03-01",
            "test_dates": [d[0] for d in test_dates],
            "summary": summary,
        },
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"\n结果已保存: {result_file}")
print("\n" + "=" * 70)
print("验证完成!")
print("=" * 70)
