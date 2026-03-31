#!/usr/bin/env python3
"""
RFScore 三策略最近三个月对比 - 简化版
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 60)
print("RFScore 三策略对比 - 最近三个月")
print("=" * 60)


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


def select_stocks(date_str, hold_num, pb_group_max=1):
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
    picks = df[df["pb_group"] <= pb_group_max].head(hold_num)["code"].tolist()
    return picks


def calc_return(stocks, start, end):
    if not stocks:
        return 0
    returns = []
    for s in stocks:
        try:
            p1 = get_price(s, end_date=start, count=1, fields="close", panel=False)
            p2 = get_price(s, end_date=end, count=1, fields="close", panel=False)
            if not p1.empty and not p2.empty:
                r = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                    p1["close"].iloc[-1]
                )
                returns.append(r)
        except:
            pass
    return np.mean(returns) if returns else 0


dates = ["2025-12-30", "2026-01-05", "2026-02-05", "2026-03-02"]
print(f"\n测试日期: {dates}")

results = {"v2": [], "release": [], "defensive": []}

for i, d in enumerate(dates):
    print(f"\n[{i + 1}/{len(dates)}] {d}")

    breadth = calc_breadth(d)
    trend = calc_trend(d)
    print(f"  广度={breadth:.3f}, 趋势={'向上' if trend else '向下'}")

    next_dates = get_trade_days(d, "2026-03-28")
    next_d = str(next_dates[20]) if len(next_dates) > 20 else str(next_dates[-1])

    # V2: 20只 or 10只
    v2_hold = 20 if breadth >= 0.25 or trend else (10 if breadth >= 0.15 else 0)
    v2_picks = select_stocks(d, v2_hold, 1) if v2_hold > 0 else []
    v2_ret = calc_return(v2_picks, d, next_d)
    results["v2"].append(v2_ret)
    print(f"  V2: 持仓={len(v2_picks)}, 收益={v2_ret * 100:.2f}%")

    # Release V1: 15/12/10/0
    if breadth < 0.15:
        r1_hold = 0
    elif breadth < 0.25:
        r1_hold = 10
    elif breadth < 0.35 and not trend:
        r1_hold = 12
    else:
        r1_hold = 15
    r1_picks = select_stocks(d, r1_hold, 1) if r1_hold > 0 else []
    r1_ret = calc_return(r1_picks, d, next_d)
    results["release"].append(r1_ret)
    print(f"  ReleaseV1: 持仓={len(r1_picks)}, 收益={r1_ret * 100:.2f}%")

    # Defensive: 50%进攻 + 30%ETF
    def_weight = 0.5 if breadth >= 0.25 or trend else (0.25 if breadth >= 0.15 else 0)
    def_picks = select_stocks(d, 10, 1)
    def_stock_ret = calc_return(def_picks, d, next_d)
    def_etf_ret = calc_return(["511010.XSHG", "518880.XSHG", "510880.XSHG"], d, next_d)
    def_ret = def_stock_ret * def_weight + def_etf_ret * 0.3
    results["defensive"].append(def_ret)
    print(
        f"  Defensive: 仓位={def_weight:.0%}, 股票={def_stock_ret * 100:.2f}%, ETF={def_etf_ret * 100:.2f}%, 组合={def_ret * 100:.2f}%"
    )

print("\n" + "=" * 60)
print("结果汇总")
print("=" * 60)

for name, rets in results.items():
    total = np.sum(rets) * 100
    avg = np.mean(rets) * 100
    sharpe = np.mean(rets) / np.std(rets) * np.sqrt(12) if np.std(rets) > 0 else 0
    win = len([r for r in rets if r > 0]) / len(rets) * 100
    print(
        f"{name}: 累计={total:.2f}%, 月均={avg:.2f}%, 夏普={sharpe:.2f}, 胜率={win:.0f}%"
    )

with open(
    "/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_3m_comparison.json", "w"
) as f:
    json.dump({k: [r * 100 for r in v] for k, v in results.items()}, f)

print("\n结果已保存到 output/rfscore_3m_comparison.json")
