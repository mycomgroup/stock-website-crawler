# 主线信号放宽测试 - 极简版（3版本+月度采样）
from jqdata import *
import pandas as pd

print("主线信号放宽测试 - 极简版")

test_start = "2024-01-01"
test_end = "2024-12-31"
trade_days = get_trade_days(test_start, test_end)

print(f"测试期间: {test_start} ~ {test_end}, 共{len(trade_days)}天")

sample_dates = [
    "2024-01-15",
    "2024-02-20",
    "2024-03-15",
    "2024-04-15",
    "2024-05-15",
    "2024-06-15",
    "2024-07-15",
    "2024-08-15",
    "2024-09-15",
    "2024-10-15",
    "2024-11-15",
    "2024-12-15",
]

print(f"采样日期: {len(sample_dates)}天")

versions = {
    "原版": (50, 150, 0.30),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

results = {}

for vname, (cap_min, cap_max, pos_max) in versions.items():
    print(f"\n{'=' * 50}")
    print(f"版本: {vname} (市值{cap_min}-{cap_max}亿, 位置≤{pos_max * 100}%)")
    print(f"{'=' * 50}")

    signals = []

    for idx, sample_date in enumerate(sample_dates):
        print(f"  处理: {sample_date} ({idx + 1}/{len(sample_dates)})")

        try:
            prev_idx = trade_days.tolist().index(pd.Timestamp(sample_date)) - 1
            if prev_idx < 0:
                continue
            prev_date = trade_days[prev_idx].strftime("%Y-%m-%d")

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.circulating_market_cap >= cap_min,
                valuation.circulating_market_cap <= cap_max,
            )
            df_val = get_fundamentals(q, date=sample_date)

            if df_val.empty:
                continue

            candidates = df_val["code"].tolist()[:100]

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
                        end_date=sample_date,
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

                    if not (-5.0 <= open_pct <= 5.0):
                        continue

                    df_pos = get_price(
                        stock,
                        end_date=sample_date,
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

                    signals.append(
                        {
                            "date": sample_date,
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

        full_year = int(len(signals) * (len(trade_days) / len(sample_dates)))

        results[vname] = {
            "total": full_year,
            "sample": len(signals),
            "daily_avg": len(signals) / len(sample_dates),
            "return_avg": df_s["intra_return"].mean(),
            "win_rate": df_s["win"].mean() * 100,
            "max_return": df_s["max_return"].mean(),
            "df": df_s,
        }

        print(f"\n  样本信号: {len(signals)}个")
        print(f"  预估全年: {full_year}个")
        print(f"  日均信号: {len(signals) / len(sample_dates):.2f}个")
        print(f"  日内收益: {df_s['intra_return'].mean():.2f}%")
        print(f"  胜率: {df_s['win'].mean() * 100:.2f}%")
        print(f"  最大收益: {df_s['max_return'].mean():.2f}%")

print("\n" + "=" * 80)
print("对比汇总")
print("=" * 80)

if len(results) > 0:
    print("\n| 版本 | 预估全年信号 | 日均信号 | 日内收益 | 胜率 | 最大收益 |")
    print("|------|-------------|----------|----------|------|----------|")

    for vname in ["原版", "放宽C", "放宽D"]:
        if vname in results:
            r = results[vname]
            print(
                f"| {vname} | {r['total']} | {r['daily_avg']:.2f} | {r['return_avg']:.2f}% | {r['win_rate']:.2f}% | {r['max_return']:.2f}% |"
            )

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
