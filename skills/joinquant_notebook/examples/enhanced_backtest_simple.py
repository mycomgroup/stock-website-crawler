#!/usr/bin/env python3
"""
增强策略 Notebook 回测（简化版）
仅测试 2023-2024 年
"""

from jqdata import *
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

print("=" * 70)
print("增强策略 Notebook 回测（简化版）")
print("回测时间：2023-01-01 至 2024-12-31")
print("=" * 70)

START_DATE = "2023-01-01"
END_DATE = "2024-12-31"
IPO_DAYS = 180


def get_trade_months(start, end):
    all_days = get_trade_days(start, end)
    months = {}
    for d in all_days:
        key = d[:7]
        if key not in months:
            months[key] = d
    return sorted(months.values())


def get_stocks(date_str):
    hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
    zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
    stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

    # 过滤新股
    threshold = (
        datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=IPO_DAYS)
    ).strftime("%Y-%m-%d")
    sec = get_all_securities("stock", date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= threshold]
    stocks = sec.index.tolist()

    # 过滤 ST
    is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()
    return stocks


def select_base(date_str, n=20):
    """基础选股：ROA > 0 + PB 最低"""
    stocks = get_stocks(date_str)
    if len(stocks) < 10:
        return []

    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str).dropna()
    df = df[df["roa"] > 0]
    if df.empty:
        return []

    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    selected = df[df["pb_group"] <= 1].sort_values("roa", ascending=False)
    return selected["code"].tolist()[:n]


def calc_breadth(date_str):
    """市场广度"""
    hs300 = get_index_stocks("000300.XSHG", date=date_str)[:50]
    above = 0
    total = 0
    for s in hs300:
        try:
            p = get_price(s, end_date=date_str, count=20, fields="close", panel=False)
            if len(p) >= 20:
                if p["close"].iloc[-1] > p["close"].mean():
                    above += 1
                total += 1
        except:
            pass
    return above / max(total, 1)


def calc_sentiment(date_str):
    """情绪指标：涨停数"""
    all_s = get_all_securities("stock", date=date_str).index.tolist()
    sample = [s for s in all_s if s[0] not in ["4", "8"] and not s.startswith("68")][
        :200
    ]
    try:
        df = get_price(
            sample,
            end_date=date_str,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        ).dropna()
        return len(df[df["close"] >= df["high_limit"] * 0.995])
    except:
        return 0


def select_enhanced(date_str, n=15):
    """增强选股"""
    breadth = calc_breadth(date_str)
    sentiment = calc_sentiment(date_str)

    if breadth < 0.15:
        return [], breadth, sentiment, "清仓"
    elif breadth < 0.25:
        n = 10
        reason = "底部"
    elif breadth < 0.40 and sentiment < 20:
        n = 8
        reason = "减仓"
    else:
        reason = "正常"

    stocks = select_base(date_str, n)
    return stocks, breadth, sentiment, reason


def calc_return(stocks, d1, d2):
    if not stocks:
        return 0
    rets = []
    for s in stocks:
        try:
            p1 = get_price(s, end_date=d1, count=1, fields="close", panel=False)
            p2 = get_price(s, end_date=d2, count=1, fields="close", panel=False)
            if not p1.empty and not p2.empty:
                rets.append(
                    (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1]))
                    / float(p1["close"].iloc[-1])
                )
        except:
            pass
    return np.mean(rets) if rets else 0


# 主回测
months = get_trade_months(START_DATE, END_DATE)
print(f"\n测试月份数: {len(months)}")

base_rets = []
enh_rets = []
skip_months = []

print("\n--- 原始策略 ---")
for i, m in enumerate(months):
    next_m = months[i + 1] if i + 1 < len(months) else END_DATE
    stocks = select_base(m, 20)
    r = calc_return(stocks, m, next_m)
    base_rets.append(r)
    print(f"[{i + 1}/{len(months)}] {m}: {len(stocks)}只, {r * 100:.2f}%")

print("\n--- 增强策略 ---")
for i, m in enumerate(months):
    next_m = months[i + 1] if i + 1 < len(months) else END_DATE
    stocks, br, se, reason = select_enhanced(m)

    if stocks:
        r = calc_return(stocks, m, next_m)
        enh_rets.append(r)
        print(
            f"[{i + 1}/{len(months)}] {m}: 广度={br:.2f} 情绪={se} {reason} -> {len(stocks)}只, {r * 100:.2f}%"
        )
    else:
        enh_rets.append(0)
        skip_months.append(m)
        print(f"[{i + 1}/{len(months)}] {m}: 广度={br:.2f} 情绪={se} -> 清仓观望")


# 统计
def stats(rets):
    if not rets:
        return {"total": 0, "avg": 0, "sharpe": 0, "win": 0}
    total = (1 + pd.Series(rets)).prod() - 1
    avg = np.mean(rets)
    std = np.std(rets) if len(rets) > 1 else 0.01
    sharpe = avg / std * np.sqrt(12) if std > 0 else 0
    win = sum(1 for r in rets if r > 0) / len(rets)
    return {"total": total * 100, "avg": avg * 100, "sharpe": sharpe, "win": win * 100}


bs = stats(base_rets)
es = stats(enh_rets)

print("\n" + "=" * 70)
print("策略对比")
print("=" * 70)
print(f"{'指标':<15} {'原始':<15} {'增强':<15} {'差异'}")
print("-" * 60)
print(
    f"{'累计收益':<15} {bs['total']:.2f}%{'':<10} {es['total']:.2f}%{'':<10} {es['total'] - bs['total']:+.2f}%"
)
print(
    f"{'月均收益':<15} {bs['avg']:.2f}%{'':<10} {es['avg']:.2f}%{'':<10} {es['avg'] - bs['avg']:+.2f}%"
)
print(
    f"{'夏普比率':<15} {bs['sharpe']:.2f}{'':<12} {es['sharpe']:.2f}{'':<12} {es['sharpe'] - bs['sharpe']:+.2f}"
)
print(
    f"{'胜率':<15} {bs['win']:.1f}%{'':<10} {es['win']:.1f}%{'':<10} {es['win'] - bs['win']:+.1f}%"
)
print(f"\n清仓月份: {len(skip_months)} 次")

if es["sharpe"] > bs["sharpe"]:
    print("\n✓ 增强策略风险调整后收益更好")
print("=" * 70)
