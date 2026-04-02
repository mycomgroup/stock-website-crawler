#!/usr/bin/env python3
print("Debug panel=False index")
from jqdata import *
import pandas as pd

date = "2024-01-03"

all_stocks = get_all_securities("stock", date).index.tolist()
stocks = [s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"]

prices = get_price(
    stocks,
    end_date=date,
    frequency="daily",
    fields=["close", "high_limit"],
    count=1,
    panel=False,
)

print(f"Prices type: {type(prices)}")
print(f"Prices index type: {type(prices.index)}")
print(f"Prices head:\n{prices.head()}")

if not prices.empty:
    prices = prices.dropna()
    prices["code"] = prices.index  # Save code
    hl = prices[prices["close"] == prices["high_limit"]]
    print(f"\nLimit-up stocks: {len(hl)}")
    print(f"HL index sample: {list(hl.index[:5])}")
    print(f"HL codes sample: {list(hl['code'].head())}")
