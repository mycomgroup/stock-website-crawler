from jqdata import *
import numpy as np

print("=" * 60)
print("二板策略快速验证（仅测试2023年Q1）")
print("=" * 60)

year = 2023
trade_days = get_trade_days(f"{year}-01-01", f"{year}-03-31")
print(f"测试期间: 2023-Q1, 共{len(trade_days)}个交易日")

trades, wins, profits = 0, 0, []

for i in range(2, len(trade_days) - 1):
    date, next_date = trade_days[i], trade_days[i + 1]
    prev1, prev2 = trade_days[i - 1], trade_days[i - 2]

    if i % 10 == 0:
        print(f"处理 {date} ({i}/{len(trade_days)})...")

    try:
        stocks = get_all_securities("stock", date).index.tolist()
        stocks = [s for s in stocks[:800] if not s.startswith(("68", "4", "8"))]

        def is_zt(s, d):
            try:
                df = get_price(
                    s, end_date=d, count=1, fields=["close", "high_limit"], panel=False
                )
                return len(df) > 0 and df.iloc[0]["close"] == df.iloc[0]["high_limit"]
            except:
                return False

        zt1 = [s for s in stocks if is_zt(s, date)]
        zt2 = [s for s in stocks if is_zt(s, prev1)]
        zt3 = [s for s in stocks if is_zt(s, prev2)]

        sb = list(set(zt1) & set(zt2) - set(zt3))[:5]

        for stock in sb:
            try:
                vol = get_price(
                    stock, end_date=date, count=2, fields=["volume"], panel=False
                )
                if (
                    len(vol) >= 2
                    and vol.iloc[-1]["volume"] / vol.iloc[-2]["volume"] > 1.875
                ):
                    continue

                cap = get_fundamentals(
                    query(valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    ),
                    date,
                )
                if len(cap) == 0:
                    continue

                next_df = get_price(
                    stock,
                    end_date=next_date,
                    count=1,
                    fields=["open", "close", "high_limit"],
                    panel=False,
                )
                if len(next_df) == 0:
                    continue

                if next_df.iloc[0]["open"] >= next_df.iloc[0]["high_limit"] * 0.99:
                    continue

                buy = next_df.iloc[0]["open"] * 1.005
                profit = (next_df.iloc[0]["close"] / buy - 1) * 100
                trades += 1
                profits.append(profit)
                if profit > 0:
                    wins += 1
                break
            except:
                pass
    except:
        pass

print(
    f"\n结果: 交易{trades}次, 胜率{wins / trades * 100:.1f}%, 平均收益{np.mean(profits):.2f}%"
)
print("=" * 60)
