#!/usr/bin/env python3
"""
任务06v2：阈值优化 - 超简化版
只测试0, 30, 50三个阈值，最少采样
"""

from jqdata import *
import json

print("阈值优化测试")

thresholds = [0, 30, 50]
test_dates = [
    "2021-03-01",
    "2021-06-01",
    "2021-09-01",
    "2022-03-01",
    "2022-06-01",
    "2022-09-01",
    "2023-03-01",
    "2023-06-01",
    "2023-09-01",
    "2024-03-01",
    "2024-06-01",
    "2024-09-01",
]


def get_zt_count(date):
    stocks = get_all_securities("stock", date).index.tolist()[:500]
    stocks = [s for s in stocks if not s.startswith("68")]
    df = get_price(
        stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    return len(df[df["close"] == df["high_limit"]])


results = {}
for t in thresholds:
    count = 0
    for d in test_dates:
        zt = get_zt_count(d)
        if t == 0 or zt >= t:
            count += 1
    results[t] = count
    print(f"阈值{t}: 通过{count}天")

print(json.dumps(results, indent=2))
