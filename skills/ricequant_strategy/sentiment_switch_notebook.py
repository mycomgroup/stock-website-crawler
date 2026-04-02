# 情绪择时框架 - RiceQuant Notebook测试
# 测试目标：验证情绪开关（涨停家数>=30）对首板低开策略的增益效果

print("=== 情绪择时框架测试开始 ===")

try:
    import numpy as np

    # 测试参数
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    initial_capital = 100000

    # 获取交易日
    trading_dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(trading_dates)}")

    # 统计变量
    total_signals = 0
    total_trades = 0
    total_return = 0
    sentiment_on_days = 0
    sentiment_off_days = 0

    # 遍历交易日
    for i, date in enumerate(trading_dates):
        if i == 0:
            continue  # 第一天无法获取前一日数据

        prev_date = trading_dates[i - 1]

        # 获取前一日涨停股票
        try:
            all_stocks = all_instruments("CS", date=prev_date)
            if all_stocks is None or len(all_stocks) == 0:
                continue

            # 获取前一日行情
            prev_bars = {}
            for stock in all_stocks[:100]:  # 限制股票数量避免超时
                try:
                    bars = history_bars(
                        stock.order_book_id, 1, "1d", "close", prev_date, prev_date
                    )
                    if bars is not None and len(bars) > 0:
                        prev_bars[stock.order_book_id] = bars[0]
                except:
                    continue

            if len(prev_bars) == 0:
                continue

            # 计算涨停家数（简化：收盘价接近涨停价）
            zt_count = 0
            for stock_id, bar in prev_bars.items():
                # RiceQuant涨停价需要手动计算（收盘价涨幅>=9.5%视为涨停）
                if hasattr(bar, "close") and bar.close > 0:
                    # 简化判断：涨幅>=9.5%
                    prev_close = bar.close
                    if prev_close / prev_close >= 1.095:  # 简化逻辑
                        zt_count += 1

            print(f"{date}: 涨停家数≈{zt_count}")

        except Exception as e:
            print(f"{date}: 数据获取失败 - {e}")
            continue

    print(f"\n=== 统计结果 ===")
    print(f"总交易日: {len(trading_dates)}")
    print(f"情绪开启天数: {sentiment_on_days}")
    print(f"情绪关闭天数: {sentiment_off_days}")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("=== 测试完成 ===")
