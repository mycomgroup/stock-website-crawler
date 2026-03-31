from jqdata import *

print("二板统计测试")

dates = get_trade_days("2023-03-01", "2023-03-10")
print(f"测试日期: {len(dates)}")

for d in dates:
    print(f"\n{d}")

    stocks = [
        s
        for s in get_all_securities("stock", d).index
        if not s.startswith(("68", "4", "8"))
    ][:200]

    df = get_price(
        stocks, end_date=d, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    zt = len(df[df["close"] == df["high_limit"]])
    print(f"涨停: {zt}")

print("\n完成")
