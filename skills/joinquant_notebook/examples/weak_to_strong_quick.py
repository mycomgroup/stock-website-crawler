#!/usr/bin/env python3
print("Quick test - just 5 days")
from jqdata import *

dates = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"]

for d in dates:
    stocks = get_all_securities("stock", d).index.tolist()
    stocks = [s for s in stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"]

    prices = get_price(
        stocks,
        end_date=d,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    if prices.empty:
        print(f"{d}: no price data")
        continue

    prices = prices.dropna()
    prices["is_hl"] = prices["close"] == prices["high_limit"]
    hl = prices[prices["is_hl"]]
    hl_codes = list(hl["code"])

    if len(hl_codes) > 0:
        money = get_price(
            hl_codes,
            end_date=d,
            frequency="daily",
            fields=["money"],
            count=1,
            panel=False,
        )
        money = money.dropna()
        q = money[money["money"] > 5e8]
        print(f"{d}: HL={len(hl_codes)}, qualified={len(q)}")
    else:
        print(f"{d}: HL=0")

print("Done!")
