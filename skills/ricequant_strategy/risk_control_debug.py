# -*- coding: utf-8 -*-
"""
风控测试 - RiceQuant Notebook格式
快速验证策略逻辑
"""

print("=" * 60)
print("风控A/B测试 - RiceQuant Notebook验证")
print("=" * 60)

import datetime as dt
import pandas as pd
import numpy as np

test_date = "2023-06-01"
print(f"\n测试日期: {test_date}")

print("\n1. 获取股票池...")
all_stocks = all_instruments("CS")
stocks = [
    s.order_book_id
    for s in all_stocks
    if s.order_book_id[:2] != "68" and s.order_book_id[0] not in ["3", "4", "8"]
]
print(f"股票数量: {len(stocks)}")

print("\n2. 查找昨日涨停股...")
prev_date = pd.Timestamp(test_date) - dt.timedelta(days=1)
prev_date_str = prev_date.strftime("%Y-%m-%d")
print(f"前一日: {prev_date_str}")

limit_up_count = 0
limit_up_stocks = []

for stock in stocks[:100]:
    try:
        bars = history_bars(stock, 1, "1d", "close,limit_up,volume", prev_date_str)

        if bars is None or len(bars) == 0:
            continue

        close = bars[-1]["close"]
        limit_up = bars[-1]["limit_up"]
        volume = bars[-1]["volume"]

        if close >= limit_up * 0.99 and volume > 1000000:
            limit_up_stocks.append(stock)
            limit_up_count += 1

    except:
        continue

print(f"昨日涨停股数量: {limit_up_count}")
print(f"前5只: {limit_up_stocks[:5]}")

print("\n3. 检查弱转强条件...")
qualified_count = 0
qualified_stocks = []

for stock in limit_up_stocks[:20]:
    try:
        today_bars = history_bars(stock, 1, "1d", "open,limit_up", test_date)

        if today_bars is None or len(today_bars) == 0:
            continue

        open_price = today_bars[-1]["open"]
        limit_up = today_bars[-1]["limit_up"]

        if limit_up <= 0:
            continue

        open_ratio = open_price / (limit_up / 1.1)

        print(
            f"  {stock}: 开盘价{open_price:.2f}, 涨停价{limit_up:.2f}, 开盘比{open_ratio:.3f}"
        )

        if 1 < open_ratio < 1.06:
            qualified_stocks.append(
                {"stock": stock, "open_price": open_price, "open_ratio": open_ratio}
            )
            qualified_count += 1

    except:
        continue

print(f"\n符合弱转强条件: {qualified_count}")

if qualified_count > 0:
    print("\n符合条件股票:")
    for q in qualified_stocks:
        print(f"  {q['stock']}: 开盘比 {q['open_ratio']:.3f}")

    print("\n4. 模拟买入...")
    print(f"如果买入前{min(qualified_count, 3)}只股票:")
    for i, q in enumerate(qualified_stocks[:3], 1):
        print(f"  {i}. {q['stock']} @ {q['open_price']:.2f}")
else:
    print("\n警告: 没有符合弱转强条件的股票")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
