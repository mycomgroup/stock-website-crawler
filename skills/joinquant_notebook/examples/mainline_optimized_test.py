from jqdata import *
import pandas as pd

print("=" * 60)
print("主线策略优化版 - 排除一字板 + 市值筛选")
print("=" * 60)

test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-01-01"]

print(f"测试期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"交易日数: {len(test_dates)}")

trades = []

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    if i % 20 == 0:
        print(f"进度: {i}/{len(test_dates)}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "6834"]

        limit_up_stocks = []

        for stock in all_stocks[:2000]:
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

        if not limit_up_stocks:
            continue

        candidates = []

        for stock in limit_up_stocks[:100]:
            try:
                price_curr = get_price(
                    stock,
                    end_date=curr_date,
                    count=1,
                    fields=["open", "close", "high", "low"],
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

                market_cap = float(val["circulating_market_cap"].iloc[0])

                # 市值筛选：50-150亿
                if not (50 <= market_cap <= 150):
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
                curr_high = float(price_curr["high"].iloc[0])
                curr_low = float(price_curr["low"].iloc[0])

                open_pct = (curr_open - prev_close) / prev_close * 100

                # 排除一字板：开盘价!=最高价且开盘价!=最低价
                if curr_open == curr_high or curr_open == curr_low:
                    continue

                # 假弱高开：+0.5%~+1.5%
                if not (0.5 <= open_pct <= 1.5):
                    continue

                intra_return = (curr_close - curr_open) / curr_open * 100
                max_return = (curr_high - curr_open) / curr_open * 100

                candidates.append(
                    {
                        "stock": stock,
                        "open_pct": open_pct,
                        "market_cap": market_cap,
                        "intra_return": intra_return,
                        "max_return": max_return,
                    }
                )
            except:
                continue

        if not candidates:
            continue

        # 按开盘涨幅排序，选最接近1%的
        candidates.sort(key=lambda x: abs(x["open_pct"] - 1.0))

        # 买入前3个
        for j, cand in enumerate(candidates[:3]):
            trades.append(
                {
                    "date": curr_date,
                    "stock": cand["stock"],
                    "open_pct": cand["open_pct"],
                    "market_cap": cand["market_cap"],
                    "intra_return": cand["intra_return"],
                    "max_return": cand["max_return"],
                }
            )

    except Exception as e:
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
    print(f"平均最高收益: {df['max_return'].mean():.2f}%")
    print(f"胜率: {(df['intra_return'] > 0).sum() / len(df) * 100:.1f}%")
    print(f"平均市值: {df['market_cap'].mean():.1f}亿")
    print(f"平均开盘涨幅: {df['open_pct'].mean():.2f}%")

    print("\n前10笔交易:")
    print(df.head(10).to_string(index=False))

print("\n测试完成！")
