from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

"""
任务01：首板信号收敛 - 复核版
完全按照result_01的筛选标准，包含所有硬过滤条件

硬过滤条件：
1. 流通市值：50-150亿
2. 相对位置：≤30%（15日内）
3. 连板状态：近1日无涨停

测试期间：
- 训练期：2021-01-01 ~ 2023-12-31
- 验证期：2024-01-01 ~ 2024-12-31
- 样本外：2025-01-01 ~ 2025-12-31（如有）
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


def get_relative_position(prices):
    """计算相对位置"""
    if len(prices) < 2:
        return 1.0
    high_n = prices.max()
    low_n = prices.min()
    current = prices.iloc[-1]
    if high_n == low_n:
        return 0.5
    return (current - low_n) / (high_n - low_n)


print("=" * 80)
print("首板信号收敛分析 - 复核版（含硬过滤）")
print("=" * 80)

periods = {
    "训练期": ("2021-01-01", "2023-12-31"),
    "验证期": ("2024-01-01", "2024-12-31"),
    "样本外": ("2025-01-01", "2025-12-31"),
}

all_results = {}

for period_name, (start_date, end_date) in periods.items():
    print(f"\n{period_name}: {start_date} ~ {end_date}")
    print("-" * 80)

    signals = []

    trade_days = get_trade_days(start_date, end_date)
    print(f"交易日数: {len(trade_days)}")

    for i in range(1, len(trade_days)):
        curr_date = trade_days[i]
        prev_date = trade_days[i - 1]

        if i % 50 == 0:
            print(f"处理进度: {i}/{len(trade_days)} ({curr_date})")

        try:
            all_stocks = get_all_securities("stock", curr_date).index.tolist()

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

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock]
                    curr_row = price_curr[price_curr["code"] == stock]

                    if prev_row.empty or curr_row.empty:
                        continue

                    prev_close = float(prev_row["close"].iloc[0])
                    curr_open = float(curr_row["open"].iloc[0])
                    curr_close = float(curr_row["close"].iloc[0])
                    curr_high = float(curr_row["high"].iloc[0])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if not (-10 <= open_pct <= 10):
                        continue

                    q = query(valuation.code, valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    )
                    df_val = get_fundamentals(q, date=curr_date)

                    if df_val.empty:
                        continue

                    market_cap = float(df_val["circulating_market_cap"].iloc[0])

                    if not (50 <= market_cap <= 150):
                        continue

                    prices_15d = get_price(
                        stock,
                        end_date=prev_date,
                        count=15,
                        fields=["close"],
                        panel=False,
                    )

                    if prices_15d.empty or len(prices_15d) < 10:
                        continue

                    rel_position = get_relative_position(prices_15d["close"])

                    if rel_position > 0.30:
                        continue

                    lb_data = get_price(
                        stock,
                        end_date=prev_date,
                        count=2,
                        fields=["close", "high_limit"],
                        panel=False,
                    )

                    if len(lb_data) >= 2:
                        prev_prev_close = float(lb_data["close"].iloc[0])
                        prev_prev_limit = float(lb_data["high_limit"].iloc[0])

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
                            "rel_position": rel_position,
                        }
                    )

                except Exception as e:
                    continue

        except Exception as e:
            continue

    if len(signals) == 0:
        print(f"未找到信号")
        continue

    df = pd.DataFrame(signals)
    print(f"\n总计找到 {len(df)} 个信号（应用硬过滤后）")

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
            "avg_market_cap": subset["market_cap"].mean(),
            "avg_rel_position": subset["rel_position"].mean(),
        }

        type_stats.append(stats)

    results_df = pd.DataFrame(type_stats)
    results_df = results_df.sort_values("avg_max_return", ascending=False)

    print("\n结构分组收益对比:")
    print(
        results_df[
            ["open_type", "count", "avg_intra_return", "avg_max_return", "win_rate"]
        ].to_string(index=False)
    )

    all_results[period_name] = {
        "total_signals": len(df),
        "results": results_df.to_dict("records"),
    }

print("\n" + "=" * 80)
print("最终对比结果")
print("=" * 80)

for period_name, data in all_results.items():
    print(f"\n{period_name}: 总信号数 {data['total_signals']}")
    if data["results"]:
        for r in data["results"][:3]:
            print(
                f"  {r['open_type']}: {r['count']}个, 日内收益 {r['avg_intra_return']:.2f}%, 胜率 {r['win_rate']:.1f}%"
            )

print("\n分析完成！")
