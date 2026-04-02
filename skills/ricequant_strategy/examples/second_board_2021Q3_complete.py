"""
二板策略完整版 - 快速测试（仅2021年Q3）
包含所有过滤条件
"""

print("=" * 80)
print("二板策略完整版 - 2021年Q3测试")
print("=" * 80)

import pandas as pd
import numpy as np

start_date = "2021-07-01"
end_date = "2021-09-30"

print(f"测试期间: {start_date} ~ {end_date}")

try:
    trading_days = get_trading_dates(start_date, end_date)
    dates_ts = [pd.Timestamp(str(d)[:10]) for d in trading_days]

    print(f"交易日数: {len(dates_ts)}")

    # 获取股票池
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    print(f"股票池: {len(stocks)}只")

    trades = []

    for i in range(2, len(dates_ts) - 1):
        today = dates_ts[i]
        yesterday = dates_ts[i - 1]
        day_before_yesterday = dates_ts[i - 2]
        tomorrow = dates_ts[i + 1]

        if i % 5 == 0:
            print(f"处理: {i}/{len(dates_ts)}")

        try:
            # 1. 情绪开关
            prices_emotion = get_price(
                stocks[:500],
                start_date=str(yesterday)[:10],
                end_date=str(yesterday)[:10],
                frequency="1d",
                fields=["close", "limit_up"],
            )

            if prices_emotion is None or prices_emotion.empty:
                continue

            zt_count = 0
            for stock in stocks[:500]:
                try:
                    key = (stock, yesterday)
                    if key in prices_emotion.index:
                        close = float(prices_emotion.loc[key, "close"])
                        limit_up = float(prices_emotion.loc[key, "limit_up"])
                        if close >= limit_up * 0.99:
                            zt_count += 1
                except:
                    pass

            if zt_count < 10:
                continue

            # 2. 找二板
            prices_3d = get_price(
                stocks[:300],
                start_date=str(day_before_yesterday)[:10],
                end_date=str(today)[:10],
                frequency="1d",
                fields=["close", "limit_up", "open", "volume"],
            )

            if prices_3d is None or prices_3d.empty:
                continue

            second_board_candidates = []

            for stock in stocks[:300]:
                try:
                    # 昨天涨停
                    key_yesterday = (stock, yesterday)
                    if key_yesterday not in prices_3d.index:
                        continue

                    y_close = float(prices_3d.loc[key_yesterday, "close"])
                    y_limit = float(prices_3d.loc[key_yesterday, "limit_up"])
                    y_open = float(prices_3d.loc[key_yesterday, "open"])
                    y_volume = float(prices_3d.loc[key_yesterday, "volume"])

                    if y_close < y_limit * 0.99:
                        continue

                    # 非一字板
                    if abs(y_open - y_limit) < 0.01:
                        continue

                    # 前天涨停
                    key_db_yesterday = (stock, day_before_yesterday)
                    if key_db_yesterday not in prices_3d.index:
                        continue

                    db_y_close = float(prices_3d.loc[key_db_yesterday, "close"])
                    db_y_limit = float(prices_3d.loc[key_db_yesterday, "limit_up"])
                    db_y_volume = float(prices_3d.loc[key_db_yesterday, "volume"])

                    if db_y_close < db_y_limit * 0.99:
                        continue

                    # 缩量
                    if y_volume > db_y_volume * 1.875:
                        continue

                    second_board_candidates.append(stock)

                except:
                    pass

            if len(second_board_candidates) == 0:
                continue

            # 3. 过滤换手率和市值
            try:
                fundamentals_data = get_fundamentals(
                    query(
                        fundamentals.eod_derivative_indicator.turnover_rate,
                        fundamentals.eod_market_cap.market_cap,
                    ).filter(fundamentals.stockcode.in_(second_board_candidates)),
                    str(yesterday)[:10],
                )

                if fundamentals_data is None or fundamentals_data.empty:
                    continue

                # 换手率 < 30%
                fundamentals_data = fundamentals_data[
                    fundamentals_data["turnover_rate"] < 30
                ]

                if len(fundamentals_data) == 0:
                    continue

                # 按市值排序
                fundamentals_data = fundamentals_data.sort_values("market_cap")
                top_stocks = fundamentals_data.index.tolist()[:3]

            except:
                top_stocks = second_board_candidates[:3]

            # 4. 买入
            for stock in top_stocks:
                try:
                    key_today = (stock, today)
                    if key_today not in prices_3d.index:
                        continue

                    today_open = float(prices_3d.loc[key_today, "open"])
                    today_limit = float(prices_3d.loc[key_today, "limit_up"])

                    # 非涨停开盘
                    if today_open >= today_limit * 0.99:
                        continue

                    # 次日数据
                    prices_next = get_price(
                        stock,
                        start_date=str(tomorrow)[:10],
                        end_date=str(tomorrow)[:10],
                        frequency="1d",
                        fields=["open", "high", "close"],
                    )

                    if prices_next is None or prices_next.empty:
                        continue

                    next_key = (stock, tomorrow)
                    if next_key not in prices_next.index:
                        continue

                    next_open = float(prices_next.loc[next_key, "open"])

                    # 买入和卖出
                    buy_price = today_open * 1.005
                    sell_price = next_open
                    profit = (sell_price / buy_price - 1) * 100

                    trades.append(
                        {"date": str(today)[:10], "stock": stock, "profit": profit}
                    )

                except:
                    pass

        except:
            pass

    # 统计
    if len(trades) > 0:
        profits = [t["profit"] for t in trades]
        wins = [p for p in profits if p > 0]

        print(f"\n结果:")
        print(f"  交易数: {len(trades)}")
        print(f"  胜率: {len(wins) / len(trades) * 100:.2f}%")
        print(f"  平均收益: {np.mean(profits):.2f}%")
        print(f"  累计收益: {sum(profits):.2f}%")

        print(f"\n前5笔交易:")
        for t in trades[:5]:
            print(f"  {t['date']}: {t['stock']} 收益 {t['profit']:.2f}%")
    else:
        print("\n无交易")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
