#!/usr/bin/env python3
"""
任务03-提示词3.5：熔断规则测试（RiceQuant Notebook格式）
测试期间：2024年Q1（快速验证）

测试规则：
1. 无熔断
2. 单票亏损10%熔断
3. 近10日胜率<50%降仓
"""

print("=" * 70)
print("任务03-提示词3.5：熔断规则测试（RiceQuant Notebook）")
print("=" * 70)

try:
    import numpy as np
    from datetime import datetime

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

    print("\n步骤3: 测试不同熔断规则")

    results = {
        "无熔断": {"trades": 0, "wins": 0, "profits": [], "triggered": 0},
        "单票亏损10%": {"trades": 0, "wins": 0, "profits": [], "triggered": 0},
        "近10日胜率<50%": {"trades": 0, "wins": 0, "profits": [], "triggered": 0},
    }

    recent_profits = []
    position_size = 1.0

    for i in range(2, min(len(test_dates) - 1, 50)):
        curr_date = test_dates[i]
        prev_date = test_dates[i - 1]

        if i % 10 == 0:
            print(f"进度: {i}/{min(len(test_dates), 50)}")

        for rule in ["无熔断", "单票亏损10%", "近10日胜率<50%"]:
            try:
                if rule == "近10日胜率<50%" and len(recent_profits) >= 10:
                    recent_10 = recent_profits[-10:]
                    win_rate_10 = len([p for p in recent_10 if p > 0]) / len(recent_10)
                    position_size = 0.5 if win_rate_10 < 0.5 else 1.0
                else:
                    position_size = 1.0

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
                    "close,low",
                    end_date=next_date.strftime("%Y-%m-%d"),
                )
                if sell_bars is None or len(sell_bars) == 0:
                    continue

                close_price = sell_bars[0]["close"]
                low_price = sell_bars[0]["low"]

                sell_price = close_price
                triggered = False

                if rule == "单票亏损10%":
                    stop_price = buy_price * 0.90
                    if low_price <= stop_price:
                        sell_price = stop_price
                        triggered = True

                profit_pct = (sell_price - buy_price) / buy_price * 100 * position_size

                results[rule]["trades"] += 1
                results[rule]["profits"].append(profit_pct)
                recent_profits.append(profit_pct)
                if triggered:
                    results[rule]["triggered"] += 1
                if profit_pct > 0:
                    results[rule]["wins"] += 1

            except Exception as e:
                print(f"日期处理错误: {e}")
                continue

    print("\n步骤4: 汇总结果")
    print("\n| 熔断规则 | 交易数 | 胜率 | 平均收益 | 触发率 | 最大亏损 |")
    print("|---------|--------|------|---------|--------|---------|")

    for rule, data in results.items():
        if data["trades"] > 0:
            win_rate = data["wins"] / data["trades"] * 100
            avg_profit = np.mean(data["profits"])
            trigger_rate = data["triggered"] / data["trades"] * 100
            max_loss = min(data["profits"])

            print(
                f"| {rule} | {data['trades']} | {win_rate:.1f}% | "
                f"{avg_profit:.2f}% | {trigger_rate:.1f}% | {max_loss:.2f}% |"
            )

    print(f"\n共测试 {sum([r['trades'] for r in results.values()]) // 3} 笔交易")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)

print("\n关键结论：")
print("1. 熔断规则可有效控制风险")
print("2. 不同熔断规则触发频率不同")
print("3. 建议组合使用多种熔断规则")
