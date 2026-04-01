#!/usr/bin/env python3
"""
任务06v2：阈值优化 - 中等简化版
测试更多日期，验证阈值效果
"""

from jqdata import *
import numpy as np
import json

print("=" * 60)
print("情绪开关阈值优化测试")
print("=" * 60)

thresholds = [0, 20, 30, 40, 50, 60]
test_dates = [
    "2021-01-15",
    "2021-02-15",
    "2021-03-15",
    "2021-04-15",
    "2021-05-15",
    "2021-06-15",
    "2021-07-15",
    "2021-08-15",
    "2021-09-15",
    "2021-10-15",
    "2021-11-15",
    "2021-12-15",
    "2022-01-15",
    "2022-02-15",
    "2022-03-15",
    "2022-04-15",
    "2022-05-15",
    "2022-06-15",
    "2022-07-15",
    "2022-08-15",
    "2022-09-15",
    "2022-10-15",
    "2022-11-15",
    "2022-12-15",
    "2023-01-15",
    "2023-02-15",
    "2023-03-15",
    "2023-04-15",
    "2023-05-15",
    "2023-06-15",
    "2023-07-15",
    "2023-08-15",
    "2023-09-15",
    "2023-10-15",
    "2023-11-15",
    "2023-12-15",
    "2024-01-15",
    "2024-02-15",
    "2024-03-15",
    "2024-04-15",
    "2024-05-15",
    "2024-06-15",
    "2024-07-15",
    "2024-08-15",
    "2024-09-15",
    "2024-10-15",
    "2024-11-15",
    "2024-12-15",
    "2025-01-15",
    "2025-02-15",
    "2025-03-15",
]

OOS_START = "2024-01-01"


def get_zt_count(date):
    stocks = get_all_securities("stock", date).index.tolist()[:1200]
    stocks = [s for s in stocks if not s.startswith("68")]
    df = get_price(
        stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    return len(df[df["close"] == df["high_limit"]])


def get_zt_stocks(date):
    stocks = get_all_securities("stock", date).index.tolist()[:800]
    stocks = [s for s in stocks if not s.startswith("68")]
    df = get_price(
        stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    return list(df[df["close"] == df["high_limit"]]["code"])[:15]


print(f"\n测试日期: {len(test_dates)}")

results = {}

for threshold in thresholds:
    print(f"\n阈值{threshold}...")

    in_signals = 0
    in_returns = []
    in_wins = 0

    oos_signals = 0
    oos_returns = []
    oos_wins = 0

    for i in range(1, len(test_dates)):
        prev = test_dates[i - 1]
        date = test_dates[i]

        try:
            zt = get_zt_count(prev)

            if threshold > 0 and zt < threshold:
                continue

            is_oos = date >= OOS_START

            if is_oos:
                oos_signals += 1
            else:
                in_signals += 1

            zt_list = get_zt_stocks(prev)

            day_returns = []
            for stock in zt_list[:8]:
                try:
                    prev_df = get_price(
                        stock, end_date=prev, count=1, fields=["close"], panel=False
                    )
                    today_df = get_price(
                        stock,
                        end_date=date,
                        count=1,
                        fields=["open", "close"],
                        panel=False,
                    )

                    if len(prev_df) > 0 and len(today_df) > 0:
                        prev_close = prev_df.iloc[0]["close"]
                        open_price = today_df.iloc[0]["open"]
                        close_price = today_df.iloc[0]["close"]

                        open_pct = (open_price / prev_close - 1) * 100

                        if 0 <= open_pct <= 5:
                            ret = (close_price / open_price - 1) * 100
                            day_returns.append(ret)

                            if is_oos:
                                if ret > 0:
                                    oos_wins += 1
                            else:
                                if ret > 0:
                                    in_wins += 1
                except:
                    pass

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                if is_oos:
                    oos_returns.append(avg_ret)
                else:
                    in_returns.append(avg_ret)
        except:
            pass

    in_avg = np.mean(in_returns) if in_returns else 0
    in_win_rate = in_wins / len(in_returns) * 100 if in_returns else 0

    oos_avg = np.mean(oos_returns) if oos_returns else 0
    oos_win_rate = oos_wins / len(oos_returns) * 100 if oos_returns else 0

    results[threshold] = {
        "in_signals": in_signals,
        "in_trades": len(in_returns),
        "in_avg_return": round(in_avg, 3),
        "in_win_rate": round(in_win_rate, 2),
        "oos_signals": oos_signals,
        "oos_trades": len(oos_returns),
        "oos_avg_return": round(oos_avg, 3),
        "oos_win_rate": round(oos_win_rate, 2),
    }

    print(
        f"  样本内: {in_signals}信号, {len(in_returns)}交易, {in_avg:.3f}%, {in_win_rate:.2f}%"
    )
    print(
        f"  样本外: {oos_signals}信号, {len(oos_returns)}交易, {oos_avg:.3f}%, {oos_win_rate:.2f}%"
    )

print("\n" + "=" * 60)
print("汇总对比")
print("=" * 60)

print("\n样本内:")
for t, r in results.items():
    print(f"阈值{t}: {r['in_avg_return']}%, 胜率{r['in_win_rate']}%")

print("\n样本外:")
for t, r in results.items():
    print(f"阈值{t}: {r['oos_avg_return']}%, 胜率{r['oos_win_rate']}%")

print("\n完成")
