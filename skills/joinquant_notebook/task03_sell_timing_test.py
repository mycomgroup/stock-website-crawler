#!/usr/bin/env python3
"""
任务03-提示词3.1：卖出时机对比测试（JoinQuant Notebook格式）
测试期间：2024年Q1（快速验证）
"""

print("=" * 70)
print("任务03-提示词3.1：卖出时机对比测试（JoinQuant Notebook）")
print("=" * 70)

try:
    import numpy as np
    from jqdata import *

    print("\n步骤1: 获取交易日")
    test_dates = get_trade_days("2024-01-01", "2024-03-31")
    print(f"测试期间: 2024年Q1, 共{len(test_dates)}个交易日")

    print("\n步骤2: 定义辅助函数")

    def get_zt_stocks(date_str):
        """获取涨停股票"""
        try:
            all_stocks = get_all_securities("stock", date_str).index.tolist()
            all_stocks = [
                s
                for s in all_stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ][:300]

            zt_stocks = []
            for stock in all_stocks[:100]:
                try:
                    df = get_price(
                        stock,
                        end_date=date_str,
                        count=1,
                        fields=["close", "high_limit"],
                    )
                    if len(df) > 0:
                        if df["close"].iloc[0] >= df["high_limit"].iloc[0] * 0.99:
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
                df = get_price(s, end_date=date_str, count=1, fields=["low", "high"])
                if len(df) > 0:
                    if df["low"].iloc[0] != df["high"].iloc[0]:
                        result.append(s)
            except:
                pass
        return result

    def get_market_cap(stocks, date_str):
        """获取市值（流通市值5-15亿）"""
        result = []
        for s in stocks[:20]:
            try:
                q = query(valuation.circulating_market_cap).filter(valuation.code == s)
                df = get_fundamentals(q, date=date_str)
                if len(df) > 0:
                    cap = df["circulating_market_cap"].iloc[0]
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

            buy_df = get_price(
                test_stock,
                end_date=curr_date.strftime("%Y-%m-%d"),
                count=1,
                fields=["open", "high_limit"],
            )
            if len(buy_df) == 0:
                continue

            buy_price = buy_df["open"].iloc[0]
            limit_up = buy_df["high_limit"].iloc[0]

            if buy_price >= limit_up * 0.99:
                continue

            next_date = test_dates[i + 1]
            sell_df = get_price(
                test_stock,
                end_date=next_date.strftime("%Y-%m-%d"),
                count=1,
                fields=["open", "close", "high"],
            )
            if len(sell_df) == 0:
                continue

            open_price = sell_df["open"].iloc[0]
            close_price = sell_df["close"].iloc[0]
            high_price = sell_df["high"].iloc[0]

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

    total_trades = sum([r["trades"] for r in results.values()]) // 3
    print(f"\n共测试 {total_trades} 笔交易")

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
