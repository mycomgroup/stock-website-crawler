from jqdata import *

print("二板2023年1月快速测试")

dates = get_trade_days("2023-01-01", "2023-01-31")
print(f"交易日: {len(dates)}")

trades = []
for i in range(2, len(dates) - 1):
    d = dates[i]
    print(f"{d}...")

    stocks = [
        s
        for s in get_all_securities("stock", d).index[:500]
        if not s.startswith(("68", "4", "8"))
    ]

    def is_zt(s, day):
        try:
            p = get_price(s, end_date=day, count=1, fields=["close", "high_limit"])
            return len(p) > 0 and p["close"].iloc[0] >= p["high_limit"].iloc[0] * 0.99
        except:
            return False

    zt1 = [s for s in stocks if is_zt(s, d)]
    zt2 = [s for s in stocks if is_zt(s, dates[i - 1])]
    zt3 = [s for s in stocks if is_zt(s, dates[i - 2])]

    sb = list(set(zt1) & set(zt2) - set(zt3))[:3]

    for stock in sb:
        try:
            v = get_price(stock, end_date=d, count=2, fields=["volume"])
            if v["volume"].iloc[-1] / v["volume"].iloc[-2] > 1.875:
                continue

            p = get_price(
                stock,
                end_date=dates[i + 1],
                count=1,
                fields=["open", "close", "high_limit"],
            )
            if p["open"].iloc[0] >= p["high_limit"].iloc[0] * 0.99:
                continue

            buy = p["open"].iloc[0] * 1.005
            profit = (p["close"].iloc[0] / buy - 1) * 100
            trades.append(profit)
            print(f"  买入{stock}, 收益{profit:.2f}%")
            break
        except:
            pass

print(f"\n结果: {len(trades)}笔交易")
if trades:
    wins = len([p for p in trades if p > 0])
    print(f"胜率: {wins / len(trades) * 100:.1f}%")
    print(f"总收益: {sum(trades):.2f}%")
