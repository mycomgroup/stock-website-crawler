"""
二板接力 2022年Q2测试 - RiceQuant Notebook格式
测试范围：2022-04-01 至 2022-06-30
"""

print("=" * 80)
print("二板接力 2022年Q2测试")
print("=" * 80)

try:
    import pandas as pd
    import numpy as np

    print("✓ 导入依赖成功")

    year = 2022
    start_date = f"{year}-04-01"
    end_date = f"{year}-06-30"

    print(f"\n测试范围: {start_date} 至 {end_date}")

    all_dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(all_dates)}")

    signals = []

    for i in range(2, min(len(all_dates), 50)):
        prev_prev = all_dates[i - 2]
        prev = all_dates[i - 1]
        curr = all_dates[i]

        if i % 5 == 0:
            print(f"处理第{i}天: {prev} -> {curr}")

        try:
            all_stocks = [s for s in get_all_securities(["stock"]).index.tolist()]
            all_stocks = [
                s
                for s in all_stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            if len(all_stocks) > 500:
                all_stocks = all_stocks[:500]

            price_prev = get_price(
                all_stocks,
                end_date=prev,
                frequency="1d",
                fields=["close", "limit_up"],
                count=1,
            )

            if price_prev.empty:
                continue

            zt_stocks = []
            for stock in all_stocks:
                try:
                    close = price_prev.loc[prev, (stock, "close")]
                    limit_up = price_prev.loc[prev, (stock, "limit_up")]
                    if abs(close - limit_up) / limit_up < 0.01:
                        zt_stocks.append(stock)
                except:
                    continue

            zt_count = len(zt_stocks)
            if i % 5 == 0:
                print(f"  涨停数: {zt_count}")

            if zt_count < 10:
                continue

            price_pp = get_price(
                zt_stocks,
                end_date=prev_prev,
                frequency="1d",
                fields=["close", "limit_up"],
                count=1,
            )

            if price_pp.empty:
                continue

            for stock in zt_stocks[:30]:
                try:
                    pp_close = price_pp.loc[prev_prev, (stock, "close")]
                    pp_limit = price_pp.loc[prev_prev, (stock, "limit_up")]

                    if abs(pp_close - pp_limit) / pp_limit >= 0.01:
                        continue

                    price_curr = get_price(
                        stock,
                        end_date=curr,
                        frequency="1d",
                        fields=["open", "close", "limit_up"],
                        count=1,
                    )

                    if price_curr.empty:
                        continue

                    curr_open = price_curr.loc[curr, "open"]
                    curr_close = price_curr.loc[curr, "close"]
                    curr_limit = price_curr.loc[curr, "limit_up"]

                    if abs(curr_open - curr_limit) / curr_limit < 0.01:
                        continue

                    ret = (curr_close - curr_open) / curr_open * 100
                    signals.append(
                        {
                            "date": str(curr),
                            "stock": stock,
                            "return": ret,
                            "win": ret > 0,
                        }
                    )

                except:
                    continue
        except:
            continue

    print("\n" + "=" * 80)
    print("2022年Q2测试结果")
    print("=" * 80)

    if len(signals) > 0:
        df = pd.DataFrame(signals)
        print(f"信号数: {len(df)}")
        print(f"平均收益: {df['return'].mean():.2f}%")
        print(f"胜率: {df['win'].sum() / len(df) * 100:.1f}%")
    else:
        print("无信号")

    print("\n✓ 2022年Q2测试完成")

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback

    traceback.print_exc()

print("=" * 80)
