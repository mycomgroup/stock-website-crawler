from jqdata import *
import numpy as np

print("二板2024年快速验证")
print("=" * 60)

dates = get_trade_days("2024-01-01", "2024-12-31")
print(f"交易日: {len(dates)}")

trades = []
zt_counts = []

for i in range(2, len(dates) - 1):
    d = dates[i]

    if i % 50 == 0:
        print(f"{d} ({i}/{len(dates)})")

    try:
        stocks = [
            s
            for s in get_all_securities("stock", d).index
            if not s.startswith(("68", "4", "8"))
        ]

        df = get_price(
            stocks[:800],
            end_date=d,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        df = df.dropna()
        zt = df[df["close"] == df["high_limit"]]
        zt_count = len(zt)
        zt_counts.append(zt_count)

        if zt_count < 10:
            continue

        zt_stocks = list(zt["code"])

        prev_df = get_price(
            stocks[:800],
            end_date=dates[i - 1],
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        prev_df = prev_df.dropna()
        prev_zt = list(prev_df[prev_df["close"] == prev_df["high_limit"]]["code"])

        prev2_df = get_price(
            stocks[:800],
            end_date=dates[i - 2],
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        prev2_df = prev2_df.dropna()
        prev2_zt = list(prev2_df[prev2_df["close"] == prev2_df["high_limit"]]["code"])

        sb = list(set(zt_stocks) & set(prev_zt) - set(prev2_zt))

        if len(sb) == 0:
            continue

        for stock in sb[:5]:
            try:
                v = get_price(
                    stock, end_date=d, count=2, fields=["volume"], panel=False
                )
                if v["volume"].iloc[-1] / v["volume"].iloc[-2] > 1.875:
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
                break
            except:
                pass
    except:
        pass

print(f"\n结果: {len(trades)}笔交易")
print(f"平均涨停家数: {np.mean(zt_counts):.1f}")
if trades:
    wins = len([p for p in trades if p > 0])
    print(f"胜率: {wins / len(trades) * 100:.1f}%")
    print(f"总收益: {sum(trades):.1f}%")
    print(f"平均收益: {np.mean(trades):.2f}%")
