from jqdata import *
import pandas as pd

print("=" * 60)
print("主线策略简化版测试 - JoinQuant")
print("=" * 60)

test_dates = list(get_trade_days(end_date="2024-06-30", count=30))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-06-01"]

print(f"测试期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"交易日数: {len(test_dates)}")

trades = []

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    print(f"\n处理: {curr_date}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "6834"]

        print(f"  筛选前股票数: {len(all_stocks)}")

        limit_up_stocks = []

        for stock in all_stocks[:1000]:
            try:
                price = get_price(
                    stock,
                    end_date=prev_date,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                if price.empty:
                    continue

                close = float(price["close"].iloc[0])
                high_limit = float(price["high_limit"].iloc[0])

                if abs(close - high_limit) / high_limit < 0.01:
                    limit_up_stocks.append(stock)
            except:
                continue

        print(f"  涨停股票数: {len(limit_up_stocks)}")

        if not limit_up_stocks:
            print("  无涨停股票")
            continue

        candidates = []

        for stock in limit_up_stocks[:50]:
            try:
                price_curr = get_price(
                    stock,
                    end_date=curr_date,
                    count=1,
                    fields=["open", "close", "high"],
                    panel=False,
                )
                if price_curr.empty:
                    continue

                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code == stock
                )
                val = get_fundamentals(q, date=curr_date)
                if val.empty:
                    continue

                prev_close = float(
                    get_price(
                        stock,
                        end_date=prev_date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )["close"].iloc[0]
                )
                curr_open = float(price_curr["open"].iloc[0])
                curr_close = float(price_curr["close"].iloc[0])

                open_pct = (curr_open - prev_close) / prev_close * 100

                # 放宽条件：-2%~+3%
                if not (-2 <= open_pct <= 3):
                    continue

                market_cap = float(val["circulating_market_cap"].iloc[0])

                candidates.append(
                    {
                        "stock": stock,
                        "open_pct": open_pct,
                        "market_cap": market_cap,
                        "curr_open": curr_open,
                        "curr_close": curr_close,
                    }
                )
            except:
                continue

        print(f"  候选股票数: {len(candidates)}")

        if not candidates:
            print("  无候选股票")
            continue

        # 按市值排序
        candidates.sort(key=lambda x: x["market_cap"])

        # 买入前3个
        for j, cand in enumerate(candidates[:3]):
            intra_return = (
                (cand["curr_close"] - cand["curr_open"]) / cand["curr_open"] * 100
            )
            trades.append(
                {
                    "date": curr_date,
                    "stock": cand["stock"],
                    "open_pct": cand["open_pct"],
                    "market_cap": cand["market_cap"],
                    "intra_return": intra_return,
                }
            )
            print(
                f"  买入{j + 1}: {cand['stock']}, 开盘{cand['open_pct']:.2f}%, "
                f"市值{cand['market_cap']:.1f}亿, 日内收益{intra_return:.2f}%"
            )

    except Exception as e:
        print(f"  错误: {e}")
        continue

print("\n" + "=" * 60)
print("交易汇总")
print("=" * 60)

if len(trades) == 0:
    print("无交易")
else:
    df = pd.DataFrame(trades)

    print(f"\n总交易数: {len(df)}")
    print(f"平均日内收益: {df['intra_return'].mean():.2f}%")
    print(f"胜率: {(df['intra_return'] > 0).sum() / len(df) * 100:.1f}%")
    print(f"平均市值: {df['market_cap'].mean():.1f}亿")

    print("\n交易明细:")
    print(df.to_string(index=False))

print("\n测试完成！")
