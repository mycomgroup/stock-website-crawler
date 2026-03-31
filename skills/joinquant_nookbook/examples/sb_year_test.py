from jqdata import *
import numpy as np

print("二板2021-2023逐年实测")
print("=" * 60)

results = {}

for year in [2021, 2022, 2023]:
    print(f"\n{year}年")
    trades = []

    # 测试每个月份的前5个交易日
    for month in range(1, 13):
        dates = get_trade_days(f"{year}-{month:02d}-01", f"{year}-{month:02d}-28")[:6]

        for i in range(2, len(dates) - 1):
            d = dates[i]

            try:
                stocks = [
                    s
                    for s in get_all_securities("stock", d).index
                    if not s.startswith(("68", "4", "8"))
                ][:300]

                df = get_price(
                    stocks,
                    end_date=d,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                df = df.dropna()
                zt = df[df["close"] == df["high_limit"]]
                zt_count = len(zt)

                if zt_count < 10:
                    continue

                zt_list = zt["code"].tolist()

                df1 = get_price(
                    stocks,
                    end_date=dates[i - 1],
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                df1 = df1.dropna()
                zt1 = df1[df1["close"] == df1["high_limit"]]["code"].tolist()

                df2 = get_price(
                    stocks,
                    end_date=dates[i - 2],
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                df2 = df2.dropna()
                zt2 = df2[df2["close"] == df2["high_limit"]]["code"].tolist()

                sb = list(set(zt_list) & set(zt1) - set(zt2))

                if len(sb) == 0:
                    continue

                for s in sb[:3]:
                    try:
                        v = get_price(
                            s, end_date=d, count=2, fields=["volume"], panel=False
                        )
                        if v["volume"].iloc[-1] / v["volume"].iloc[-2] > 1.875:
                            continue

                        c = get_fundamentals(
                            query(valuation.circulating_market_cap).filter(
                                valuation.code == s
                            ),
                            d,
                        )
                        if len(c) == 0:
                            continue

                        p = get_price(
                            s,
                            end_date=dates[i + 1],
                            count=1,
                            fields=["open", "close", "high_limit"],
                            panel=False,
                        )
                        if p["open"].iloc[0] >= p["high_limit"].iloc[0] * 0.99:
                            continue

                        buy = p["open"].iloc[0] * 1.005
                        profit = (p["close"].iloc[0] / buy - 1) * 100
                        trades.append(profit)
                        break
                    except:
                        pass
            except:
                pass

    if trades:
        wins = len([p for p in trades if p > 0])
        results[year] = {
            "trades": len(trades),
            "wins": wins,
            "win_rate": wins / len(trades) * 100,
            "total": sum(trades),
            "avg": np.mean(trades),
        }
        print(
            f"  {len(trades)}笔, 胜率{wins / len(trades) * 100:.1f}%, 收益{sum(trades):.1f}%"
        )
    else:
        results[year] = {"trades": 0}
        print(f"  无交易")

print("\n汇总:")
for y in [2021, 2022, 2023]:
    r = results.get(y, {})
    if r.get("trades", 0) > 0:
        print(
            f"{y}: {r['trades']}笔, 胜率{r['win_rate']:.1f}%, 总收益{r['total']:.1f}%"
        )
    else:
        print(f"{y}: 无交易")
