"""
二板策略分季度测试 - 2021年
Q1/Q2/Q3/Q4分别测试，避免超时
"""

print("=" * 80)
print("二板策略分季度测试 - 2021年")
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

        for i in range(2, len(dates_ts) - 1):  # 从第3天开始（需要前2天数据）
            test_date = dates_ts[i]
            next_date = dates_ts[i + 1]

            if i % 10 == 0:
                print(f"处理: {i}/{len(dates_ts)}")

            try:
                # 获取当日涨停
                prices_today = get_price(
                    stocks[:300],
                    start_date=str(test_date)[:10],
                    end_date=str(test_date)[:10],
                    frequency="1d",
                    fields=["close", "limit_up"],
                )

                if prices_today is None or prices_today.empty:
                    continue

                # 找涨停
                zt_stocks = []
                for stock in stocks[:300]:
                    try:
                        key = (stock, test_date)
                        if key in prices_today.index:
                            close = float(prices_today.loc[key, "close"])
                            limit_up = float(prices_today.loc[key, "limit_up"])

                            if close >= limit_up * 0.99:
                                zt_stocks.append(stock)
                    except:
                        pass

                if len(zt_stocks) == 0:
                    continue

                # 找二板
                prev_date = dates_ts[i - 1]
                prev2_date = dates_ts[i - 2]

                prices_3d = get_price(
                    zt_stocks[:20],
                    start_date=str(prev2_date)[:10],
                    end_date=str(test_date)[:10],
                    frequency="1d",
                    fields=["close", "limit_up"],
                )

                if prices_3d is None or prices_3d.empty:
                    continue

                for stock in zt_stocks[:20]:
                    try:
                        # 今天涨停
                        key_today = (stock, test_date)
                        if key_today not in prices_3d.index:
                            continue

                        today_close = float(prices_3d.loc[key_today, "close"])
                        today_limit = float(prices_3d.loc[key_today, "limit_up"])

                        # 昨天涨停
                        key_prev = (stock, prev_date)
                        if key_prev not in prices_3d.index:
                            continue

                        yesterday_close = float(prices_3d.loc[key_prev, "close"])
                        yesterday_limit = float(prices_3d.loc[key_prev, "limit_up"])

                        # 前天不涨停
                        key_prev2 = (stock, prev2_date)
                        if key_prev2 not in prices_3d.index:
                            continue

                        prev2_close = float(prices_3d.loc[key_prev2, "close"])
                        prev2_limit = float(prices_3d.loc[key_prev2, "limit_up"])

                        # 判断二板
                        if today_close >= today_limit * 0.99:
                            if yesterday_close >= yesterday_limit * 0.99:
                                if prev2_close < prev2_limit * 0.99:
                                    # 非涨停开盘买入
                                    next_prices = get_price(
                                        stock,
                                        start_date=str(next_date)[:10],
                                        end_date=str(next_date)[:10],
                                        fields=["open", "close", "high"],
                                    )

                                    if next_prices is None or next_prices.empty:
                                        continue

                                    next_key = (stock, next_date)
                                    if next_key not in next_prices.index:
                                        continue

                                    open_price = float(
                                        next_prices.loc[next_key, "open"]
                                    )
                                    close_price = float(
                                        next_prices.loc[next_key, "close"]
                                    )
                                    high_price = float(
                                        next_prices.loc[next_key, "high"]
                                    )

                                    if open_price >= today_limit * 0.99:
                                        continue

                                    # 用涨停价买入
                                    buy_price = today_limit * 1.005
                                    profit = (close_price / buy_price - 1) * 100

                                    trades.append(
                                        {
                                            "date": str(test_date)[:10],
                                            "stock": stock,
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
