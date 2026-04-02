"""
小市值因子 vs 事件策略归因分析 - RiceQuant Notebook版本
因子简单，优先使用 RiceQuant（Session自动管理）
"""

print("=== 小市值因子 vs 事件策略归因分析 ===")

try:
    import pandas as pd
    import numpy as np

    # 回测参数
    test_date = "2024-01-03"  # RiceQuant格式
    prev_date = "2024-01-02"

    print(f"测试日期: {prev_date} -> {test_date}")

    # ============ 策略A: 纯小市值因子 ============
    print("\n=== 策略A: 纯小市值因子 ===")

    # RiceQuant API: all_instruments
    stocks = all_instruments("CS")
    print(f"全市场股票数: {len(stocks)}")

    # RiceQuant API: get_factor 获取市值
    # 限制股票数量避免超时
    test_stocks = list(stocks.order_book_id)[:500]

    try:
        factor_data = get_factor(
            test_stocks, ["market_cap"], start_date=test_date, end_date=test_date
        )

        if factor_data is not None and len(factor_data) > 0:
            # 按市值排序
            factor_data = factor_data.sort_values("market_cap", ascending=True)

            # 选最小的前10%，最多20只
            target_count = max(1, int(len(factor_data) * 0.1))
            small_cap_stocks = factor_data.head(min(target_count, 20))

            print(f"策略A选股数: {len(small_cap_stocks)}")
            print("\n市值最小的股票（前5只）:")
            print(small_cap_stocks.head())
        else:
            print("获取市值因子失败")

    except Exception as e:
        print(f"策略A查询失败: {e}")

    # ============ 策略B: 小市值 + 事件 ============
    print("\n=== 策略B: 小市值+事件（市值5-15亿+首板） ===")

    # 市值限制：5-15亿（RiceQuant市值单位通常是亿元）
    try:
        factor_data_b = get_factor(
            test_stocks, ["market_cap"], start_date=prev_date, end_date=prev_date
        )

        if factor_data_b is not None and len(factor_data_b) > 0:
            # 筛选市值5-15亿
            cap_filtered = factor_data_b[
                (factor_data_b["market_cap"] >= 5) & (factor_data_b["market_cap"] <= 15)
            ]

            print(f"市值5-15亿的股票数: {len(cap_filtered)}")

            if len(cap_filtered) > 0:
                small_cap_codes = list(cap_filtered.index)[:100]

                # RiceQuant API: history_bars 获取涨停价
                # 检查首板：昨日涨停
                limit_up_stocks = []

                for stock in small_cap_codes[:20]:  # 只测试前20只避免超时
                    try:
                        bars = history_bars(
                            stock, 1, "1d", ["close", "limit_up"], prev_date
                        )

                        if bars is not None and len(bars) > 0:
                            close = bars["close"].iloc[-1]
                            limit_up = bars["limit_up"].iloc[-1]

                            if close == limit_up:
                                limit_up_stocks.append(stock)
                    except:
                        pass

                print(f"首板股票数: {len(limit_up_stocks)}")

                if len(limit_up_stocks) > 0:
                    print("首板股票列表:")
                    for stock in limit_up_stocks:
                        print(f"  {stock}")

                    # 检查今日低开
                    low_open_stocks = []
                    for stock in limit_up_stocks:
                        try:
                            prev_close_bars = history_bars(
                                stock, 1, "1d", ["close"], prev_date
                            )
                            curr_open_bars = history_bars(
                                stock, 1, "1d", ["open"], test_date
                            )

                            if (
                                prev_close_bars is not None
                                and curr_open_bars is not None
                            ):
                                prev_close = prev_close_bars["close"].iloc[-1]
                                curr_open = curr_open_bars["open"].iloc[-1]

                                open_pct = (curr_open - prev_close) / prev_close * 100

                                if -3.0 <= open_pct <= 1.5:
                                    low_open_stocks.append(
                                        {"stock": stock, "open_pct": open_pct}
                                    )
                        except:
                            pass

                    print(f"\n低开股票数（-3% ~ +1.5%）: {len(low_open_stocks)}")
                    if len(low_open_stocks) > 0:
                        print("策略B最终选股:")
                        for item in low_open_stocks[:5]:
                            print(
                                f"  {item['stock']}: 开盘涨幅 {item['open_pct']:.2f}%"
                            )
    except Exception as e:
        print(f"策略B查询失败: {e}")

    # ============ 策略C: 纯事件（全市场首板低开） ============
    print("\n=== 策略C: 纯事件（全市场首板低开） ===")

    # 不限制市值，全市场首板
    try:
        # 测试前200只股票（避免超时）
        all_test_stocks = list(stocks.order_book_id)[:200]

        limit_up_c = []
        for stock in all_test_stocks:
            try:
                bars_c = history_bars(stock, 1, "1d", ["close", "limit_up"], prev_date)

                if bars_c is not None and len(bars_c) > 0:
                    close_c = bars_c["close"].iloc[-1]
                    limit_up_c_val = bars_c["limit_up"].iloc[-1]

                    if close_c == limit_up_c_val:
                        limit_up_c.append(stock)
            except:
                pass

        print(f"全市场首板股票数（前200只样本）: {len(limit_up_c)}")

        if len(limit_up_c) > 0:
            print("首板股票:")
            for stock in limit_up_c[:10]:
                print(f"  {stock}")
    except Exception as e:
        print(f"策略C查询失败: {e}")

    print("\n=== 归因分析快速验证完成 ===")
    print("说明:")
    print("- 这是RiceQuant Notebook快速验证版本")
    print("- 由于API时间限制，只测试了部分股票")
    print("- 完整回测需使用RiceQuant策略编辑器")

except Exception as e:
    print(f"执行错误: {e}")
    import traceback

    traceback.print_exc()

print("=== 测试完成 ===")
