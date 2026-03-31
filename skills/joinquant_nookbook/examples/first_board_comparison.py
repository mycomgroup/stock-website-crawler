from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

"""
首板信号收敛 - 对比分析版
重点对比result_01数据差异，只测试2024年Q4（10-12月）
"""


def classify_open_type(open_pct):
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -1.0 <= open_pct < 0.0:
        return "真低开B"
    elif 0.0 <= open_pct < 0.5:
        return "平开附近"
    elif -5.0 <= open_pct < -3.0:
        return "深度低开"
    elif 1.5 <= open_pct <= 2.5:
        return "微高开"
    else:
        return "其他"


print("=" * 80)
print("首板信号收敛 - 对比分析（2024年Q4，含硬过滤）")
print("=" * 80)

test_dates = ["2024-10-01", "2024-11-01", "2024-12-01"]

signals_no_filter = []
signals_with_filter = []

for curr_date_str in test_dates:
    print(f"\n处理日期: {curr_date_str}")

    curr_date = curr_date_str
    trade_days = get_trade_days(end_date=curr_date, count=2)
    prev_date = str(trade_days[0])

    all_stocks = get_all_securities("stock", curr_date).index.tolist()
    print(f"  总股票数: {len(all_stocks)}")

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
        abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
        < 0.01
    ]["code"].tolist()

    print(f"  涨停板股票: {len(limit_stocks)}")

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

            intra_return = (curr_close - curr_open) / curr_open * 100

            signals_no_filter.append(
                {
                    "date": curr_date,
                    "stock": stock,
                    "open_pct": open_pct,
                    "intra_return": intra_return,
                    "open_type": classify_open_type(open_pct),
                    "is_win": intra_return > 0,
                }
            )

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
                stock, end_date=prev_date, count=15, fields=["close"], panel=False
            )

            if prices_15d.empty or len(prices_15d) < 10:
                continue

            high_15d = float(prices_15d["close"].max())
            low_15d = float(prices_15d["close"].min())
            current_price = float(prices_15d["close"].iloc[-1])

            if high_15d == low_15d:
                rel_position = 0.5
            else:
                rel_position = (current_price - low_15d) / (high_15d - low_15d)

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

                if abs(prev_prev_close - prev_prev_limit) / prev_prev_limit < 0.01:
                    continue

            signals_with_filter.append(
                {
                    "date": curr_date,
                    "stock": stock,
                    "open_pct": open_pct,
                    "intra_return": intra_return,
                    "open_type": classify_open_type(open_pct),
                    "is_win": intra_return > 0,
                    "market_cap": market_cap,
                    "rel_position": rel_position,
                }
            )

        except Exception as e:
            continue

print("\n" + "=" * 80)
print("对比分析结果")
print("=" * 80)

df_no_filter = pd.DataFrame(signals_no_filter)
df_with_filter = pd.DataFrame(signals_with_filter)

print(f"\n无过滤信号数: {len(df_no_filter)}")
print(f"有硬过滤信号数: {len(df_with_filter)}")

if len(df_no_filter) > 0:
    print("\n无过滤结构收益:")
    for open_type in df_no_filter["open_type"].unique():
        if open_type == "其他":
            continue
        subset = df_no_filter[df_no_filter["open_type"] == open_type]
        avg_ret = subset["intra_return"].mean()
        win_rate = subset["is_win"].sum() / len(subset) * 100
        print(
            f"  {open_type}: {len(subset)}个, 收益 {avg_ret:.2f}%, 胜率 {win_rate:.1f}%"
        )

if len(df_with_filter) > 0:
    print("\n有硬过滤结构收益:")
    for open_type in df_with_filter["open_type"].unique():
        if open_type == "其他":
            continue
        subset = df_with_filter[df_with_filter["open_type"] == open_type]
        avg_ret = subset["intra_return"].mean()
        win_rate = subset["is_win"].sum() / len(subset) * 100
        print(
            f"  {open_type}: {len(subset)}个, 收益 {avg_ret:.2f}%, 胜率 {win_rate:.1f}%"
        )

print("\n分析完成！")
