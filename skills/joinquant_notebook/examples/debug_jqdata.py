#!/usr/bin/env python3
print("Test 1: get_all_securities")
from jqdata import *

stocks = get_all_securities("stock", "2024-01-01")
print(f"Total stocks: {len(stocks)}")

if len(stocks) > 0:
    print(f"First stock: {stocks.index[0]}")

print("\nTest 2: get_trade_days")
td = get_trade_days(start_date="2024-01-01", end_date="2024-01-10")
print(f"Trade days: {len(td)}")
print(td[:3])

print("\nTest 3: get_price on single stock")
p = get_price(
    "000001.XSHE",
    end_date="2024-01-02",
    frequency="daily",
    fields=["close", "high_limit"],
    count=1,
)
print(p)
