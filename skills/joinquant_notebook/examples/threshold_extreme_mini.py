#!/usr/bin/env python3
"""阈值测试 - 极简版（5个日期）"""

from jqdata import *
import numpy as np

print("阈值极简测试")

thresholds = [0, 30, 50]
dates = ["2022-01-04", "2022-06-01", "2023-01-04", "2023-06-01", "2024-01-04"]


def get_zt(date):
    stocks = list(get_all_securities("stock", date).index)[:500]
    stocks = [s for s in stocks if not s.startswith("68")]
    df = get_price(
        stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    return len(df[df["close"] == df["high_limit"]])


results = {}
for t in thresholds:
    signals = 0
    returns = []

    for i in range(1, len(dates)):
        prev = dates[i - 1]
        date = dates[i]

        zt = get_zt(prev)

        if t > 0 and zt < t:
            continue

        signals += 1

        stocks = list(get_all_securities("stock", prev).index)[:400]
        stocks = [s for s in stocks if not s.startswith("68")]
        prev_df = get_price(
            stocks, end_date=prev, count=1, fields=["close", "high_limit"], panel=False
        )
        zt_list = list(prev_df[prev_df["close"] == prev_df["high_limit"]]["code"])[:10]

        day_rets = []
        for stock in zt_list:
            try:
                b = get_price(
                    stock, end_date=date, count=1, fields=["open"], panel=False
                )
                s = get_price(
                    stock, end_date=date, count=1, fields=["high"], panel=False
                )

                if len(b) > 0 and len(s) > 0:
                    op = b.iloc[0]["open"]
                    hi = s.iloc[0]["high"]
                    day_rets.append((hi / op - 1) * 100)
            except:
                pass

        if day_rets:
            returns.append(np.mean(day_rets))

    avg = np.mean(returns) if returns else 0
    results[t] = {"signals": signals, "avg": round(avg, 3)}
    print(f"阈值{t}: {signals}信号, {avg:.3f}%")

print("\n完成")
