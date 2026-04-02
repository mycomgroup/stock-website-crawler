#!/usr/bin/env python3
print("Step by step debug")
from jqdata import *
import pandas as pd

date = "2024-01-03"

# Step 1: Get all stocks
all_stocks = get_all_securities("stock", date)
print(f"1. All stocks: {len(all_stocks)}")

# Step 2: Filter by code prefix
stocks = [s for s in all_stocks.index if s[0] not in ["4", "8", "3"] and s[:2] != "68"]
print(f"2. After filter: {len(stocks)}")

# Step 3: Get yesterday's limit-up stocks
prices = get_price(
    stocks,
    end_date=date,
    frequency="daily",
    fields=["close", "high_limit"],
    count=1,
    panel=False,
)
print(f"3. Prices shape: {prices.shape if not prices.empty else 'empty'}")

if not prices.empty:
    prices = prices.dropna()
    hl = prices[prices["close"] == prices["high_limit"]]
    print(f"4. Limit-up stocks: {len(hl)}")
    if len(hl) > 0:
        print(f"   Sample: {list(hl.index[:5])}")

        # Step 4: Get money for limit-up stocks
        money = get_price(
            list(hl.index),
            end_date=date,
            frequency="daily",
            fields=["money"],
            count=1,
            panel=False,
        )
        if not money.empty:
            money = money.dropna()
            qualified = money[money["money"] > 5e8]
            print(f"5. Qualified (>5e8): {len(qualified)}")
            if len(qualified) > 0:
                print(f"   Sample: {list(qualified.index[:3])}")
