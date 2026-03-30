from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

"""
任务01重做：首板信号收敛 - 全量2024数据
使用与原始研究一致的筛选标准
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


print("开始首板信号收敛分析（2024全年，完整筛选标准）...")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
start_idx = all_dates_2024.index("2024-01-02") if "2024-01-02" in all_dates_2024 else 0
test_dates = all_dates_2024[start_idx:]

print(f"测试期间：2024-01-02 到 2024-12-31，共 {len(test_dates)} 个交易日")

signals = []
total_zt_count = 0

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    if i % 20 == 0:
        print(f"处理进度：{i}/{len(test_dates)} ({i / len(test_dates) * 100:.1f}%)")

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

        total_zt_count += len(limit_stocks)

        if len(limit_stocks) == 0:
            continue

        price_curr = get_price(
            limit_stocks,
            end_date=curr_date,
            count=1,
            fields=["open", "close", "high", "high_limit"],
            panel=False,
        )

        if price_curr.empty:
            continue

        q = query(
            valuation.code,
            valuation.circulating_market_cap,
        ).filter(valuation.code.in_(limit_stocks))

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

                if -10 <= open_pct <= 10:
                    val_row = val_data[val_data["code"] == stock]
                    if len(val_row) == 0:
                        continue

                    market_cap = float(val_row["circulating_market_cap"].iloc[0])

                    if not (50 <= market_cap <= 150):
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

                    if position > 0.30:
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

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "open_type": classify_open_type(open_pct),
                            "is_win": intra_return > 0,
                            "market_cap": market_cap,
                            "position": position,
                        }
                    )
            except Exception as e:
                continue
    except Exception as e:
        continue

if len(signals) == 0:
    print("未找到任何首板信号")
else:
    df = pd.DataFrame(signals)

    print(f"\n总计涨停板天数：{total_zt_count}")
    print(f"筛选后首板信号：{len(df)} 个")
    print(f"平均每日信号：{len(df) / len(test_dates):.2f} 个")

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
    print("结构分组收益对比 (2024全年，完整筛选)")
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

    print("\n" + "=" * 80)
    print("数据质量验证:")
    print("=" * 80)

    if "假弱高开" in results_df["open_type"].values:
        jw_row = results_df[results_df["open_type"] == "假弱高开"].iloc[0]
        print(f"\n假弱高开结构:")
        print(f"  原研究收益: +0.77%")
        print(f"  本次实测收益: {jw_row['avg_intra_return']:.2f}%")
        print(f"  差异: {jw_row['avg_intra_return'] - 0.77:.2f}%")
        print(f"  原研究样本: 68个")
        print(f"  本次实测样本: {jw_row['count']}个")

    if "真低开A" in results_df["open_type"].values:
        zk_row = results_df[results_df["open_type"] == "真低开A"].iloc[0]
        print(f"\n真低开A结构:")
        print(f"  原研究收益: +0.79%")
        print(f"  本次实测收益: {zk_row['avg_intra_return']:.2f}%")
        print(f"  差异: {zk_row['avg_intra_return'] - 0.79:.2f}%")
        print(f"  原研究样本: 61个")
        print(f"  本次实测样本: {zk_row['count']}个")

print("\n分析完成！")
