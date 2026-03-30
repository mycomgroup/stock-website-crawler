from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

"""
任务01：首板信号收敛 - 高效版
只分析涨停板股票，提高效率
"""


def classify_open_type(open_pct):
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -1.0 <= open_pct < 0.0:
        return "真低开B"
    elif 0.0 <= open_pct < 0.5:
        return "边界A_平开附近"
    elif -5.0 <= open_pct < -3.0:
        return "边界B_深度低开"
    elif 1.5 <= open_pct <= 2.5:
        return "边界C_微高开"
    else:
        return "其他"


print("开始首板信号收敛分析（2024年，只分析涨停板）...")
print("=" * 80)

test_dates = [
    "2024-01-02",
    "2024-02-01",
    "2024-03-01",
    "2024-04-01",
    "2024-05-01",
    "2024-06-01",
    "2024-07-01",
    "2024-08-01",
    "2024-09-01",
    "2024-10-01",
    "2024-11-01",
    "2024-12-01",
]

signals = []

for i in range(len(test_dates)):
    curr_date = test_dates[i]

    try:
        prev_date = get_trade_days(end_date=curr_date, count=2)[0]

        price_prev = get_price(
            get_all_securities("stock", prev_date).index.tolist()[:1000],
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

        print(f"\n{curr_date}: 找到 {len(limit_stocks)} 个涨停板股票")

        if len(limit_stocks) == 0:
            continue

        price_curr = get_price(
            limit_stocks[:100],
            end_date=curr_date,
            count=1,
            fields=["open", "close", "high", "high_limit"],
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

                if -10 <= open_pct <= 10:
                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "open_type": classify_open_type(open_pct),
                            "is_win": intra_return > 0,
                        }
                    )
            except Exception as e:
                continue
    except Exception as e:
        continue

if len(signals) == 0:
    print("未找到任何首板信号")
    exit()

df = pd.DataFrame(signals)

print(f"\n总计找到 {len(df)} 个首板信号")

type_stats = []

for open_type in df["open_type"].unique():
    if open_type == "其他":
        continue

    subset = df[df["open_type"] == open_type]

    stats = {
        "open_type": open_type,
        "count": len(subset),
        "avg_open_pct": subset["open_pct"].mean(),
        "avg_intra_return": subset["intra_return"].mean(),
        "avg_max_return": subset["max_return"].mean(),
        "win_rate": subset["is_win"].sum() / len(subset) * 100,
        "min_open_pct": subset["open_pct"].min(),
        "max_open_pct": subset["open_pct"].max(),
    }

    type_stats.append(stats)

results_df = pd.DataFrame(type_stats)
results_df = results_df.sort_values("avg_max_return", ascending=False)

print("\n" + "=" * 80)
print("结构分组收益对比 (2024年样本)")
print("=" * 80)
print(results_df.to_string(index=False))

print("\n" + "=" * 80)
print("核心结论:")
print("=" * 80)

if len(results_df) > 0:
    best = results_df.iloc[0]
    print(f"\n最佳结构: {best['open_type']}")
    print(f"  - 信号数: {best['count']}")
    print(f"  - 日内收益均值: {best['avg_intra_return']:.2f}%")
    print(f"  - 最高收益均值: {best['avg_max_return']:.2f}%")
    print(f"  - 胜率: {best['win_rate']:.1f}%")

    if len(results_df) > 1:
        second = results_df.iloc[1]
        print(f"\n次优结构: {second['open_type']}")
        print(f"  - 信号数: {second['count']}")
        print(f"  - 日内收益均值: {second['avg_intra_return']:.2f}%")
        print(f"  - 最高收益均值: {second['avg_max_return']:.2f}%")
        print(f"  - 胜率: {second['win_rate']:.1f}%")

output_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output/first_board_convergence_2024.json"

import json
import os

os.makedirs(
    "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output",
    exist_ok=True,
)

output_data = {
    "timestamp": datetime.now().isoformat(),
    "total_signals": len(df),
    "results": results_df.to_dict("records"),
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存至: {output_file}")
print("\n分析完成！")
