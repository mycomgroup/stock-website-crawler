# 主线信号放宽测试 - 对比不同筛选条件
from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 80)
print("主线信号放宽测试 - 2024全年")
print("=" * 80)

test_start = "2024-01-01"
test_end = "2024-12-31"

trade_days = get_trade_days(test_start, test_end)
print(f"测试期间: {test_start} ~ {test_end}, 共{len(trade_days)}个交易日")

versions = {
    "原版": (50, 150, 0.30, "市值50-150亿+位置≤30%+无连板"),
    "放宽A": (40, 200, 0.30, "市值40-200亿+位置≤30%+无连板"),
    "放宽B": (50, 150, 0.50, "市值50-150亿+位置≤50%+无连板"),
    "放宽C": (40, 200, 0.50, "市值40-200亿+位置≤50%+无连板"),
    "放宽D": (30, 300, 0.50, "市值30-300亿+位置≤50%+无连板"),
}

results = {}

for version_name, (cap_min, cap_max, pos_max, desc) in versions.items():
    print(f"\n{'=' * 60}")
    print(f"测试版本: {version_name} - {desc}")
    print(f"{'=' * 60}")

    all_signals = []
    signal_count = 0
    daily_signals = []

    for i, date in enumerate(trade_days):
        ds = date.strftime("%Y-%m-%d")
        if i % 50 == 0:
            print(f"处理中: {ds} ({i + 1}/{len(trade_days)})")

        try:
            prev_date = trade_days[i - 1].strftime("%Y-%m-%d") if i > 0 else None
            if not prev_date:
                continue

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.circulating_market_cap >= cap_min,
                valuation.circulating_market_cap <= cap_max,
            )
            df_val = get_fundamentals(q, date=ds)
            if df_val.empty:
                continue

            candidates = df_val["code"].tolist()
            daily_count = 0

            for stock in candidates[:200]:
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
                        fields=["open", "close", "high", "low", "high_limit"],
                        panel=False,
                    )
                    if df_curr.empty:
                        continue

                    curr_open = float(df_curr["open"].iloc[0])
                    curr_close = float(df_curr["close"].iloc[0])
                    curr_high = float(df_curr["high"].iloc[0])
                    curr_low = float(df_curr["low"].iloc[0])
                    high_limit = float(df_curr["high_limit"].iloc[0])

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
                            "cap": df_val[df_val["code"] == stock][
                                "circulating_market_cap"
                            ].iloc[0],
                        }
                    )

                    signal_count += 1
                    daily_count += 1

                except Exception as e:
                    continue

            daily_signals.append(daily_count)

        except Exception as e:
            continue

    if len(all_signals) > 0:
        df_signals = pd.DataFrame(all_signals)

        results[version_name] = {
            "total_signals": len(all_signals),
            "avg_daily_signals": len(all_signals) / len(trade_days),
            "avg_intra_return": df_signals["intra_return"].mean(),
            "win_rate": df_signals["win"].mean() * 100,
            "avg_max_return": df_signals["max_return"].mean(),
            "signals_df": df_signals,
            "desc": desc,
        }

        print(f"\n结果汇总:")
        print(f"  总信号数: {results[version_name]['total_signals']}")
        print(f"  每日平均信号: {results[version_name]['avg_daily_signals']:.2f}")
        print(f"  日内收益均值: {results[version_name]['avg_intra_return']:.2f}%")
        print(f"  胜率: {results[version_name]['win_rate']:.2f}%")
        print(f"  最大收益均值: {results[version_name]['avg_max_return']:.2f}%")

print("\n" + "=" * 80)
print("各版本对比汇总")
print("=" * 80)

print("\n| 版本 | 筛选条件 | 信号数 | 日均信号 | 日内收益 | 胜率 | 最大收益 |")
print("|------|----------|--------|----------|----------|------|----------|")

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
            print(f"\n{vname} - 假弱高开结构:")
            print(f"  信号数: {len(df_jwr)}")
            print(f"  日内收益均值: {df_jwr['intra_return'].mean():.2f}%")
            print(f"  胜率: {df_jwr['win'].mean() * 100:.2f}%")
            print(f"  最大收益均值: {df_jwr['max_return'].mean():.2f}%")

print("\n" + "=" * 80)
print("样本外验证（2024-07-01后）")
print("=" * 80)

out_sample_date = "2024-07-01"

for vname in ["原版", "放宽A", "放宽B", "放宽C", "放宽D"]:
    if vname in results:
        df = results[vname]["signals_df"]
        df_out = df[df["date"] >= out_sample_date]

        if len(df_out) > 0:
            print(f"\n{vname} - 样本外结果（{out_sample_date}后）:")
            print(f"  信号数: {len(df_out)}")
            print(f"  日内收益均值: {df_out['intra_return'].mean():.2f}%")
            print(f"  胜率: {df_out['win'].mean() * 100:.2f}%")
            print(f"  最大收益均值: {df_out['max_return'].mean():.2f}%")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
