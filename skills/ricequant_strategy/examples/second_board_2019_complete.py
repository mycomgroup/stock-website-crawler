"""
二板策略完整版 - 2019年测试
"""

print("=" * 80)
print("二板策略完整版 - 2019年")
print("=" * 80)

import pandas as pd
import numpy as np

YEAR = 2019
QUARTERS = [
    ("Q1", "01-01", "03-31"),
    ("Q2", "04-01", "06-30"),
    ("Q3", "07-01", "09-30"),
    ("Q4", "10-01", "12-31"),
]

results_by_quarter = {}

for q_name, q_start, q_end in QUARTERS:
    print(f"\n{'=' * 60}")
    print(f"测试 2019年 {q_name}")
    print(f"{'=' * 60}")

    start_date = f"2019-{q_start}"
    end_date = f"2019-{q_end}"

    try:
        trading_days = get_trading_dates(start_date, end_date)
        dates_ts = [pd.Timestamp(str(d)[:10]) for d in trading_days]

        print(f"交易日数: {len(dates_ts)}")

        if len(dates_ts) < 3:
            results_by_quarter[q_name] = {"trades": 0}
            continue

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
                # 情绪开关
                prices_emotion = get_price(
                    stocks[:500],
                    start_date=str(yesterday)[:10],
                    end_date=str(yesterday)[:10],
                    frequency="1d",
                    fields=["close", "limit_up"],
                )
                if prices_emotion is None or prices_emotion.empty:
                    continue

                zt_count = sum(
                    1
                    for stock in stocks[:500]
                    if (stock, yesterday) in prices_emotion.index
                    and float(prices_emotion.loc[(stock, yesterday), "close"])
                    >= float(prices_emotion.loc[(stock, yesterday), "limit_up"]) * 0.99
                )

                if zt_count < 10:
                    continue

                # 找二板
                prices_3d = get_price(
                    stocks[:300],
                    start_date=str(day_before_yesterday)[:10],
                    end_date=str(today)[:10],
                    frequency="1d",
                    fields=["close", "limit_up", "open", "volume"],
                )
                if prices_3d is None or prices_3d.empty:
                    continue

                second_board_candidates = []
                for stock in stocks[:300]:
                    try:
                        key_yesterday = (stock, yesterday)
                        if key_yesterday not in prices_3d.index:
                            continue

                        y_close = float(prices_3d.loc[key_yesterday, "close"])
                        y_limit = float(prices_3d.loc[key_yesterday, "limit_up"])
                        y_open = float(prices_3d.loc[key_yesterday, "open"])
                        y_volume = float(prices_3d.loc[key_yesterday, "volume"])

                        if y_close < y_limit * 0.99 or abs(y_open - y_limit) < 0.01:
                            continue

                        key_db_yesterday = (stock, day_before_yesterday)
                        if key_db_yesterday not in prices_3d.index:
                            continue

                        db_y_close = float(prices_3d.loc[key_db_yesterday, "close"])
                        db_y_limit = float(prices_3d.loc[key_db_yesterday, "limit_up"])
                        db_y_volume = float(prices_3d.loc[key_db_yesterday, "volume"])

                        if (
                            db_y_close < db_y_limit * 0.99
                            or y_volume > db_y_volume * 1.875
                        ):
                            continue

                        second_board_candidates.append(stock)
                    except:
                        pass

                if len(second_board_candidates) == 0:
                    continue

                # 过滤换手率和市值
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
                    fundamentals_data = fundamentals_data[
                        fundamentals_data["turnover_rate"] < 30
                    ]
                    if len(fundamentals_data) == 0:
                        continue
                    fundamentals_data = fundamentals_data.sort_values("market_cap")
                    top_stocks = fundamentals_data.index.tolist()[:3]
                except:
                    top_stocks = second_board_candidates[:3]

                # 买入
                for stock in top_stocks:
                    try:
                        key_today = (stock, today)
                        if key_today not in prices_3d.index:
                            continue

                        today_open = float(prices_3d.loc[key_today, "open"])
                        today_limit = float(prices_3d.loc[key_today, "limit_up"])

                        if today_open >= today_limit * 0.99:
                            continue

                        prices_next = get_price(
                            stock,
                            start_date=str(tomorrow)[:10],
                            end_date=str(tomorrow)[:10],
                            frequency="1d",
                            fields=["open"],
                        )
                        if prices_next is None or prices_next.empty:
                            continue

                        next_key = (stock, tomorrow)
                        if next_key not in prices_next.index:
                            continue

                        next_open = float(prices_next.loc[next_key, "open"])

                        buy_price = today_open * 1.005
                        sell_price = next_open
                        profit = (sell_price / buy_price - 1) * 100

                        trades.append(
                            {"date": str(today)[:10], "stock": stock, "profit": profit}
                        )
                    except:
                        pass
            except:
                pass

        if len(trades) > 0:
            profits = [t["profit"] for t in trades]
            wins = [p for p in profits if p > 0]
            results_by_quarter[q_name] = {
                "trades": len(trades),
                "win_rate": len(wins) / len(trades) * 100,
                "avg_profit": np.mean(profits),
                "cumulative": sum(profits),
            }
            print(
                f"\n{q_name}结果: 交易{len(trades)}笔, 胜率{len(wins) / len(trades) * 100:.2f}%, 累计{sum(profits):.2f}%"
            )
        else:
            results_by_quarter[q_name] = {"trades": 0}
            print(f"\n{q_name}: 无交易")
    except Exception as e:
        print(f"错误: {e}")
        results_by_quarter[q_name] = {"trades": 0}

# 汇总
print(f"\n{'=' * 80}\n2019年汇总\n{'=' * 80}")
total_trades = sum(r.get("trades", 0) for r in results_by_quarter.values())
print(f"总交易数: {total_trades}")
for q_name in ["Q1", "Q2", "Q3", "Q4"]:
    r = results_by_quarter.get(q_name, {})
    if r.get("trades", 0) > 0:
        print(
            f"{q_name}: 交易{r['trades']}笔, 胜率{r['win_rate']:.2f}%, 累计{r['cumulative']:.2f}%"
        )
    else:
        print(f"{q_name}: 无交易")
print("=" * 80)
