#!/usr/bin/env python3
"""
任务06v2：阈值优化 - 超简化版
只测试3个阈值，用最少采样
"""

from jqdata import *
import numpy as np
import json
import os

print("阈值优化超简化版")

thresholds = [0, 30, 50]
test_dates = [
    "2021-03-01",
    "2021-06-01",
    "2021-09-01",
    "2021-12-01",
    "2022-03-01",
    "2022-06-01",
    "2022-09-01",
    "2022-12-01",
    "2023-03-01",
    "2023-06-01",
    "2023-09-01",
    "2023-12-01",
    "2024-03-01",
    "2024-06-01",
    "2024-09-01",
    "2024-12-01",
]

OOS_START = "2024-01-01"


def get_zt_count(date):
    stocks = get_all_securities("stock", date).index.tolist()[:1000]
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
    return list(df[df["close"] == df["high_limit"]]["code"])[:10]


results = {}

for threshold in thresholds:
    print(f"\n阈值{threshold}...")

    signals = 0
    returns = []
    wins = 0

    for i in range(1, len(test_dates)):
        prev = test_dates[i - 1]
        date = test_dates[i]

        try:
            zt = get_zt_count(prev)

            if threshold > 0 and zt < threshold:
                continue

            signals += 1

            zt_list = get_zt_stocks(prev)

            for stock in zt_list[:5]:
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
                            returns.append(ret)
                            if ret > 0:
                                wins += 1
                except:
                    pass
        except:
            pass

    avg_ret = np.mean(returns) if returns else 0
    win_rate = wins / len(returns) * 100 if returns else 0

    results[threshold] = {
        "signals": signals,
        "trades": len(returns),
        "avg_return": round(avg_ret, 3),
        "win_rate": round(win_rate, 2),
    }

    print(
        f"  信号:{signals}, 交易:{len(returns)}, 收益:{avg_ret:.3f}%, 胜率:{win_rate:.2f}%"
    )

print("\n结果:")
for t, r in results.items():
    print(f"阈值{t}: {r}")

os.makedirs("/Users/fengzhi/Downloads/git/testlixingren/output", exist_ok=True)
with open(
    "/Users/fengzhi/Downloads/git/testlixingren/output/threshold_mini.json", "w"
) as f:
    json.dump(results, f)

print("\n完成")
