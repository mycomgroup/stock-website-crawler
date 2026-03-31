# 完整全年回测 - Q1（1-3月）修正版
from jqdata import *
import pandas as pd

print("=" * 80)
print("主线信号完整回测 - 2024年Q1（1-3月）")
print("=" * 80)

trade_days = get_trade_days("2024-01-01", "2024-03-31")
print(f"Q1交易日数: {len(trade_days)}")


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


signals = []

for i in range(1, len(trade_days)):
    prev_date = trade_days[i - 1]
    curr_date = trade_days[i]

    if i % 10 == 0:
        print(f"进度: {i}/{len(trade_days)} ({i / len(trade_days) * 100:.1f}%)")

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

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(limit_stocks)
        )

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

                if not (-10 <= open_pct <= 10):
                    continue

                val_row = val_data[val_data["code"] == stock]
                if len(val_row) == 0:
                    continue

                market_cap = float(val_row["circulating_market_cap"].iloc[0])

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

if len(signals) > 0:
    df = pd.DataFrame(signals)

    print(f"\nQ1总信号: {len(df)}")
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
        print(f"  位置≤{pos_max * 100}%: {len(subset)}个")

    print("\n按开盘类型分组:")
    open_types = ["假弱高开", "真低开A", "真低开B", "平开附近", "深度低开", "微高开"]
    for ot in open_types:
        subset = df[df["open_type"] == ot]
        if len(subset) > 0:
            print(f"  {ot}: {len(subset)}个, 收益{subset['intra_return'].mean():.2f}%")

    print("\n组合筛选:")

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

print("=" * 80)
