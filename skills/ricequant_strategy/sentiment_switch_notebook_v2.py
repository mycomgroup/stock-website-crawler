# 情绪择时框架 - RiceQuant Notebook测试 v2
# 测试目标：验证情绪开关对首板低开的增益

print("=== 情绪择时框架测试 v2 ===")

try:
    # 测试参数
    test_start = "2024-03-01"
    test_end = "2024-03-15"

    # 获取交易日
    trading_dates = get_trading_dates(test_start, test_end)
    print(f"测试期间: {test_start} 至 {test_end}")
    print(f"交易日数: {len(trading_dates)}")

    # 统计变量
    signals = []

    # 遍历前5个交易日进行快速测试
    for i in range(min(5, len(trading_dates))):
        date = trading_dates[i]

        try:
            # 获取当日所有股票
            all_stocks = all_instruments("CS", date=date)
            if all_stocks is None or len(all_stocks) == 0:
                print(f"{date}: 无股票数据")
                continue

            # 限制股票数量避免超时（取前200只）
            test_stocks = all_stocks[:200]

            # 统计涨停家数（涨幅>=9.8%）
            zt_count = 0

            for stock in test_stocks:
                try:
                    # 获取当日和前一日收盘价
                    bars = history_bars(
                        stock.order_book_id, 2, "1d", "close", date, date
                    )
                    if bars is not None and len(bars) >= 2:
                        today_close = bars[-1]
                        prev_close = bars[-2]
                        if prev_close > 0:
                            pct_change = (today_close / prev_close - 1) * 100
                            if pct_change >= 9.8:  # 涨幅>=9.8%视为涨停
                                zt_count += 1
                except:
                    continue

            # 情绪开关判断
            sentiment_on = zt_count >= 10  # 简化阈值

            print(f"{date}: 涨停≈{zt_count}, 情绪={'开' if sentiment_on else '关'}")

            if sentiment_on:
                # 统计低开股票（次日低开-5%~-1%）
                if i + 1 < len(trading_dates):
                    next_date = trading_dates[i + 1]
                    low_open_count = 0

                    for stock in test_stocks:
                        try:
                            # 获取次日开盘价和前日收盘价
                            bars_next = history_bars(
                                stock.order_book_id,
                                2,
                                "1d",
                                "close",
                                next_date,
                                next_date,
                            )
                            if bars_next is not None and len(bars_next) >= 2:
                                # RiceQuant获取开盘价需要用history_bars的open字段
                                bars_open = history_bars(
                                    stock.order_book_id,
                                    1,
                                    "1d",
                                    "open",
                                    next_date,
                                    next_date,
                                )
                                if bars_open is not None and len(bars_open) > 0:
                                    next_open = bars_open[0]
                                    prev_close = bars_next[-2]
                                    if prev_close > 0:
                                        open_ratio = (next_open / prev_close - 1) * 100
                                        if -5 <= open_ratio <= -1:
                                            low_open_count += 1
                        except:
                            continue

                    signals.append(
                        {
                            "date": date,
                            "zt_count": zt_count,
                            "sentiment": "on",
                            "next_date": next_date,
                            "low_open_count": low_open_count,
                        }
                    )
                    print(f"  -> 次日低开股票数: {low_open_count}")

        except Exception as e:
            print(f"{date}: 错误 - {e}")
            continue

    # 输出统计
    print(f"\n=== 测试结果 ===")
    print(f"信号数: {len(signals)}")
    if len(signals) > 0:
        for sig in signals:
            print(
                f"  {sig['date']}: 涨停{sig['zt_count']} -> 次日低开{sig['low_open_count']}只"
            )

except Exception as e:
    print(f"整体错误: {e}")
    import traceback

    traceback.print_exc()

print("=== 测试完成 ===")
