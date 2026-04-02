#!/usr/bin/env python3
print("=" * 60)
print("弱转强竞价策略 - 2024年信号统计 v3")
print("=" * 60)

from jqdata import *
import pandas as pd

START_DATE = "2024-01-01"
END_DATE = "2024-06-30"

trade_days = get_trade_days(start_date=START_DATE, end_date=END_DATE)
print(f"\n【1】交易日: {len(trade_days)} 天")

signal_count = 0
valid_days = 0

# Use only first 30 days to test quickly
test_days = trade_days[:30]

for date in test_days:
    date_str = date.strftime("%Y-%m-%d")

    try:
        # Get all stocks
        all_stocks = get_all_securities("stock", date_str).index.tolist()
        stocks = [
            s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"
        ]

        # Get prices
        prices = get_price(
            stocks,
            end_date=date_str,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if prices.empty:
            continue

        prices = prices.dropna()

        # Find limit-up stocks - use "code" column
        prices["is_hl"] = prices["close"] == prices["high_limit"]
        hl = prices[prices["is_hl"]]

        if len(hl) == 0:
            continue

        # Get actual stock codes from 'code' column
        hl_codes = list(hl["code"])

        # Get money data - pass as list
        money = get_price(
            hl_codes,
            end_date=date_str,
            frequency="daily",
            fields=["money"],
            count=1,
            panel=False,
        )
        if money.empty:
            continue

        money = money.dropna()
        money["qualified"] = money["money"] > 5e8
        qualified = money[money["qualified"]]

        signal_count += len(qualified)
        valid_days += 1

        if len(qualified) > 0:
            print(f"  {date_str}: {len(qualified)} signals")

    except Exception as e:
        print(f"  Error {date_str}: {str(e)[:50]}")
        continue

avg = signal_count / valid_days if valid_days > 0 else 0

print(f"\n【2】信号统计(前30天):")
print(f"  有效交易日: {valid_days}")
print(f"  总信号数: {signal_count}")
print(f"  日均信号: {avg:.1f}")

print("\n【3】结论:")
if avg >= 1:
    print(f"  ✓ 信号充足，日均{avg:.1f}个，可执行回测")
elif avg > 0:
    print(f"  ⚠ 信号较少，日均{avg:.1f}个")
else:
    print(f"  ✗ 无任何信号")

print("\n" + "=" * 60)
