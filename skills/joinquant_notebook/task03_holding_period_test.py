#!/usr/bin/env python3
"""
任务03-提示词3.4：持仓周期测试（JoinQuant Notebook格式）
测试期间：2024年Q1
"""

print("=" * 70)
print("任务03-提示词3.4：持仓周期测试（JoinQuant Notebook）")
print("=" * 70)

try:
    import numpy as np
    from jqdata import *

    test_dates = get_trade_days("2024-01-01", "2024-03-31")
    print(f"测试期间: 2024年Q1, 共{len(test_dates)}个交易日")

    def get_zt_stocks(date_str):
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
                    stock, end_date=date_str, count=1, fields=["close", "high_limit"]
                )
                if (
                    len(df) > 0
                    and df["close"].iloc[0] >= df["high_limit"].iloc[0] * 0.99
                ):
                    zt_stocks.append(stock)
            except:
                pass
        return zt_stocks

    def filter_yzb(stock_list, date_str):
        result = []
        for s in stock_list[:30]:
            try:
                df = get_price(s, end_date=date_str, count=1, fields=["low", "high"])
                if len(df) > 0 and df["low"].iloc[0] != df["high"].iloc[0]:
                    result.append(s)
            except:
                pass
        return result

    def get_market_cap(stocks, date_str):
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

    def check_zt(stock, date_str):
        try:
            df = get_price(
                stock, end_date=date_str, count=1, fields=["close", "high_limit"]
            )
            return (
                len(df) > 0 and df["close"].iloc[0] >= df["high_limit"].iloc[0] * 0.99
            )
        except:
            return False

    results = {
        "T+1": {"trades": 0, "wins": 0, "profits": [], "holding_days": []},
        "T+2": {"trades": 0, "wins": 0, "profits": [], "holding_days": []},
        "T+1或T+2": {
            "trades": 0,
            "wins": 0,
            "profits": [],
            "holding_days": [],
            "zt_holds": 0,
        },
    }

    for i in range(2, min(len(test_dates) - 2, 50)):
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
            if (
                len(buy_df) == 0
                or buy_df["open"].iloc[0] >= buy_df["high_limit"].iloc[0] * 0.99
            ):
                continue

            buy_price = buy_df["open"].iloc[0]

            for rule in ["T+1", "T+2", "T+1或T+2"]:
                sell_price = None
                holding_days = None

                if rule == "T+1":
                    next_date = test_dates[i + 1]
                    sell_df = get_price(
                        test_stock,
                        end_date=next_date.strftime("%Y-%m-%d"),
                        count=1,
                        fields=["close"],
                    )
                    if len(sell_df) > 0:
                        sell_price = sell_df["close"].iloc[0]
                        holding_days = 1

                elif rule == "T+2":
                    next_date2 = test_dates[i + 2]
                    sell_df = get_price(
                        test_stock,
                        end_date=next_date2.strftime("%Y-%m-%d"),
                        count=1,
                        fields=["close"],
                    )
                    if len(sell_df) > 0:
                        sell_price = sell_df["close"].iloc[0]
                        holding_days = 2

                elif rule == "T+1或T+2":
                    next_date = test_dates[i + 1]
                    if check_zt(test_stock, next_date.strftime("%Y-%m-%d")):
                        next_date2 = test_dates[i + 2]
                        sell_df = get_price(
                            test_stock,
                            end_date=next_date2.strftime("%Y-%m-%d"),
                            count=1,
                            fields=["close"],
                        )
                        if len(sell_df) > 0:
                            sell_price = sell_df["close"].iloc[0]
                            holding_days = 2
                            results[rule]["zt_holds"] += 1
                    else:
                        sell_df = get_price(
                            test_stock,
                            end_date=next_date.strftime("%Y-%m-%d"),
                            count=1,
                            fields=["close"],
                        )
                        if len(sell_df) > 0:
                            sell_price = sell_df["close"].iloc[0]
                            holding_days = 1

                if sell_price and holding_days:
                    profit_pct = (sell_price - buy_price) / buy_price * 100
                    results[rule]["trades"] += 1
                    results[rule]["profits"].append(profit_pct)
                    results[rule]["holding_days"].append(holding_days)
                    if profit_pct > 0:
                        results[rule]["wins"] += 1

        except Exception as e:
            continue

    print("\n| 持仓周期 | 交易数 | 胜率 | 平均收益 | 平均持仓 | 涨停持有 |")
    print("|---------|--------|------|---------|---------|---------|")

    for rule, data in results.items():
        if data["trades"] > 0:
            win_rate = data["wins"] / data["trades"] * 100
            avg_profit = np.mean(data["profits"])
            avg_holding = np.mean(data["holding_days"])
            zt_holds = data.get("zt_holds", 0)

            print(
                f"| {rule} | {data['trades']} | {win_rate:.1f}% | "
                f"{avg_profit:.2f}% | {avg_holding:.1f}天 | {zt_holds} |"
            )

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n测试完成")
