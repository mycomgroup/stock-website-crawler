from jqdata import *
import numpy as np

print("二板2021-2023快速验证")
print("=" * 60)

results = {}

for year in [2021, 2022, 2023]:
    print(f"\n测试{year}年...")

    trades = []
    dates = get_trade_days(f"{year}-01-01", f"{year}-12-31")

    for i in range(2, len(dates) - 1):
        d, d_next = dates[i], dates[i + 1]
        d_prev1, d_prev2 = dates[i - 1], dates[i - 2]

        if i % 30 == 0:
            print(f"  {d} ({i}/{len(dates)})")

        try:
            stocks = [
                s
                for s in get_all_securities("stock", d).index
                if not s.startswith(("68", "4", "8"))
            ]

            def zt(s, day):
                try:
                    p = get_price(
                        s, end_date=day, count=1, fields=["close", "high_limit"]
                    )
                    return len(p) > 0 and p["close"][0] >= p["high_limit"][0] * 0.99
                except:
                    return False

            zt1 = [s for s in stocks if zt(s, d)]
            zt2 = [s for s in stocks if zt(s, d_prev1)]
            zt3 = [s for s in stocks if zt(s, d_prev2)]

            sb = list(set(zt1) & set(zt2) - set(zt3))[:10]

            for stock in sb:
                try:
                    v = get_price(stock, end_date=d, count=2, fields=["volume"])
                    if len(v) >= 2 and v["volume"][-1] / v["volume"][-2] > 1.875:
                        continue

                    c = get_fundamentals(
                        query(valuation.circulating_market_cap).filter(
                            valuation.code == stock
                        ),
                        d,
                    )
                    if len(c) == 0:
                        continue

                    p = get_price(
                        stock,
                        end_date=d_next,
                        count=1,
                        fields=["open", "close", "high_limit"],
                    )
                    if len(p) == 0 or p["open"][0] >= p["high_limit"][0] * 0.99:
                        continue

                    buy = p["open"][0] * 1.005
                    profit = (p["close"][0] / buy - 1) * 100
                    trades.append(profit)
                    break
                except:
                    pass
        except:
            pass

    if trades:
        results[year] = {
            "count": len(trades),
            "win": len([p for p in trades if p > 0]),
            "profit": sum(trades),
            "avg": np.mean(trades),
        }
        print(
            f"{year}完成: {len(trades)}笔, 胜率{results[year]['win'] / len(trades) * 100:.1f}%, 收益{sum(trades):.1f}%"
        )
    else:
        results[year] = {"count": 0}
        print(f"{year}未完成")

print("\n" + "=" * 60)
print("汇总:")
for y in [2021, 2022, 2023]:
    r = results.get(y, {})
    if r.get("count", 0) > 0:
        print(
            f"{y}: {r['count']}笔, 胜率{r['win'] / r['count'] * 100:.1f}%, 总收益{r['profit']:.1f}%"
        )
    else:
        print(f"{y}: 未完成")

positive = len(
    [y for y in [2021, 2022, 2023] if results.get(y, {}).get("profit", 0) > 0]
)
print(f"\n正收益年份: {positive}/3")
print(f"判定: {'稳定' if positive >= 2 else '不稳定'}")
