#!/usr/bin/env python3
"""
增强策略验证：2022-2024（含熊市）
"""

from jqdata import *
import pandas as pd
import numpy as np

print("增强策略验证：2022-2024")
print("包含 2022 年熊市")
print("=" * 50)

# 关键月份：熊市底部 + 反弹 + 正常
test_dates = [
    "2022-01-04",
    "2022-04-01",
    "2022-07-01",
    "2022-10-10",  # 熊市
    "2023-01-03",
    "2023-04-03",
    "2023-07-03",  # 反弹
    "2024-01-02",
    "2024-04-01",
    "2024-06-03",  # 正常
]
next_dates = [
    "2022-02-01",
    "2022-05-05",
    "2022-08-01",
    "2022-11-01",
    "2023-02-01",
    "2023-05-04",
    "2023-08-01",
    "2024-02-01",
    "2024-05-06",
    "2024-07-01",
]


def get_stocks(date):
    hs300 = get_index_stocks("000300.XSHG", date=date)
    zz500 = get_index_stocks("000905.XSHG", date=date)
    stocks = [s for s in set(hs300) | set(zz500) if not s.startswith("688")]
    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    return is_st[is_st == False].index.tolist()[:300]


def select_base(date, n=20):
    stocks = get_stocks(date)
    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date).dropna()
    df = df[df["roa"] > 0]
    if df.empty:
        return []
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"),
            min(10, len(df)),
            labels=False,
            duplicates="drop",
        )
        + 1
    )
    selected = df[df["pb_group"] <= 1].sort_values("roa", ascending=False)
    return selected["code"].tolist()[:n]


def calc_breadth(date):
    hs300 = get_index_stocks("000300.XSHG", date=date)[:30]
    above = 0
    for s in hs300:
        try:
            p = get_price(s, end_date=date, count=20, fields="close", panel=False)
            if len(p) >= 20 and p["close"].iloc[-1] > p["close"].mean():
                above += 1
        except:
            pass
    return above / max(len(hs300), 1)


def calc_sentiment(date):
    all_s = get_all_securities("stock", date=date).index.tolist()
    sample = [s for s in all_s if s[0] not in ["4", "8"] and not s.startswith("68")][
        :150
    ]
    try:
        df = get_price(
            sample, end_date=date, count=1, fields=["close", "high_limit"], panel=False
        ).dropna()
        return len(df[df["close"] >= df["high_limit"] * 0.995])
    except:
        return 0


def select_enhanced(date, n=15):
    breadth = calc_breadth(date)
    sentiment = calc_sentiment(date)

    # 四档决策
    if breadth < 0.15:
        return [], breadth, sentiment, "清仓(极端)"
    elif breadth < 0.25:
        n = 10
        reason = "底部"
    elif breadth < 0.40 and sentiment < 15:
        n = 8
        reason = "减仓(弱情绪)"
    else:
        reason = "正常"

    stocks = select_base(date, n)
    return stocks, breadth, sentiment, reason


def calc_return(stocks, d1, d2):
    if not stocks:
        return 0
    rets = []
    for s in stocks[:10]:
        try:
            p1 = get_price(s, end_date=d1, count=1, fields="close", panel=False)
            p2 = get_price(s, end_date=d2, count=1, fields="close", panel=False)
            if not p1.empty and not p2.empty:
                r = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                    p1["close"].iloc[-1]
                )
                rets.append(r)
        except:
            pass
    return np.mean(rets) if rets else 0


# 回测
print("\n原始策略：")
base_rets = []
for i, (d, nd) in enumerate(zip(test_dates, next_dates)):
    stocks = select_base(d, 20)
    r = calc_return(stocks, d, nd)
    base_rets.append(r)
    print(f"  {d}: {len(stocks)}只, 收益={r * 100:+.2f}%")

print("\n增强策略：")
enh_rets = []
skips = []
for i, (d, nd) in enumerate(zip(test_dates, next_dates)):
    stocks, br, se, reason = select_enhanced(d)
    if stocks:
        r = calc_return(stocks, d, nd)
        enh_rets.append(r)
        print(
            f"  {d}: 广度={br:.2f} 涨停={se} {reason} -> {len(stocks)}只, 收益={r * 100:+.2f}%"
        )
    else:
        enh_rets.append(0)
        skips.append(d)
        print(f"  {d}: 广度={br:.2f} 涨停={se} -> {reason}")

# 结果
print("\n" + "=" * 50)
base_total = (1 + pd.Series(base_rets)).prod() - 1
enh_total = (1 + pd.Series(enh_rets)).prod() - 1
base_sharpe = np.mean(base_rets) / (np.std(base_rets) + 0.001) * np.sqrt(12)
enh_sharpe = np.mean(enh_rets) / (np.std(enh_rets) + 0.001) * np.sqrt(12)

print("策略对比：")
print(f"  原始: 累计={base_total * 100:.2f}%, 夏普={base_sharpe:.2f}")
print(f"  增强: 累计={enh_total * 100:.2f}%, 夏普={enh_sharpe:.2f}")
print(f"  清仓避险: {len(skips)} 次")
if skips:
    print(f"  清仓月份: {skips}")
print("=" * 50)
