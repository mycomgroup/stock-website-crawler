"""
二板接力 2025年Q1测试 - RiceQuant正确API版本
测试范围：2025-01-01 至 2025-03-30
"""

print("=" * 80)
print("二板接力 2025年Q1测试")
print("=" * 80)

try:
    import pandas as pd
    import numpy as np

    print("✓ 导入依赖成功")

    start_date = "2025-01-01"
    end_date = "2025-03-30"

    print(f"\n测试范围: {start_date} 至 {end_date}")

    all_dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(all_dates)}")

    stocks_df = all_instruments("CS")
    all_stocks_list = stocks_df["order_book_id"].tolist()
    all_stocks_list = [
        s
        for s in all_stocks_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    all_stocks_list = all_stocks_list[:300]
    print(f"测试股票数: {len(all_stocks_list)}")

    signals = []

    for i in range(2, len(all_dates)):
        prev_prev = all_dates[i - 2]
        prev = all_dates[i - 1]
        curr = all_dates[i]

        if i % 5 == 0:
            print(f"处理第{i}天: {prev} -> {curr}")

        try:
            price_data = get_price(
                all_stocks_list,
                start_date=prev_prev,
                end_date=curr,
                frequency="1d",
                fields=["close", "limit_up", "open"],
            )

            if price_data.empty:
                continue

            zt_stocks = []
            for stock in all_stocks_list:
                try:
                    prev_close = price_data.loc[prev, (stock, "close")]
                    prev_limit = price_data.loc[prev, (stock, "limit_up")]

                    if abs(prev_close - prev_limit) / prev_limit < 0.01:
                        pp_close = price_data.loc[prev_prev, (stock, "close")]
                        pp_limit = price_data.loc[prev_prev, (stock, "limit_up")]

                        if abs(pp_close - pp_limit) / pp_limit < 0.01:
                            zt_stocks.append(stock)
                except:
                    continue

            if i % 5 == 0:
                print(f"  二板候选数: {len(zt_stocks)}")

            for stock in zt_stocks[:20]:
                try:
                    curr_open = price_data.loc[curr, (stock, "open")]
                    curr_close = price_data.loc[curr, (stock, "close")]
                    curr_limit = price_data.loc[curr, (stock, "limit_up")]

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
        except Exception as e:
            if i % 5 == 0:
                print(f"  错误: {e}")
            continue

    print("\n" + "=" * 80)
    print("2025年Q1测试结果")
    print("=" * 80)

    if len(signals) > 0:
        df = pd.DataFrame(signals)
        print(f"信号数: {len(df)}")
        print(f"平均收益: {df['return'].mean():.2f}%")
        print(f"胜率: {df['win'].sum() / len(df) * 100:.1f}%")
        print(f"最大收益: {df['return'].max():.2f}%")
        print(f"最大亏损: {df['return'].min():.2f}%")
    else:
        print("无信号")

    print("\n✓ 2025年Q1测试完成")

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback

    traceback.print_exc()

print("=" * 80)
