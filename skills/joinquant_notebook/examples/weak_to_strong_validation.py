#!/usr/bin/env python3
"""弱转强竞价 - 极简验证版 V2"""

print("=" * 60)
print("弱转强竞价策略 - 2024年验证 V2")
print("=" * 60)

from jqdata import *
import pandas as pd

START_DATE = "2024-01-01"
END_DATE = "2024-06-30"

trade_days = get_trade_days(start_date=START_DATE, end_date=END_DATE)
print(f"\n【1】交易日: {len(trade_days)} 天")


def filter_stocks(date_str):
    all_stocks = get_all_securities("stock", date_str).index.tolist()
    stocks = [s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"]
    filtered = []
    for s in stocks:
        try:
            if (pd.Timestamp(date_str) - get_security_info(s).start_date).days > 50:
                filtered.append(s)
        except:
            pass
    return filtered


signal_count = 0
total_days = 0

for i in range(1, len(trade_days)):
    prev_day = trade_days[i - 1]
    prev_str = prev_day.strftime("%Y-%m-%d")

    try:
        stocks = filter_stocks(prev_str)
        if len(stocks) == 0:
            continue

        prices = get_price(
            stocks,
            end_date=prev_str,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if prices.empty:
            continue
        prices = prices.dropna()
        hl_stocks = list(prices[prices["close"] == prices["high_limit"]]["code"])

        if len(hl_stocks) == 0:
            continue

        prev_prices = get_price(
            hl_stocks,
            end_date=prev_str,
            frequency="daily",
            fields=["money"],
            count=1,
            panel=False,
        )
        if prev_prices.empty:
            continue
        prev_prices = prev_prices.dropna()
        qualified = list(prev_prices[prev_prices["money"] > 5e8].index)

        signal_count += len(qualified)
        total_days += 1

    except Exception as e:
        continue

print(f"\n【2】信号统计:")
print(f"  有效交易日: {total_days}")
print(f"  总信号数: {signal_count}")
avg = signal_count / total_days if total_days > 0 else 0
print(f"  日均信号: {avg:.1f}")

print("\n【3】结论:")
if avg >= 1:
    print(f"  信号充足，日均{avg:.1f}个信号，可执行回测")
else:
    print(f"  信号过少，日均仅{avg:.1f}个")

print("\n" + "=" * 60)
