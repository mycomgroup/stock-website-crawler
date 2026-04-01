# 深度低开专项验证 - JoinQuant Notebook版本（高效版）
# 直接查询已知涨停板数据，避免全市场扫描

print("=== 深度低开专项验证开始 ===")

try:
    from jqdata import *
    import pandas as pd
    import numpy as np

    # 测试2024年3月和11月（之前测试过的月份）
    test_dates = ["2024-03-01", "2024-11-01"]

    signals = []

    for curr_date in test_dates:
        print(f"\n处理日期: {curr_date}")

        try:
            # 获取前一个交易日
            all_dates = list(get_trade_days(end_date=curr_date, count=10))
            prev_date = None
            for d in all_dates:
                if str(d) < curr_date:
                    prev_date = str(d)
                    break

            if prev_date is None:
                print(f"  未找到前一交易日")
                continue

            print(f"  前一交易日: {prev_date}")

            # 只查询前500只股票，避免全市场扫描
            all_stocks = get_all_securities("stock", prev_date).index.tolist()[:500]

            # 批量获取前一日的涨停板股票
            price_prev = get_price(
                all_stocks,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )

            if price_prev.empty:
                print(f"  无前一交易日数据")
                continue

            # 筛选涨停板股票
            limit_stocks = price_prev[
                abs(price_prev["close"] - price_prev["high_limit"])
                / price_prev["high_limit"]
                < 0.01
            ]["code"].tolist()

            print(f"  涨停板股票数: {len(limit_stocks)}")

            if len(limit_stocks) == 0:
                continue

            # 获取涨停板股票的当日数据
            price_curr = get_price(
                limit_stocks,
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )

            if price_curr.empty:
                continue

            # 分析每只股票
            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])
                    curr_high = float(curr_row["high"])

                    # 计算开盘涨跌幅
                    open_pct = (curr_open - prev_close) / prev_close * 100

                    # 筛选深度低开：-5%~-3%
                    if -5.0 <= open_pct < -3.0:
                        intra_return = (curr_close - curr_open) / curr_open * 100
                        max_return = (curr_high - curr_open) / curr_open * 100

                        signals.append(
                            {
                                "date": curr_date,
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

        except Exception as e:
            print(f"  错误: {e}")
            continue

    print("\n" + "=" * 80)
    print("结果汇总")
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

        print("\n判定:")
        if len(df) < 30:
            if (
                df["intra_return"].mean() < 0
                and df["is_win"].sum() / len(df) * 100 < 30
            ):
                print("  删除 - 样本少且收益负、胜率极低")
            else:
                print("  需更多样本验证 - 样本不足")
        else:
            if (
                df["intra_return"].mean() > 0.5
                and df["is_win"].sum() / len(df) * 100 > 45
            ):
                print("  推荐保留 - 样本充足，收益正，胜率合理")
            elif (
                df["intra_return"].mean() > 0 or df["is_win"].sum() / len(df) * 100 > 45
            ):
                print("  建议保留 - 样本充足，有改进空间")
            else:
                print("  建议删除 - 样本充足但收益太差")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 测试完成 ===")
