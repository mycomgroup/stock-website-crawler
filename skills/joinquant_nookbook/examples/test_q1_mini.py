from jqdata import *

print("二板2023年Q1实测")

dates = get_trade_days("2023-01-01", "2023-03-31")
print(f"Q1交易日: {len(dates)}")

trades = 0
wins = 0
profits = 0

for i in range(2, min(10, len(dates) - 1)):
    d = dates[i]
    print(f"\n{d}")

    stocks = get_all_securities("stock", d).index.tolist()
    stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))][:300]

    df = get_price(
        stocks, end_date=d, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    zt = df[df["close"] == df["high_limit"]]
    zt_count = len(zt)
    print(f"涨停: {zt_count}")

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
    print(f"二板: {len(sb)}")

    if len(sb) == 0:
        continue

    for s in sb[:3]:
        try:
            v = get_price(s, end_date=d, count=2, fields=["volume"], panel=False)
            if v["volume"].iloc[-1] / v["volume"].iloc[-2] > 1.875:
                continue

            c = get_fundamentals(
                query(valuation.circulating_market_cap).filter(valuation.code == s), d
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
            trades += 1
            profits += profit
            if profit > 0:
                wins += 1
            print(f"  交易{trades}: {s} 收益{profit:.2f}%")
            break
        except:
            pass

print(
    f"\n完成: {trades}笔, 胜率{wins / trades * 100 if trades else 0:.1f}%, 收益{profits:.2f}%"
)
