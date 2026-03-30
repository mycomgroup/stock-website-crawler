# 主线信号放宽测试 - 修正版（使用正确筛选逻辑）
from jqdata import *
import pandas as pd

print("主线信号放宽测试 - 修正版（正确筛选逻辑）")

trade_days = get_trade_days("2024-01-01", "2024-12-31")
print(f"全年交易日数: {len(trade_days)}")

versions = {
    "原版": (50, 150, 0.30),
    "放宽A": (40, 200, 0.30),
    "放宽B": (50, 150, 0.50),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

test_dates_idx = [5, 6, 7, 8, 9]

results = {}

for vname, (cap_min, cap_max, pos_max) in versions.items():
    print(f"\n{'=' * 50}")
    print(f"版本: {vname} (市值{cap_min}-{cap_max}亿, 位置≤{int(pos_max * 100)}%)")
    print(f"{'=' * 50}")

    signals = []

    for idx in test_dates_idx:
        if idx >= len(trade_days) or idx < 1:
            continue

        prev_date = trade_days[idx - 1].strftime("%Y-%m-%d")
        curr_date = trade_days[idx].strftime("%Y-%m-%d")

        print(f"  处理: {curr_date}")

        try:
            all_stocks = get_all_securities("stock", prev_date).index.tolist()

            price_prev = get_price(
                all_stocks,
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
                print(f"    当日涨停数: 0")
                continue

            print(f"    当日涨停数: {len(limit_stocks)}")

            price_curr = get_price(
                limit_stocks,
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )

            if price_curr.empty:
                continue

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(limit_stocks),
                valuation.circulating_market_cap >= cap_min,
                valuation.circulating_market_cap <= cap_max,
            )

            val_data = get_fundamentals(q, date=curr_date)

            if val_data.empty:
                continue

            day_signals = 0

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])
                    curr_high = float(curr_row["high"])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if not (-10 <= open_pct <= 10):
                        continue

                    val_row = val_data[val_data["code"] == stock]
                    if len(val_row) == 0:
                        continue

                    market_cap = float(val_row["circulating_market_cap"].iloc[0])

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
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "win": win,
                        }
                    )

                    day_signals += 1

                except:
                    continue

            print(f"    当日信号数: {day_signals}")

        except:
            continue

    if len(signals) > 0:
        df_s = pd.DataFrame(signals)

        jwr_signals = df_s[(df_s["open_pct"] >= 0.5) & (df_s["open_pct"] <= 1.5)]

        results[vname] = {
            "total": len(signals),
            "jwr_count": len(jwr_signals),
            "avg_return": df_s["intra_return"].mean(),
            "avg_max": df_s["max_return"].mean(),
            "win_rate": df_s["win"].mean() * 100,
            "jwr_return": jwr_signals["intra_return"].mean()
            if len(jwr_signals) > 0
            else 0,
            "daily_avg": len(signals) / len(test_dates_idx),
        }

        print(f"\n  5天总信号: {len(signals)}")
        print(f"  日均信号: {len(signals) / len(test_dates_idx):.2f}")
        print(f"  假弱高开: {len(jwr_signals)}")
        print(f"  日内收益: {df_s['intra_return'].mean():.2f}%")
        print(f"  胜率: {df_s['win'].mean() * 100:.2f}%")
        if len(jwr_signals) > 0:
            print(f"  假弱高开收益: {jwr_signals['intra_return'].mean():.2f}%")
    else:
        results[vname] = {
            "total": 0,
            "jwr_count": 0,
            "avg_return": 0,
            "avg_max": 0,
            "win_rate": 0,
            "jwr_return": 0,
            "daily_avg": 0,
        }
        print(f"\n  5天总信号: 0")

print("\n" + "=" * 60)
print("对比汇总")
print("=" * 60)

print("\n| 版本 | 5天信号 | 日均信号 | 假弱高开 | 日内收益 | 胜率 |")
print("|------|----------|----------|----------|----------|------|")

for vname in ["原版", "放宽A", "放宽B", "放宽C", "放宽D"]:
    if vname in results:
        r = results[vname]
        print(
            f"| {vname} | {r['total']} | {r['daily_avg']:.2f} | {r['jwr_count']} | {r['avg_return']:.2f}% | {r['win_rate']:.2f}% |"
        )

if "原版" in results and results["原版"]["total"] > 0:
    base = results["原版"]
    print("\n与原版对比:")
    for vname in ["放宽A", "放宽B", "放宽C", "放宽D"]:
        if vname in results:
            r = results[vname]
            print(
                f"  {vname}: 信号{r['total'] / base['total']:.2f}x, 收益{r['avg_return'] / base['avg_return'] if base['avg_return'] != 0 else 0:.2f}x"
            )

print("=" * 60)
