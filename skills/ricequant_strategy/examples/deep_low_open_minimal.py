# 深度低开专项验证 - RiceQuant Notebook版本
# 深度低开：-5%~-3%

print("=== 深度低开专项验证开始 ===")

try:
    import pandas as pd
    import numpy as np

    # 测试2024年1月和7月数据
    test_dates = ["2024-01-15", "2024-07-15"]

    signals = []

    for test_date in test_dates:
        print(f"\n处理日期: {test_date}")

        # 获取所有股票
        all_stocks = all_instruments("CS", test_date)
        print(f"  股票总数: {len(all_stocks)}")

        # 获取前300只股票的价格数据
        stocks_sample = all_stocks["order_book_id"].tolist()[:300]

        for stock in stocks_sample:
            try:
                # 获取前一日和当日数据
                bars = history_bars(
                    stock, 2, "1d", "close,limit_up", end_date=test_date
                )

                if bars is None or len(bars) < 2:
                    continue

                prev_close = bars[-2]["close"]
                prev_limit = bars[-2]["limit_up"]
                curr_open = bars[-1]["close"]  # RiceQuant history_bars返回的是收盘价

                # 检查昨日是否涨停
                if abs(prev_close - prev_limit) / prev_limit > 0.01:
                    continue

                # 计算开盘涨跌幅
                open_pct = (curr_open - prev_close) / prev_close * 100

                # 筛选深度低开：-5%~-3%
                if -5.0 <= open_pct < -3.0:
                    # 获取当日收盘价和最高价
                    daily_bars = history_bars(
                        stock, 1, "1d", "close,high", end_date=test_date
                    )
                    if daily_bars is not None and len(daily_bars) > 0:
                        curr_close = daily_bars[-1]["close"]
                        curr_high = daily_bars[-1]["high"]

                        intra_return = (curr_close - curr_open) / curr_open * 100
                        max_return = (curr_high - curr_open) / curr_open * 100

                        signals.append(
                            {
                                "date": test_date,
                                "stock": stock,
                                "open_pct": open_pct,
                                "intra_return": intra_return,
                                "max_return": max_return,
                                "is_win": intra_return > 0,
                            }
                        )

            except Exception as e:
                continue

    print("\n" + "=" * 80)
    print("结果汇总")
    print("=" * 80)

    if len(signals) == 0:
        print("未找到深度低开样本")
    else:
        df = pd.DataFrame(signals)
        print(f"\n深度低开样本数: {len(df)}")
        print(f"平均日内收益: {df['intra_return'].mean():.2f}%")
        print(f"胜率: {df['is_win'].sum() / len(df) * 100:.1f}%")
        print(
            f"开盘涨跌幅范围: {df['open_pct'].min():.2f}% ~ {df['open_pct'].max():.2f}%"
        )
        print(f"\n详细数据:")
        for idx, row in df.iterrows():
            print(
                f"  {row['date']} {row['stock']}: 开盘{row['open_pct']:.2f}%, 日内{row['intra_return']:.2f}%"
            )

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 测试完成 ===")
