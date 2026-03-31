# 主线信号放宽测试 - 假弱高开结构对比
from jqdata import *
import pandas as pd

print("主线信号放宽测试 - 假弱高开结构对比")

trade_days = get_trade_days("2024-01-01", "2024-12-31")
print(f"全年交易日数: {len(trade_days)}")

test_periods = [
    {"name": "1月初", "indices": [5, 6, 7, 8, 9]},
    {"name": "2月初", "indices": [25, 26, 27, 28, 29]},
    {"name": "3月初", "indices": [40, 41, 42, 43, 44]},
    {"name": "6月初", "indices": [100, 101, 102, 103, 104]},
]

versions = {
    "原版_假弱高开": (50, 150, 0.30, 0.5, 1.5),
    "放宽C_假弱高开": (40, 200, 0.50, 0.5, 1.5),
}

all_results = {}

for period in test_periods:
    print(f"\n{'=' * 60}")
    print(f"时间段: {period['name']}")
    print(f"{'=' * 60}")

    period_results = {}

    for vname, (cap_min, cap_max, pos_max, open_min, open_max) in versions.items():
        print(f"\n版本: {vname}")

        signals = []

        for idx in period["indices"]:
            if idx >= len(trade_days) or idx < 1:
                continue

            prev_date = trade_days[idx - 1].strftime("%Y-%m-%d")
            curr_date = trade_days[idx].strftime("%Y-%m-%d")

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

                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code.in_(limit_stocks),
                    valuation.circulating_market_cap >= cap_min,
                    valuation.circulating_market_cap <= cap_max,
                )

                val_data = get_fundamentals(q, date=curr_date)

                if val_data.empty:
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

                        if not (-10 <= open_pct <= 10):
                            continue

                        if not (open_min <= open_pct <= open_max):
                            continue

                        val_row = val_data[val_data["code"] == stock]
                        if len(val_row) == 0:
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
                                "open_pct": open_pct,
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

            period_results[vname] = {
                "total": len(signals),
                "avg_return": df_s["intra_return"].mean(),
                "win_rate": df_s["win"].mean() * 100,
                "avg_max": df_s["max_return"].mean(),
            }

            print(f"  信号: {len(signals)}")
            print(f"  收益: {df_s['intra_return'].mean():.2f}%")
            print(f"  胜率: {df_s['win'].mean() * 100:.2f}%")
            print(f"  最大收益: {df_s['max_return'].mean():.2f}%")
        else:
            period_results[vname] = {
                "total": 0,
                "avg_return": 0,
                "win_rate": 0,
                "avg_max": 0,
            }
            print(f"  信号: 0")

    all_results[period["name"]] = period_results

print("\n" + "=" * 60)
print("假弱高开结构对比汇总")
print("=" * 60)

print("\n时间段 | 版本 | 信号 | 收益 | 胜率 | 最大收益")
print("-------|------|------|------|------|----------")

for period_name in ["1月初", "2月初", "3月初", "6月初"]:
    if period_name in all_results:
        for vname in ["原版_假弱高开", "放宽C_假弱高开"]:
            if vname in all_results[period_name]:
                r = all_results[period_name][vname]
                print(
                    f"{period_name} | {vname.replace('_假弱高开', '')} | {r['total']} | {r['avg_return']:.2f}% | {r['win_rate']:.2f}% | {r['avg_max']:.2f}%"
                )

print("\n" + "=" * 60)
print("汇总统计（20天）")
print("=" * 60)

for vname in ["原版_假弱高开", "放宽C_假弱高开"]:
    total_signals = 0
    returns = []
    max_returns = []

    for period_name in ["1月初", "2月初", "3月初", "6月初"]:
        if period_name in all_results and vname in all_results[period_name]:
            total_signals += all_results[period_name][vname]["total"]
            if all_results[period_name][vname]["avg_return"] != 0:
                returns.append(all_results[period_name][vname]["avg_return"])
                max_returns.append(all_results[period_name][vname]["avg_max"])

    avg_return = sum(returns) / len(returns) if len(returns) > 0 else 0
    avg_max = sum(max_returns) / len(max_returns) if len(max_returns) > 0 else 0
    daily_avg = total_signals / 20
    full_year = int(daily_avg * 242)

    print(f"\n{vname}:")
    print(f"  20天总信号: {total_signals}")
    print(f"  日均信号: {daily_avg:.2f}")
    print(f"  预估全年: {full_year}")
    print(f"  平均收益: {avg_return:.2f}%")
    print(f"  平均最大收益: {avg_max:.2f}%")

if "原版_假弱高开" in all_results.get(
    "1月初", {}
) and "放宽C_假弱高开" in all_results.get("1月初", {}):
    total_orig = 0
    total_relaxed = 0

    for period_name in ["1月初", "2月初", "3月初", "6月初"]:
        if period_name in all_results:
            total_orig += all_results[period_name]["原版_假弱高开"]["total"]
            total_relaxed += all_results[period_name]["放宽C_假弱高开"]["total"]

    if total_orig > 0:
        signal_mult = total_relaxed / total_orig
        print(f"\n信号数量提升: {signal_mult:.2f}x")

print("=" * 60)
