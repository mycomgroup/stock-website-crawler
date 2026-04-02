"""
二板策略分季度测试 - 2021年（修正版）
正确逻辑：昨天二板，今天开盘买入
"""

print("=" * 80)
print("二板策略分季度测试 - 2021年（修正版）")
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

        # 从第2天开始（需要昨天和前天的数据）
        for i in range(2, len(dates_ts)):
            today = dates_ts[i]
            yesterday = dates_ts[i - 1]
            day_before_yesterday = dates_ts[i - 2]

            if i % 10 == 0:
                print(f"处理: {i}/{len(dates_ts)}")

            try:
                # 获取最近3天数据（用于判断昨天是否是二板）
                prices_3d = get_price(
                    stocks[:300],
                    start_date=str(day_before_yesterday)[:10],
                    end_date=str(today)[:10],
                    frequency="1d",
                    fields=["close", "limit_up", "open"],
                )

                if prices_3d is None or prices_3d.empty:
                    continue

                # 找昨天的二板股票
                second_board_stocks = []

                for stock in stocks[:300]:
                    try:
                        # 昨天涨停
                        key_yesterday = (stock, yesterday)
                        if key_yesterday not in prices_3d.index:
                            continue

                        y_close = float(prices_3d.loc[key_yesterday, "close"])
                        y_limit = float(prices_3d.loc[key_yesterday, "limit_up"])

                        if y_close < y_limit * 0.99:
                            continue

                        # 前天涨停
                        key_db_yesterday = (stock, day_before_yesterday)
                        if key_db_yesterday not in prices_3d.index:
                            continue

                        db_y_close = float(prices_3d.loc[key_db_yesterday, "close"])
                        db_y_limit = float(prices_3d.loc[key_db_yesterday, "limit_up"])

                        if db_y_close < db_y_limit * 0.99:
                            continue

                        # 昨天是二板！
                        second_board_stocks.append(stock)

                    except:
                        pass

                if len(second_board_stocks) == 0:
                    continue

                # 今天开盘买入（如果开盘<涨停价）
                for stock in second_board_stocks[:10]:  # 限制数量
                    try:
                        key_today = (stock, today)
                        if key_today not in prices_3d.index:
                            continue

                        today_open = float(prices_3d.loc[key_today, "open"])
                        today_limit = float(prices_3d.loc[key_today, "limit_up"])
                        today_close = float(prices_3d.loc[key_today, "close"])

                        # 非涨停开盘才买入
                        if today_open >= today_limit * 0.99:
                            continue

                        # 用开盘价买入（+0.5%滑点）
                        buy_price = today_open * 1.005
                        profit = (today_close / buy_price - 1) * 100

                        trades.append(
                            {
                                "date": str(today)[:10],
                                "stock": stock,
                                "buy_price": buy_price,
                                "sell_price": today_close,
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

            # 显示前3笔交易
            print(f"  前3笔交易:")
            for t in trades[:3]:
                print(f"    {t['date']}: {t['stock']} 收益 {t['profit']:.2f}%")
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
