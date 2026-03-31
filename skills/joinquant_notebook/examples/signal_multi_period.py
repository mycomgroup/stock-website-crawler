# 主线信号放宽测试 - 多时间段对比
from jqdata import *
import pandas as pd

print("主线信号放宽测试 - 多时间段对比")

trade_days = get_trade_days("2024-01-01", "2024-12-31")

test_periods = [
    {"name": "1月", "indices": range(5, 15)},
    {"name": "3月", "indices": range(40, 50)},
    {"name": "9月", "indices": range(170, 180)},
]

versions = {
    "原版": (50, 150, 0.30),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

all_results = {}

for period in test_periods:
    print(f"\n{'=' * 60}")
    print(f"时间段: {period['name']}")
    print(f"{'=' * 60}")

    period_results = {}

    for vname, (cap_min, cap_max, pos_max) in versions.items():
        print(f"\n版本: {vname}")

        all_signals = []

        for idx in period["indices"]:
            if idx >= len(trade_days) or idx < 1:
                continue

            test_date_obj = trade_days[idx]
            test_date = test_date_obj.strftime("%Y-%m-%d")
            prev_date_obj = trade_days[idx - 1]
            prev_date = prev_date_obj.strftime("%Y-%m-%d")

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.circulating_market_cap >= cap_min,
                valuation.circulating_market_cap <= cap_max,
            )
            df_val = get_fundamentals(q, date=test_date)

            if df_val.empty:
                continue

            candidates = df_val["code"].tolist()

            for stock in candidates:
                try:
                    df_prev = get_price(
                        stock,
                        end_date=prev_date,
                        count=1,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    if df_prev.empty:
                        continue

                    prev_close = float(df_prev["close"].iloc[0])
                    prev_limit = float(df_prev["high_limit"].iloc[0])

                    if abs(prev_close - prev_limit) / prev_limit > 0.01:
                        continue

                    df_curr = get_price(
                        stock,
                        end_date=test_date,
                        count=1,
                        fields=["open", "close", "high"],
                        panel=False,
                    )
                    if df_curr.empty:
                        continue

                    curr_open = float(df_curr["open"].iloc[0])
                    curr_close = float(df_curr["close"].iloc[0])
                    curr_high = float(df_curr["high"].iloc[0])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    df_pos = get_price(
                        stock,
                        end_date=test_date,
                        count=15,
                        fields=["close"],
                        panel=False,
                    )
                    if len(df_pos) < 5:
                        continue

                    high_15d = float(df_pos["close"].max())
                    low_15d = float(df_pos["close"].min())
                    if high_15d == low_15d:
                        continue

                    position = (df_pos["close"].iloc[-1] - low_15d) / (
                        high_15d - low_15d
                    )
                    if position > pos_max:
                        continue

                    df_lb = get_price(
                        stock,
                        end_date=prev_date,
                        count=2,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    if len(df_lb) >= 2:
                        prev_prev_close = float(df_lb["close"].iloc[-2])
                        prev_prev_limit = float(df_lb["high_limit"].iloc[-2])
                        if (
                            abs(prev_prev_close - prev_prev_limit) / prev_prev_limit
                            < 0.01
                        ):
                            continue

                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100
                    win = 1 if curr_close > curr_open else 0

                    all_signals.append(
                        {
                            "date": test_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "win": win,
                        }
                    )

                except:
                    continue

        if len(all_signals) > 0:
            df_s = pd.DataFrame(all_signals)

            jwr_signals = df_s[(df_s["open_pct"] >= 0.5) & (df_s["open_pct"] <= 1.5)]

            period_results[vname] = {
                "total": len(all_signals),
                "jwr_count": len(jwr_signals),
                "avg_return": df_s["intra_return"].mean(),
                "win_rate": df_s["win"].mean() * 100,
                "jwr_return": jwr_signals["intra_return"].mean()
                if len(jwr_signals) > 0
                else 0,
            }

            print(f"  总信号: {len(all_signals)}, 假弱高开: {len(jwr_signals)}")
            print(f"  收益: {df_s['intra_return'].mean():.2f}%")
            if len(jwr_signals) > 0:
                print(f"  假弱高开收益: {jwr_signals['intra_return'].mean():.2f}%")
        else:
            period_results[vname] = {
                "total": 0,
                "jwr_count": 0,
                "avg_return": 0,
                "win_rate": 0,
                "jwr_return": 0,
            }
            print(f"  总信号: 0")

    all_results[period["name"]] = period_results

print("\n" + "=" * 60)
print("各时间段对比汇总")
print("=" * 60)

for period_name in ["1月", "3月", "9月"]:
    if period_name in all_results:
        print(f"\n{period_name}:")
        print("| 版本 | 总信号 | 假弱高开 | 收益 | 假弱高开收益 |")
        print("|------|--------|----------|------|-------------|")

        for vname in ["原版", "放宽C", "放宽D"]:
            if vname in all_results[period_name]:
                r = all_results[period_name][vname]
                print(
                    f"| {vname} | {r['total']} | {r['jwr_count']} | {r['avg_return']:.2f}% | {r['jwr_return']:.2f}% |"
                )

print("\n" + "=" * 60)
print("全年预估（基于30天采样）")
print("=" * 60)

print("\n| 版本 | 30天信号 | 日均信号 | 预估全年 | 平均收益 | 平均胜率 |")
print("|------|----------|----------|----------|----------|----------|")

for vname in ["原版", "放宽C", "放宽D"]:
    total_30 = 0
    returns = []

    for period_name in ["1月", "3月", "9月"]:
        if period_name in all_results and vname in all_results[period_name]:
            total_30 += all_results[period_name][vname]["total"]
            if all_results[period_name][vname]["avg_return"] != 0:
                returns.append(all_results[period_name][vname]["avg_return"])

    avg_return = sum(returns) / len(returns) if len(returns) > 0 else 0
    daily_avg = total_30 / 30
    full_year = int(daily_avg * 242)

    print(
        f"| {vname} | {total_30} | {daily_avg:.2f} | {full_year} | {avg_return:.2f}% | - |"
    )

print("=" * 60)
