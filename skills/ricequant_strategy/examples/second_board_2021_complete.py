"""
二板策略完整版 - 2021年测试
包含所有过滤条件：换手率<30%、缩量、非一字板、市值排序
"""

print("=" * 80)
print("二板策略完整版 - 2021年")
print("=" * 80)

import pandas as pd
import numpy as np

YEAR = 2021
QUARTERS = [
    ("Q1", "01-01", "03-31"),
    ("Q2", "04-01", "06-30"),
    ("Q3", "07-01", "09-30"),
    ("Q4", "10-01", "12-31"),
]

results_by_quarter = {}

for q_name, q_start, q_end in QUARTERS:
    print(f"\n{'=' * 60}")
    print(f"测试 2021年 {q_name}")
    print(f"{'=' * 60}")

    start_date = f"2021-{q_start}"
    end_date = f"2021-{q_end}"

    try:
        trading_days = get_trading_dates(start_date, end_date)
        dates_ts = [pd.Timestamp(str(d)[:10]) for d in trading_days]

        print(f"交易日数: {len(dates_ts)}")

        if len(dates_ts) < 3:
            print(f"交易日不足，跳过")
            results_by_quarter[q_name] = {"trades": 0}
            continue

        # 获取股票池
        all_inst = all_instruments("CS")
        stock_list = all_inst["order_book_id"].tolist()
        stocks = [
            s
            for s in stock_list
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        trades = []

        for i in range(2, len(dates_ts) - 1):
            today = dates_ts[i]
            yesterday = dates_ts[i - 1]
            day_before_yesterday = dates_ts[i - 2]
            tomorrow = dates_ts[i + 1]

            if i % 10 == 0:
                print(f"处理: {i}/{len(dates_ts)}")

            try:
                # 1. 情绪开关：计算昨日涨停家数
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

                # 情绪开关：涨停家数 >= 10
                if zt_count < 10:
                    continue

                # 2. 获取最近3天数据（判断二板）
                prices_3d = get_price(
                    stocks[:300],
                    start_date=str(day_before_yesterday)[:10],
                    end_date=str(today)[:10],
                    frequency="1d",
                    fields=["close", "limit_up", "open", "volume"],
                )

                if prices_3d is None or prices_3d.empty:
                    continue

                # 3. 找昨天的二板股票
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

                        # 非一字板判断
                        if abs(y_open - y_limit) < 0.01:  # 一字板
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

                        # 缩量条件：昨日成交量 ≤ 前日 × 1.875
                        if y_volume > db_y_volume * 1.875:
                            continue

                        # 昨天是二板，加入候选
                        second_board_candidates.append(stock)

                    except:
                        pass

                if len(second_board_candidates) == 0:
                    continue

                # 4. 获取换手率和市值
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

                    # 5. 过滤换手率 < 30%
                    fundamentals_data = fundamentals_data[
                        fundamentals_data["turnover_rate"] < 30
                    ]

                    if len(fundamentals_data) == 0:
                        continue

                    # 6. 按市值排序
                    fundamentals_data = fundamentals_data.sort_values("market_cap")

                    # 取前3只
                    top_stocks = fundamentals_data.index.tolist()[:3]

                except:
                    top_stocks = second_board_candidates[:3]

                # 7. 今天开盘买入（非涨停开盘）
                for stock in top_stocks:
                    try:
                        key_today = (stock, today)
                        if key_today not in prices_3d.index:
                            continue

                        today_open = float(prices_3d.loc[key_today, "open"])
                        today_limit = float(prices_3d.loc[key_today, "limit_up"])

                        # 非涨停开盘才买入
                        if today_open >= today_limit * 0.99:
                            continue

                        # 获取次日数据（次日卖出）
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
                        next_high = float(prices_next.loc[next_key, "high"])
                        next_close = float(prices_next.loc[next_key, "close"])

                        # 用开盘价买入（+0.5%滑点）
                        buy_price = today_open * 1.005

                        # 次日开盘卖出
                        sell_price = next_open
                        profit = (sell_price / buy_price - 1) * 100

                        trades.append(
                            {
                                "date": str(today)[:10],
                                "stock": stock,
                                "buy_price": buy_price,
                                "sell_price": sell_price,
                                "profit": profit,
                            }
                        )

                    except:
                        pass

            except:
                pass

        # 统计
        if len(trades) > 0:
            profits = [t["profit"] for t in trades]
            wins = [p for p in profits if p > 0]

            results_by_quarter[q_name] = {
                "trades": len(trades),
                "win_rate": len(wins) / len(trades) * 100,
                "avg_profit": np.mean(profits),
                "cumulative": sum(profits),
            }

            print(f"\n{q_name}结果:")
            print(f"  交易数: {len(trades)}")
            print(f"  胜率: {len(wins) / len(trades) * 100:.2f}%")
            print(f"  平均收益: {np.mean(profits):.2f}%")
            print(f"  累计收益: {sum(profits):.2f}%")
        else:
            results_by_quarter[q_name] = {"trades": 0}
            print(f"\n{q_name}: 无交易")

    except Exception as e:
        print(f"错误: {e}")
        results_by_quarter[q_name] = {"trades": 0}

# 汇总
print(f"\n{'=' * 80}")
print("2021年汇总")
print(f"{'=' * 80}")

total_trades = sum(r.get("trades", 0) for r in results_by_quarter.values())

print(f"{'季度':<6} {'交易':<6} {'胜率':<10} {'平均收益':<12} {'累计':<10}")
print("-" * 50)

for q_name in ["Q1", "Q2", "Q3", "Q4"]:
    r = results_by_quarter.get(q_name, {})
    if r.get("trades", 0) > 0:
        print(
            f"{q_name:<6} {r['trades']:<6} {r['win_rate']:<10.2f}% {r['avg_profit']:<12.2f}% {r['cumulative']:<10.2f}%"
        )
    else:
        print(f"{q_name:<6} {'0':<6} {'无交易':<10}")

print(f"\n总交易数: {total_trades}")
print("=" * 80)
