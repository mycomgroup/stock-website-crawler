#!/usr/bin/env python3
from jqdata import *

print("测试开始")

days = get_trade_days("2025-03-01", "2025-03-30")
print(f"交易日: {len(days)}")

for d in days[-5:]:
    ds = d.strftime("%Y-%m-%d")
    stocks = get_all_securities("stock", ds).index.tolist()[:100]
    df = get_price(
        stocks, end_date=ds, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    zt = len(df[df["close"] == df["high_limit"]])
    print(f"{ds}: 涨停={zt}")

print("完成")
