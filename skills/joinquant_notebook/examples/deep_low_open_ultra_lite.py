from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

"""
任务09v2：深度低开专项验证 - 极速版
深度低开：-5%~-3%
只测试2024年2个关键月，快速验证
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


print("开始深度低开专项验证（极速版）...")
print("=" * 80)

test_dates = ["2024-03-01", "2024-11-01"]
signals = []

for curr_date in test_dates:
    print(f"\n处理 {curr_date}...")
    try:
        prev_date = get_trade_days(end_date=curr_date, count=2)[0]
        prev_date = str(prev_date)
        curr_date = str(curr_date)

        all_stocks = get_all_securities("stock", prev_date).index.tolist()[:500]

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

        print(f"  涨停板数量：{len(limit_stocks)}")

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

print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

if len(signals) == 0:
    print("未找到任何信号")
else:
    df = pd.DataFrame(signals)
    print(f"\n总信号数：{len(df)}")

    type_stats = []

    for open_type in df["open_type"].unique():
        if open_type == "其他":
            continue

        subset = df[df["open_type"] == open_type]

        stats = {
            "open_type": open_type,
            "count": len(subset),
            "avg_intra_return": subset["intra_return"].mean(),
            "avg_max_return": subset["max_return"].mean(),
            "win_rate": subset["is_win"].sum() / len(subset) * 100,
        }

        type_stats.append(stats)

    results_df = pd.DataFrame(type_stats)
    results_df = results_df.sort_values("avg_intra_return", ascending=False)

    print("\n结构分组收益对比：")
    print("=" * 80)
    print(results_df.to_string(index=False))

    deep_low = df[df["open_type"] == "边界B_深度低开"]

    print("\n" + "=" * 80)
    print("深度低开专项分析")
    print("=" * 80)

    if len(deep_low) > 0:
        print(f"\n深度低开样本数：{len(deep_low)}")
        print(f"平均日内收益：{deep_low['intra_return'].mean():.2f}%")
        print(f"胜率：{deep_low['is_win'].sum() / len(deep_low) * 100:.1f}%")
        print(
            f"开盘涨跌幅范围：{deep_low['open_pct'].min():.2f}% ~ {deep_low['open_pct'].max():.2f}%"
        )

        print("\n判定：")
        if (
            deep_low["intra_return"].mean() < 0
            and deep_low["is_win"].sum() / len(deep_low) * 100 < 30
        ):
            print("  删除 - 样本少且收益负、胜率极低")
        else:
            print("  需更多样本验证")
    else:
        print("\n无深度低开样本")
        print("判定：删除 - 样本不存在")

print("\n分析完成！")
