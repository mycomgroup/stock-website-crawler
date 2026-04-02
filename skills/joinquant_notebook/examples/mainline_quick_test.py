from jqdata import *
import pandas as pd

print("=" * 60)
print("主线策略快速验证版（采样测试）")
print("=" * 60)

# 采样测试：每周测1天
test_dates_all = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates_all = [str(d) for d in test_dates_all if str(d) >= "2024-01-01"]
test_dates = test_dates_all[::5]  # 每5个交易日取1个

print(f"测试期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"采样日数: {len(test_dates)}")

trades = []

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    print(f"\n处理: {curr_date}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "6834"]

        # 采样前500只股票
        sample_stocks = all_stocks[:500]

        limit_up_stocks = []

        for stock in sample_stocks:
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

        print(f"  涨停股票: {len(limit_up_stocks)}")

        if not limit_up_stocks:
            continue

        candidates = []

        for stock in limit_up_stocks:
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

                # 排除一字板
                if curr_open == curr_high or curr_open == curr_low:
                    continue

                # 假弱高开：+0.5%~+1.5%
                if not (0.5 <= open_pct <= 1.5):
                    continue

                intra_return = (curr_close - curr_open) / curr_open * 100

                candidates.append(
                    {
                        "stock": stock,
                        "open_pct": open_pct,
                        "market_cap": market_cap,
                        "intra_return": intra_return,
                    }
                )
            except:
                continue

        print(f"  候选股票: {len(candidates)}")

        if not candidates:
            continue

        for cand in candidates[:3]:
            trades.append(cand)
            print(
                f"  买入: {cand['stock']}, 开盘{cand['open_pct']:.2f}%, "
                f"市值{cand['market_cap']:.1f}亿, 收益{cand['intra_return']:.2f}%"
            )

    except Exception as e:
        print(f"  错误: {e}")
        continue

print("\n" + "=" * 60)
print("最终结果")
print("=" * 60)

if len(trades) == 0:
    print("无交易")
else:
    df = pd.DataFrame(trades)

    print(f"\n总交易数: {len(df)}")
    print(f"平均日内收益: {df['intra_return'].mean():.2f}%")
    print(f"胜率: {(df['intra_return'] > 0).sum() / len(df) * 100:.1f}%")
    print(f"平均市值: {df['market_cap'].mean():.1f}亿")

print("\n完成！")
