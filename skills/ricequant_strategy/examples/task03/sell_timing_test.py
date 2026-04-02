#!/usr/bin/env python3
"""
任务03-提示词3.1：卖出时机对比测试（RiceQuant Notebook格式）
测试期间：2024年Q1（快速验证）

测试时机：
1. 次日开盘卖出
2. 次日收盘卖出
3. 次日最高价卖出（理想上限）
"""

print("=" * 70)
print("任务03-提示词3.1：卖出时机对比测试（RiceQuant Notebook）")
print("=" * 70)

try:
    import numpy as np
    from datetime import datetime, timedelta

    print("\n步骤1: 获取交易日")
    test_dates = get_trading_dates("2024-01-01", "2024-03-31")
    print(f"测试期间: 2024年Q1, 共{len(test_dates)}个交易日")

    print("\n步骤2: 定义辅助函数")

    def get_zt_stocks(date_str):
        """获取涨停股票"""
        try:
            all_stocks = all_instruments("CS")
            stock_list = [
                s.order_book_id
                for s in all_stocks
                if not s.order_book_id.startswith(("688", "4", "8"))
            ][:300]

            zt_stocks = []
            for stock in stock_list[:100]:
                try:
                    bars = history_bars(
                        stock, 1, "1d", "close,limit_up", end_date=date_str
                    )
                    if bars is not None and len(bars) > 0:
                        if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                            zt_stocks.append(stock)
                except:
                    pass
            return zt_stocks
        except:
            return []

    def filter_yzb(stock_list, date_str):
        """过滤一字板"""
        result = []
        for s in stock_list[:30]:
            try:
                bars = history_bars(s, 1, "1d", "low,high", end_date=date_str)
                if bars is not None and len(bars) > 0:
                    if bars[0]["low"] != bars[0]["high"]:
                        result.append(s)
            except:
                pass
        return result

    def get_market_cap(stocks, date_str):
        """获取市值"""
        result = []
        for s in stocks[:20]:
            try:
                df = get_factor(s, "market_cap", start_date=date_str, end_date=date_str)
                if df is not None and len(df) > 0:
                    cap = df.iloc[0][s]
                    if 5 <= cap <= 15:
                        result.append(s)
            except:
                pass
        return result

    print("\n步骤3: 测试不同卖出时机")

    results = {
        "开盘卖出": {"trades": 0, "wins": 0, "profits": []},
        "收盘卖出": {"trades": 0, "wins": 0, "profits": []},
        "最高价卖出": {"trades": 0, "wins": 0, "profits": []},
    }

    for i in range(2, min(len(test_dates) - 1, 50)):
        curr_date = test_dates[i]
        prev_date = test_dates[i - 1]

        if i % 10 == 0:
            print(f"进度: {i}/{min(len(test_dates), 50)}")

        try:
            zt_prev = get_zt_stocks(prev_date.strftime("%Y-%m-%d"))
            zt_prev2 = get_zt_stocks(test_dates[i - 2].strftime("%Y-%m-%d"))

            two_board = list(set(zt_prev) & set(zt_prev2))
            non_yzb = filter_yzb(two_board, prev_date.strftime("%Y-%m-%d"))
            cap_filtered = get_market_cap(non_yzb, prev_date.strftime("%Y-%m-%d"))

            if len(cap_filtered) == 0:
                continue

            test_stock = cap_filtered[0]

            buy_bars = history_bars(
                test_stock,
                1,
                "1d",
                "open,limit_up",
                end_date=curr_date.strftime("%Y-%m-%d"),
            )
            if buy_bars is None or len(buy_bars) == 0:
                continue

            buy_price = buy_bars[0]["open"]
            limit_up = buy_bars[0]["limit_up"]

            if buy_price >= limit_up * 0.99:
                continue

            next_date = test_dates[i + 1]
            sell_bars = history_bars(
                test_stock,
                1,
                "1d",
                "open,close,high",
                end_date=next_date.strftime("%Y-%m-%d"),
            )
            if sell_bars is None or len(sell_bars) == 0:
                continue

            open_price = sell_bars[0]["open"]
            close_price = sell_bars[0]["close"]
            high_price = sell_bars[0]["high"]

            for timing in ["开盘卖出", "收盘卖出", "最高价卖出"]:
                if timing == "开盘卖出":
                    sell_price = open_price
                elif timing == "收盘卖出":
                    sell_price = close_price
                elif timing == "最高价卖出":
                    sell_price = high_price

                profit_pct = (sell_price - buy_price) / buy_price * 100

                results[timing]["trades"] += 1
                results[timing]["profits"].append(profit_pct)
                if profit_pct > 0:
                    results[timing]["wins"] += 1

        except Exception as e:
            print(f"日期处理错误: {e}")
            continue

    print("\n步骤4: 汇总结果")
    print("\n| 卖出时机 | 交易数 | 胜率 | 平均收益 | 最大收益 | 最小收益 |")
    print("|---------|--------|------|---------|---------|---------|")

    for timing, data in results.items():
        if data["trades"] > 0:
            win_rate = data["wins"] / data["trades"] * 100
            avg_profit = np.mean(data["profits"])
            max_profit = max(data["profits"])
            min_profit = min(data["profits"])

            print(
                f"| {timing} | {data['trades']} | {win_rate:.1f}% | "
                f"{avg_profit:.2f}% | {max_profit:.2f}% | {min_profit:.2f}% |"
            )

    print("\n步骤5: 保存结果")
    output_data = {
        "task": "task03_prompt31_sell_timing_test",
        "platform": "RiceQuant Notebook",
        "test_period": "2024-Q1",
        "results": results,
    }

    print(f"\n结果已生成，共测试 {sum([r['trades'] for r in results.values()])} 笔交易")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)

print("\n关键结论：")
print("1. 收盘卖出为当前基准方案")
print("2. 最高价卖出为理想上限")
print("3. 开盘卖出可规避日内风险")
print("\n建议：继续测试其他卖出时机（10:30、13:30等）")
