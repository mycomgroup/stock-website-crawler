# 主线信号放宽测试 - 精简版（采样测试）
from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("主线信号放宽测试 - 2024年采样测试")
print("=" * 80)

test_start = "2024-01-01"
test_end = "2024-12-31"

trade_days = get_trade_days(test_start, test_end)
sample_days = trade_days[::5]
print(f"测试期间: {test_start} ~ {test_end}")
print(f"采样策略: 每5天取1天，共{len(sample_days)}个测试日")

versions = {
    "原版": (50, 150, 0.30, "市值50-150亿+位置≤30%"),
    "放宽A": (40, 200, 0.30, "市值40-200亿+位置≤30%"),
    "放宽B": (50, 150, 0.50, "市值50-150亿+位置≤50%"),
    "放宽C": (40, 200, 0.50, "市值40-200亿+位置≤50%"),
    "放宽D": (30, 300, 0.50, "市值30-300亿+位置≤50%"),
}

results = {}

for version_name, (cap_min, cap_max, pos_max, desc) in versions.items():
    print(f"\n{'=' * 60}")
    print(f"测试版本: {version_name} - {desc}")
    print(f"{'=' * 60}")

    all_signals = []
    processed = 0

    for i, date in enumerate(sample_days):
        ds = date.strftime("%Y-%m-%d")
        if i % 10 == 0:
            print(f"  处理: {ds} ({i + 1}/{len(sample_days)})")

        try:
            prev_idx = trade_days.tolist().index(date) - 1
            if prev_idx < 0:
                continue
            prev_date = trade_days[prev_idx].strftime("%Y-%m-%d")

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.circulating_market_cap >= cap_min,
                valuation.circulating_market_cap <= cap_max,
            )
            df_val = get_fundamentals(q, date=ds)
            if df_val.empty:
                continue

            candidates = df_val["code"].tolist()

            for stock in candidates[:150]:
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
                        end_date=ds,
                        count=1,
                        fields=["open", "close", "high", "high_limit"],
                        panel=False,
                    )
                    if df_curr.empty:
                        continue

                    curr_open = float(df_curr["open"].iloc[0])
                    curr_close = float(df_curr["close"].iloc[0])
                    curr_high = float(df_curr["high"].iloc[0])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if not (-5.0 <= open_pct <= 5.0):
                        continue

                    df_pos = get_price(
                        stock, end_date=ds, count=15, fields=["close"], panel=False
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
                            "date": ds,
                            "stock": stock,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "win": win,
                        }
                    )

                except:
                    continue

            processed += 1

        except:
            continue

    if len(all_signals) > 0:
        df_signals = pd.DataFrame(all_signals)

        full_year_signals = len(all_signals) * (len(trade_days) / len(sample_days))

        results[version_name] = {
            "total_signals": int(full_year_signals),
            "sample_signals": len(all_signals),
            "avg_daily_signals": len(all_signals) / len(sample_days),
            "avg_intra_return": df_signals["intra_return"].mean(),
            "win_rate": df_signals["win"].mean() * 100,
            "avg_max_return": df_signals["max_return"].mean(),
            "signals_df": df_signals,
            "desc": desc,
        }

        print(f"\n结果（采样{processed}天）:")
        print(f"  样本信号数: {results[version_name]['sample_signals']}")
        print(f"  预估全年信号: {results[version_name]['total_signals']}")
        print(f"  日均信号: {results[version_name]['avg_daily_signals']:.2f}")
        print(f"  日内收益均值: {results[version_name]['avg_intra_return']:.2f}%")
        print(f"  胜率: {results[version_name]['win_rate']:.2f}%")
        print(f"  最大收益均值: {results[version_name]['avg_max_return']:.2f}%")

print("\n" + "=" * 80)
print("各版本对比汇总")
print("=" * 80)

print("\n| 版本 | 筛选条件 | 预估全年信号 | 日均信号 | 日内收益 | 胜率 | 最大收益 |")
print("|------|----------|-------------|----------|----------|------|----------|")

for vname in ["原版", "放宽A", "放宽B", "放宽C", "放宽D"]:
    if vname in results:
        r = results[vname]
        print(
            f"| {vname} | {r['desc']} | {r['total_signals']} | {r['avg_daily_signals']:.2f} | {r['avg_intra_return']:.2f}% | {r['win_rate']:.2f}% | {r['avg_max_return']:.2f}% |"
        )

print("\n" + "=" * 80)
print("与原版对比")
print("=" * 80)

if "原版" in results:
    base = results["原版"]
    print("\n| 版本 | 信号数提升 | 收益变化 | 胜率变化 | 通过门槛 |")
    print("|------|-----------|----------|----------|----------|")

    for vname in ["放宽A", "放宽B", "放宽C", "放宽D"]:
        if vname in results:
            r = results[vname]
            signal_mult = (
                r["total_signals"] / base["total_signals"]
                if base["total_signals"] > 0
                else 0
            )
            return_ratio = (
                r["avg_intra_return"] / base["avg_intra_return"]
                if base["avg_intra_return"] != 0
                else 0
            )
            win_ratio = r["win_rate"] / base["win_rate"] if base["win_rate"] > 0 else 0

            pass_gate = (
                "✅"
                if (signal_mult >= 2.0 and return_ratio >= 0.5 and win_ratio >= 0.8)
                else "❌"
            )

            print(
                f"| {vname} | {signal_mult:.2f}x | {return_ratio:.2f}x | {win_ratio:.2f}x | {pass_gate} |"
            )

print("\n" + "=" * 80)
print("假弱高开结构细分（+0.5%~+1.5%）")
print("=" * 80)

for vname in ["原版", "放宽A", "放宽B", "放宽C", "放宽D"]:
    if vname in results:
        df = results[vname]["signals_df"]
        df_jwr = df[(df["open_pct"] >= 0.5) & (df["open_pct"] <= 1.5)]

        if len(df_jwr) > 0:
            print(f"\n{vname} - 假弱高开结构（样本{len(df_jwr)}个）:")
            print(f"  日内收益均值: {df_jwr['intra_return'].mean():.2f}%")
            print(f"  胜率: {df_jwr['win'].mean() * 100:.2f}%")
            print(f"  最大收益均值: {df_jwr['max_return'].mean():.2f}%")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
