# 深度低开专项验证 - RiceQuant Notebook（修正版）
# 使用与JoinQuant相同的测试日期

print("=== 深度低开专项验证 - RiceQuant Notebook ===")
print("阶段2：与JoinQuant对比验证")

try:
    import pandas as pd
    import numpy as np

    # 使用与JoinQuant相同的测试日期
    test_dates = ["2024-03-01", "2024-11-01"]

    signals = []

    for test_date in test_dates:
        print(f"\n处理日期: {test_date}")

        try:
            # 获取所有股票
            all_stocks = all_instruments("CS", test_date)
            print(f"  股票总数: {len(all_stocks)}")

            # 测试前500只股票（增加样本）
            stocks_sample = all_stocks["order_book_id"].tolist()[:500]

            limit_stocks_count = 0

            for stock in stocks_sample:
                try:
                    # 获取前2日数据
                    bars = history_bars(
                        stock, 2, "1d", "close,limit_up", end_date=test_date
                    )

                    if bars is None or len(bars) < 2:
                        continue

                    prev_close = bars[-2]["close"]
                    prev_limit = bars[-2]["limit_up"]

                    # 检查昨日是否涨停
                    if abs(prev_close - prev_limit) / prev_limit < 0.01:
                        limit_stocks_count += 1

                        # 获取当日数据（包括开盘价）
                        daily_bars = history_bars(
                            stock, 1, "1d", "open,close,high", end_date=test_date
                        )

                        if daily_bars is None or len(daily_bars) < 1:
                            continue

                        curr_open = daily_bars[-1]["open"]
                        curr_close = daily_bars[-1]["close"]
                        curr_high = daily_bars[-1]["high"]

                        # 计算开盘涨跌幅
                        open_pct = (curr_open - prev_close) / prev_close * 100

                        # 筛选深度低开：-5%~-3%
                        if -5.0 <= open_pct < -3.0:
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

                            print(
                                f"    深度低开: {stock}, 开盘{open_pct:.2f}%, 日内{intra_return:.2f}%"
                            )

                except Exception as e:
                    continue

            print(f"  涨停板股票数: {limit_stocks_count}")

        except Exception as e:
            print(f"  错误: {e}")
            import traceback

            traceback.print_exc()
            continue

    print("\n" + "=" * 80)
    print("阶段2结果汇总")
    print("=" * 80)

    if len(signals) == 0:
        print("\n未找到深度低开样本")
        print("判定: 删除 - 样本不存在")
    else:
        df = pd.DataFrame(signals)
        print(f"\n深度低开样本数: {len(df)}")
        print(f"平均日内收益: {df['intra_return'].mean():.2f}%")
        print(f"平均最高收益: {df['max_return'].mean():.2f}%")
        print(f"胜率: {df['is_win'].sum() / len(df) * 100:.1f}%")
        print(
            f"开盘涨跌幅范围: {df['open_pct'].min():.2f}% ~ {df['open_pct'].max():.2f}%"
        )

        print("\n详细样本:")
        for idx, row in df.iterrows():
            print(
                f"  {row['date']} {row['stock']}: 开盘{row['open_pct']:.2f}%, 日内{row['intra_return']:.2f}%"
            )

        print("\n阶段2判定:")
        if len(df) < 30:
            if (
                df["intra_return"].mean() < 0
                and df["is_win"].sum() / len(df) * 100 < 30
            ):
                print("  删除 - 样本少且收益负、胜率极低")
            else:
                print("  需进入阶段3验证 - 样本不足")
        else:
            if (
                df["intra_return"].mean() > 0.5
                and df["is_win"].sum() / len(df) * 100 > 45
            ):
                print("  推荐保留 - 样本充足，收益正，胜率合理")
            else:
                print("  需进入阶段3验证 - 收益或胜率不达标")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 阶段2测试完成 ===")
