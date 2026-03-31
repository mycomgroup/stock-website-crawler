from jqdata import *
import numpy as np

print("2022年4月二板实测")
print("=" * 60)

dates = get_trade_days("2022-04-01", "2022-04-30")
print(f"交易日: {len(dates)}")

trades = []

for i in range(2, len(dates) - 1):
    d = dates[i]
    print(f"\n{d}")

    try:
        stocks = [
            s
            for s in get_all_securities("stock", d).index
            if not s.startswith(("68", "4", "8"))
        ][:500]

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

        for s in sb[:5]:
            try:
                v = get_price(s, end_date=d, count=2, fields=["volume"], panel=False)
                if v["volume"].iloc[-1] / v["volume"].iloc[-2] > 1.875:
                    continue

                c = get_fundamentals(
                    query(valuation.circulating_market_cap).filter(valuation.code == s),
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
                if len(p) == 0 or p["open"].iloc[0] >= p["high_limit"].iloc[0] * 0.99:
                    continue

                buy = p["open"].iloc[0] * 1.005
                profit = (p["close"].iloc[0] / buy - 1) * 100
                trades.append(profit)
                print(f"  交易{len(trades)}: {s} 收益{profit:.2f}%")
                break
            except:
                pass
    except:
        pass

print("\n" + "=" * 60)
print(f"结果: {len(trades)}笔交易")
if trades:
    wins = len([p for p in trades if p > 0])
    print(f"胜率: {wins / len(trades) * 100:.1f}%")
    print(f"总收益: {sum(trades):.2f}%")
    print(f"平均收益: {np.mean(trades):.2f}%")
