# 完整全年回测 - 优化版（先筛选市值范围）
from jqdata import *
import pandas as pd

print("=" * 80)
print("主线信号完整回测 - 2024全年（优化版）")
print("=" * 80)

trade_days = get_trade_days("2024-01-01", "2024-12-31")
print(f"全年交易日数: {len(trade_days)}")


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
    else:
        return "其他"


signals = []

print("\n开始处理...")

for i in range(1, len(trade_days)):
    prev_date = trade_days[i - 1]
    curr_date = trade_days[i]

    if i % 20 == 0:
        print(
            f"进度: {i}/{len(trade_days)} ({i / len(trade_days) * 100:.1f}%) - 累计信号: {len(signals)}"
        )

    try:
        q_cap = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.circulating_market_cap >= 40,
            valuation.circulating_market_cap <= 200,
        )

        df_cap = get_fundamentals(q_cap, date=curr_date)

        if df_cap.empty:
            continue

        candidates = df_cap["code"].tolist()

        price_prev = get_price(
            candidates,
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
                prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                prev_close = float(prev_row["close"])
                curr_open = float(curr_row["open"])
                curr_close = float(curr_row["close"])
                curr_high = float(curr_row["high"])

                open_pct = (curr_open - prev_close) / prev_close * 100

                if not (-10 <= open_pct <= 10):
                    continue

                market_cap = float(
                    df_cap[df_cap["code"] == stock]["circulating_market_cap"].iloc[0]
                )

                prices_15d = get_price(
                    stock, end_date=prev_date, count=15, fields=["close"], panel=False
                )

                if len(prices_15d) < 10:
                    continue

                high_15d = float(prices_15d["close"].max())
                low_15d = float(prices_15d["close"].min())

                if high_15d == low_15d:
                    continue

                position = (prev_close - low_15d) / (high_15d - low_15d)

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

                    if abs(prev_prev_close - prev_prev_limit) / prev_prev_limit < 0.01:
                        continue

                intra_return = (curr_close - curr_open) / curr_open * 100
                max_return = (curr_high - curr_open) / curr_open * 100
                win = 1 if intra_return > 0 else 0
                open_type = classify_open_type(open_pct)

                signals.append(
                    {
                        "date": curr_date.strftime("%Y-%m-%d"),
                        "stock": stock,
                        "open_pct": open_pct,
                        "intra_return": intra_return,
                        "max_return": max_return,
                        "win": win,
                        "open_type": open_type,
                        "market_cap": market_cap,
                        "position": position,
                    }
                )

            except:
                continue

    except:
        continue

print(f"\n最终进度: {len(trade_days)}/{len(trade_days)} (100%)")

if len(signals) > 0:
    df = pd.DataFrame(signals)

    print(f"\n全年总信号: {len(df)}")
    print(f"日均信号: {len(df) / len(trade_days):.2f}")

    print("\n按市值分组:")
    cap_ranges = [(30, 300), (40, 200), (50, 150)]
    for cap_min, cap_max in cap_ranges:
        subset = df[(df["market_cap"] >= cap_min) & (df["market_cap"] <= cap_max)]
        print(f"  市值{cap_min}-{cap_max}亿: {len(subset)}个")

    print("\n按位置分组:")
    pos_thresholds = [0.30, 0.40, 0.50]
    for pos_max in pos_thresholds:
        subset = df[df["position"] <= pos_max]
        print(
            f"  位置≤{pos_max * 100}%: {len(subset)}个, 收益{subset['intra_return'].mean():.2f}%"
        )

    print("\n按开盘类型分组:")
    open_types = ["假弱高开", "真低开A", "真低开B", "平开附近", "深度低开"]
    for ot in open_types:
        subset = df[df["open_type"] == ot]
        if len(subset) > 0:
            print(
                f"  {ot}: {len(subset)}个, 收益{subset['intra_return'].mean():.2f}%, 胜率{subset['win'].mean() * 100:.2f}%"
            )

    print("\n组合筛选结果:")

    orig_jwr = df[
        (df["market_cap"] >= 50)
        & (df["market_cap"] <= 150)
        & (df["position"] <= 0.30)
        & (df["open_type"] == "假弱高开")
    ]
    print(
        f"原版(假弱高开): {len(orig_jwr)}个, 收益{orig_jwr['intra_return'].mean():.2f}%, 胜率{orig_jwr['win'].mean() * 100:.2f}%"
    )

    relaxed_jwr = df[
        (df["market_cap"] >= 40)
        & (df["market_cap"] <= 200)
        & (df["position"] <= 0.50)
        & (df["open_type"] == "假弱高开")
    ]
    print(
        f"放宽C(假弱高开): {len(relaxed_jwr)}个, 收益{relaxed_jwr['intra_return'].mean():.2f}%, 胜率{relaxed_jwr['win'].mean() * 100:.2f}%"
    )

    orig_true_low = df[
        (df["market_cap"] >= 50)
        & (df["market_cap"] <= 150)
        & (df["position"] <= 0.30)
        & (df["open_type"] == "真低开A")
    ]
    print(f"原版(真低开A): {len(orig_true_low)}个")

    relaxed_true_low = df[
        (df["market_cap"] >= 40)
        & (df["market_cap"] <= 200)
        & (df["position"] <= 0.50)
        & (df["open_type"] == "真低开A")
    ]
    print(f"放宽C(真低开A): {len(relaxed_true_low)}个")

    print("\n参数优化（位置阈值）:")
    for pos_max in [0.30, 0.35, 0.40, 0.45, 0.50]:
        subset = df[
            (df["market_cap"] >= 40)
            & (df["market_cap"] <= 200)
            & (df["position"] <= pos_max)
            & (df["open_type"] == "假弱高开")
        ]
        if len(subset) > 0:
            print(
                f"  位置≤{pos_max * 100}%: {len(subset)}个, 收益{subset['intra_return'].mean():.2f}%"
            )

print("=" * 80)
