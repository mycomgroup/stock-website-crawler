# 参数优化 - 位置阈值对比（采样测试）
from jqdata import *
import pandas as pd

print("=" * 80)
print("参数优化 - 位置阈值对比（2024年采样）")
print("=" * 80)

trade_days = get_trade_days("2024-01-01", "2024-12-31")

test_dates_indices = [
    5,
    6,
    7,
    8,
    9,
    25,
    26,
    27,
    28,
    29,
    40,
    41,
    42,
    43,
    44,
    100,
    101,
    102,
    103,
    104,
    150,
    151,
    152,
    153,
    154,
    200,
    201,
    202,
    203,
    204,
]

print(f"采样天数: {len(test_dates_indices)}")

pos_thresholds = [0.30, 0.35, 0.40, 0.45, 0.50]

results = {}

for pos_max in pos_thresholds:
    print(f"\n位置阈值: {pos_max * 100}%")

    signals = []

    for idx in test_dates_indices:
        if idx >= len(trade_days) or idx < 1:
            continue

        prev_date = trade_days[idx - 1].strftime("%Y-%m-%d")
        curr_date = trade_days[idx].strftime("%Y-%m-%d")

        try:
            q_cap = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.circulating_market_cap >= 40,
                valuation.circulating_market_cap <= 200,
            )

            df_cap = get_fundamentals(q_cap, date=curr_date)

            if df_cap.empty:
                continue

            candidates = df_cap["code"].tolist()

            price_prev = get_price(
                candidates,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )

            if price_prev.empty:
                continue

            limit_stocks = price_prev[
                abs(price_prev["close"] - price_prev["high_limit"])
                / price_prev["high_limit"]
                < 0.01
            ]["code"].tolist()

            if len(limit_stocks) == 0:
                continue

            price_curr = get_price(
                limit_stocks,
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )

            if price_curr.empty:
                continue

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])
                    curr_high = float(curr_row["high"])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if not (0.5 <= open_pct <= 1.5):
                        continue

                    prices_15d = get_price(
                        stock,
                        end_date=prev_date,
                        count=15,
                        fields=["close"],
                        panel=False,
                    )

                    if len(prices_15d) < 10:
                        continue

                    high_15d = float(prices_15d["close"].max())
                    low_15d = float(prices_15d["close"].min())

                    if high_15d == low_15d:
                        continue

                    position = (prev_close - low_15d) / (high_15d - low_15d)

                    if position > pos_max:
                        continue

                    lb_data_2d = get_price(
                        stock,
                        end_date=prev_date,
                        count=2,
                        fields=["close", "high_limit"],
                        panel=False,
                    )

                    if len(lb_data_2d) >= 2:
                        prev_prev_close = float(lb_data_2d["close"].iloc[0])
                        prev_prev_limit = float(lb_data_2d["high_limit"].iloc[0])

                        if (
                            abs(prev_prev_close - prev_prev_limit) / prev_prev_limit
                            < 0.01
                        ):
                            continue

                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100
                    win = 1 if intra_return > 0 else 0

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "win": win,
                        }
                    )

                except:
                    continue

        except:
            continue

    if len(signals) > 0:
        df_s = pd.DataFrame(signals)

        results[pos_max] = {
            "total": len(signals),
            "avg_return": df_s["intra_return"].mean(),
            "avg_max": df_s["max_return"].mean(),
            "win_rate": df_s["win"].mean() * 100,
        }

        print(
            f"  信号: {len(signals)}, 收益: {df_s['intra_return'].mean():.2f}%, 最大收益: {df_s['max_return'].mean():.2f}%, 胜率: {df_s['win'].mean() * 100:.2f}%"
        )
    else:
        results[pos_max] = {"total": 0, "avg_return": 0, "avg_max": 0, "win_rate": 0}
        print(f"  信号: 0")

print("\n" + "=" * 80)
print("参数对比汇总")
print("=" * 80)

print("\n位置阈值 | 信号数 | 平均收益 | 最大收益 | 胜率 | 年化收益预估")
print("---------|--------|----------|----------|------|--------------")

for pos_max in pos_thresholds:
    if pos_max in results:
        r = results[pos_max]
        annual = r["avg_return"] * 242 / 30 if r["avg_return"] != 0 else 0
        print(
            f"{pos_max * 100}% | {r['total']} | {r['avg_return']:.2f}% | {r['avg_max']:.2f}% | {r['win_rate']:.2f}% | {annual:.2f}%"
        )

print("\n最优参数:")
best_pos = max(
    results.keys(),
    key=lambda k: results[k]["total"] if results[k]["avg_return"] > 1.0 else 0,
)
print(f"  位置阈值: {best_pos * 100}%")
print(f"  信号数: {results[best_pos]['total']}")
print(f"  收益: {results[best_pos]['avg_return']:.2f}%")
print(f"  胜率: {results[best_pos]['win_rate']:.2f}%")

print("=" * 80)
