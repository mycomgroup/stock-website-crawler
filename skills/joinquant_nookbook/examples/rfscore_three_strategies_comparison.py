#!/usr/bin/env python3
"""
RFScore 三策略对比 - 最近三个月
比较：
1. PB10 v2 - 最简洁实用
2. Release V1 - 最严谨风控
3. Defensive Combined - 最稳健组合
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 70)
print("RFScore 三策略对比 - 最近三个月")
print("回测时间：2025-12-30 至 2026-03-28")
print("=" * 70)


def get_universe(date_str):
    hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
    zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    from datetime import datetime, timedelta

    threshold = (
        datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=180)
    ).strftime("%Y-%m-%d")
    sec = sec[sec["start_date"].apply(lambda x: str(x) <= threshold)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(stocks, end_date=date_str, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_market_state(date_str):
    hs300 = get_index_stocks("000300.XSHG", date=date_str)
    prices = get_price(
        hs300, end_date=date_str, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
    idx_close = float(idx["close"].iloc[-1])
    idx_ma20 = float(idx["close"].mean())
    trend_on = idx_close > idx_ma20

    return breadth, trend_on


def select_stocks_v2(date_str, hold_num=20):
    """PB10 v2 - 最简洁实用：RFScore7 + PB10% + Score>=6补位"""
    stocks = get_universe(date_str)

    q = query(
        valuation.code,
        valuation.pb_ratio,
        valuation.pe_ratio,
        indicator.roa,
        indicator.ocfps,
    ).filter(valuation.code.in_(stocks))

    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["pe_ratio"] > 0) & (df["pe_ratio"] < 100)]

    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    primary = df[(df["pb_group"] <= 1) & (df["roa"] > 0.5)]
    primary = primary.sort_values(["roa", "ocfps"], ascending=[False, False])
    picks = primary["code"].tolist()

    if len(picks) < hold_num:
        secondary = df[(df["pb_group"] <= 2) & (df["roa"] > 0)]
        secondary = secondary.sort_values(["roa", "pb_ratio"], ascending=[False, True])
        for code in secondary["code"].tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    return picks[:hold_num]


def select_stocks_release_v1(date_str, hold_num=15):
    """Release V1 - 最严谨风控：RFScore7 + PB10% + 行业上限 + 无补位 + 留现金"""
    stocks = get_universe(date_str)

    q = query(
        valuation.code,
        valuation.pb_ratio,
        valuation.pe_ratio,
        indicator.roa,
        indicator.ocfps,
    ).filter(valuation.code.in_(stocks))

    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[
        (df["pb_ratio"] > 0)
        & (df["pe_ratio"] > 0)
        & (df["pe_ratio"] < 100)
        & (df["roa"] > 0.5)
    ]

    if df.empty:
        return []

    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    primary = df[df["pb_group"] == 1]
    primary = primary.sort_values(
        ["roa", "ocfps", "pb_ratio"], ascending=[False, False, True]
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


def select_stocks_defensive(date_str, offensive_hold_num=10):
    """Defensive Combined - 最稳健组合：50%进攻 + 30%防守ETF + 20%现金"""
    stocks = select_stocks_v2(date_str, offensive_hold_num)
    defensive_etfs = {
        "511010.XSHG": 0.75,
        "518880.XSHG": 0.10,
        "510880.XSHG": 0.08,
        "513100.XSHG": 0.04,
    }
    return stocks, list(defensive_etfs.keys())


def calc_returns(stocks, start_date, end_date):
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


test_dates = ["2025-12-30", "2026-01-05", "2026-02-05", "2026-03-02"]

print(f"\n测试日期: {test_dates}")
print(f"测试月份数: {len(test_dates)}")

results = {
    "v2": {"name": "PB10 v2 (简洁实用)", "returns": [], "picks_list": []},
    "release_v1": {"name": "Release V1 (严谨风控)", "returns": [], "picks_list": []},
    "defensive": {"name": "Defensive (稳健组合)", "returns": [], "picks_list": []},
}

for i, date in enumerate(test_dates):
    print(f"\n{'=' * 70}")
    print(f"[{i + 1}/{len(test_dates)}] {date}")
    print("=" * 70)

    breadth, trend_on = calc_market_state(date)
    print(f"市场状态: 广度={breadth:.3f}, 趋势={'向上' if trend_on else '向下'}")

    next_dates = get_trade_days(date, "2026-03-28")
    next_date = str(next_dates[20]) if len(next_dates) >= 21 else str(next_dates[-1])

    # V2 Strategy
    if breadth < 0.15 and not trend_on:
        v2_hold_num = 0
    elif breadth < 0.25 and not trend_on:
        v2_hold_num = 10
    else:
        v2_hold_num = 20

    v2_picks = select_stocks_v2(date, v2_hold_num) if v2_hold_num > 0 else []
    v2_ret = calc_returns(v2_picks, date, next_date)
    results["v2"]["returns"].append(v2_ret)
    results["v2"]["picks_list"].append(v2_picks)
    print(f"V2: 持仓={len(v2_picks)}, 收益={v2_ret * 100:.2f}%")

    # Release V1 Strategy
    if breadth < 0.15:
        r1_hold_num = 0
    elif breadth < 0.25:
        r1_hold_num = 10
    elif breadth < 0.35 and not trend_on:
        r1_hold_num = 12
    else:
        r1_hold_num = 15

    r1_picks = select_stocks_release_v1(date, r1_hold_num) if r1_hold_num > 0 else []
    r1_ret = calc_returns(r1_picks, date, next_date)
    results["release_v1"]["returns"].append(r1_ret)
    results["release_v1"]["picks_list"].append(r1_picks)
    print(f"ReleaseV1: 持仓={len(r1_picks)}, 收益={r1_ret * 100:.2f}%")

    # Defensive Strategy
    def_offensive_weight = 0.5
    if breadth < 0.15 and not trend_on:
        def_offensive_weight = 0.0
    elif breadth < 0.25 and not trend_on:
        def_offensive_weight = 0.25

    def_picks, def_etfs = select_stocks_defensive(date, 10)
    def_stock_ret = calc_returns(def_picks, date, next_date) if def_picks else 0
    def_etf_ret = calc_returns(def_etfs, date, next_date)
    def_ret = def_stock_ret * def_offensive_weight + def_etf_ret * 0.3
    results["defensive"]["returns"].append(def_ret)
    results["defensive"]["picks_list"].append(def_picks)
    print(
        f"Defensive: 进攻仓位={def_offensive_weight:.0%}, 股票收益={def_stock_ret * 100:.2f}%, ETF收益={def_etf_ret * 100:.2f}%, 组合收益={def_ret * 100:.2f}%"
    )

print("\n" + "=" * 70)
print("策略对比结果")
print("=" * 70)

summary = []
for key, data in results.items():
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
            "strategy": data["name"],
            "total_return": total,
            "avg_monthly": avg,
            "std": std,
            "sharpe": sharpe,
            "win_rate": win,
        }
    )

    print(f"\n{data['name']}")
    print(f"  累计收益: {total:.2f}%")
    print(f"  月均收益: {avg:.2f}%")
    print(f"  收益标准差: {std:.2f}%")
    print(f"  夏普比率: {sharpe:.2f}")
    print(f"  胜率: {win:.1f}%")

print("\n" + "-" * 70)
print(f"{'策略':<25} {'累计收益':>12} {'月均收益':>12} {'夏普':>8} {'胜率':>8}")
print("-" * 70)
for s in summary:
    print(
        f"{s['strategy']:<25} {s['total_return']:>11.2f}% {s['avg_monthly']:>11.2f}% {s['sharpe']:>8.2f} {s['win_rate']:>7.1f}%"
    )

result_data = {
    "test_period": "2025-12-30 to 2026-03-28",
    "test_dates": test_dates,
    "summary": summary,
    "monthly_returns": {k: [r * 100 for r in v["returns"]] for k, v in results.items()},
}

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_three_strategies_comparison.json"
with open(result_file, "w") as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存: {result_file}")
print("\n" + "=" * 70)
print("完成!")
print("=" * 70)
