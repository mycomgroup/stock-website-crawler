# 最小化测试 - 2025年12月到2026年3月
from jqdata import *

print("龙头底分型最小测试")

days = get_trade_days("2025-12-01", "2026-03-20")[-10:]
print(f"测试天数: {len(days)}")

signals = 0

for d in days:
    ds = d.strftime("%Y-%m-%d")
    stocks = get_all_securities("stock", ds).index.tolist()[:100]

    for s in stocks:
        try:
            df = get_price(
                s, end_date=ds, count=5, fields=["close", "high_limit"], panel=False
            )
            if len(df) > 0 and df["close"].iloc[-1] == df["high_limit"].iloc[-1]:
                signals += 1
        except:
            pass

    print(f"{ds}: 涨停数={signals}")

print(f"\n总涨停数: {signals}")
