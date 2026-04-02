from jqdata import *
import pandas as pd
import numpy as np

"""
v2任务07: 主线二板组合测试
分析主线与二板信号的重叠情况
"""

print("=" * 60)
print("v2任务07: 主线二板组合测试")
print("=" * 60)

test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-01-02"]

print(f"\n研究期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"交易日数: {len(test_dates)}")

mainline_signals = []
second_board_signals = []

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    if i % 50 == 0:
        print(f"进度: {i}/{len(test_dates)}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()

        price_prev = get_price(
            all_stocks[:2000],
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
            limit_stocks[:100],
            end_date=curr_date,
            count=1,
            fields=["open", "close", "high"],
            panel=False,
        )

        if price_curr.empty:
            continue

        for stock in limit_stocks[:100]:
            try:
                prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                prev_close = float(prev_row["close"])
                curr_open = float(curr_row["open"])
                curr_close = float(curr_row["close"])
                curr_high = float(curr_row["high"])

                open_pct = (curr_open - prev_close) / prev_close * 100

                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code == stock
                )
                val = get_fundamentals(q, date=curr_date)

                if val.empty:
                    continue

                market_cap = float(val["circulating_market_cap"].iloc[0])

                intra_return = (curr_close - curr_open) / curr_open * 100
                max_return = (curr_high - curr_open) / curr_open * 100

                signal = {
                    "date": curr_date,
                    "stock": stock,
                    "open_pct": open_pct,
                    "intra_return": intra_return,
                    "max_return": max_return,
                    "market_cap": market_cap,
                }

                if 0.5 <= open_pct <= 1.5 and 50 <= market_cap <= 150:
                    mainline_signals.append(signal)

                if -3 <= open_pct <= 3 and market_cap <= 500:
                    second_board_signals.append(signal)

            except:
                continue
    except:
        continue

print(f"\n主线信号(假弱高开): {len(mainline_signals)}个")
print(f"二板信号: {len(second_board_signals)}个")

mainline_set = set((s["date"], s["stock"]) for s in mainline_signals)
second_board_set = set((s["date"], s["stock"]) for s in second_board_signals)

overlap = mainline_set & second_board_set

print(f"\n重叠信号: {len(overlap)}个")
print(f"重叠比例: {len(overlap) / len(mainline_set) * 100:.1f}% (相对于主线)")

print("\n" + "=" * 60)
print("各版本收益对比")
print("=" * 60)

mainline_df = pd.DataFrame(mainline_signals)
second_board_df = pd.DataFrame(second_board_signals)

if len(mainline_df) > 0:
    print(f"\n主线单独:")
    print(f"  信号数: {len(mainline_df)}")
    print(
        f"  胜率: {len(mainline_df[mainline_df['intra_return'] > 0]) / len(mainline_df) * 100:.1f}%"
    )
    print(f"  日内收益: {mainline_df['intra_return'].mean():.2f}%")

if len(second_board_df) > 0:
    print(f"\n二板单独:")
    print(f"  信号数: {len(second_board_df)}")
    print(
        f"  胜率: {len(second_board_df[second_board_df['intra_return'] > 0]) / len(second_board_df) * 100:.1f}%"
    )
    print(f"  日内收益: {second_board_df['intra_return'].mean():.2f}%")

overlap_signals = [s for s in mainline_signals if (s["date"], s["stock"]) in overlap]
if len(overlap_signals) > 0:
    overlap_df = pd.DataFrame(overlap_signals)
    print(f"\n重叠信号:")
    print(f"  信号数: {len(overlap_df)}")
    print(
        f"  胜率: {len(overlap_df[overlap_df['intra_return'] > 0]) / len(overlap_df) * 100:.1f}%"
    )
    print(f"  日内收益: {overlap_df['intra_return'].mean():.2f}%")

print("\n" + "=" * 60)
print("组合建议")
print("=" * 60)

if len(overlap) < len(mainline_set) * 0.3:
    print("\n建议: ✓ 主线和二板可以并行运行")
    print("  - 重叠比例较低，两线信号独立性强")
    print("  - 可以同时参与，增加整体信号数量")
    print("  - 建议各分配50%仓位")
else:
    print("\n建议: ⚠️ 主线和二板存在较高重叠")
    print("  - 重叠比例较高，两线信号重叠明显")
    print("  - 建议选择其一运行，或设置优先级")
    print("  - 重叠时选择收益更高的版本")

print("\n分析完成！")
