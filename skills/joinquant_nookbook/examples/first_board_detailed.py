from jqdata import *
import pandas as pd

print("=" * 80)
print("首板信号收敛 - 详细分析版（2024年Q4）")
print("=" * 80)

test_dates = ["2024-10-08", "2024-11-04", "2024-12-02"]

all_signals = []

for curr_date in test_dates:
    print(f"\n处理 {curr_date}...")

    trade_days = get_trade_days(end_date=curr_date, count=2)
    prev_date = str(trade_days[0])

    all_stocks = get_all_securities("stock", curr_date).index.tolist()

    price_prev = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
    )

    limit_stocks = price_prev[
        abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
        < 0.01
    ]["code"].tolist()

    if len(limit_stocks) == 0:
        continue

    print(f"  涨停板: {len(limit_stocks)}只")

    price_curr = get_price(
        limit_stocks,
        end_date=curr_date,
        count=1,
        fields=["open", "close", "high"],
        panel=False,
    )

    for stock in limit_stocks:
        try:
            prev_row = price_prev[price_prev["code"] == stock].iloc[0]
            curr_row = price_curr[price_curr["code"] == stock].iloc[0]

            prev_close = float(prev_row["close"])
            curr_open = float(curr_row["open"])
            curr_close = float(curr_row["close"])
            curr_high = float(curr_row["high"])

            open_pct = (curr_open - prev_close) / prev_close * 100
            intra_return = (curr_close - curr_open) / curr_open * 100
            max_return = (curr_high - curr_open) / curr_open * 100

            if 0.5 <= open_pct <= 1.5:
                open_type = "假弱高开"
            elif -3.0 <= open_pct < -1.0:
                open_type = "真低开A"
            elif -1.0 <= open_pct < 0.0:
                open_type = "真低开B"
            else:
                continue

            all_signals.append(
                {
                    "date": curr_date,
                    "stock": stock,
                    "open_pct": round(open_pct, 2),
                    "intra_return": round(intra_return, 2),
                    "max_return": round(max_return, 2),
                    "open_type": open_type,
                }
            )
        except:
            continue

df = pd.DataFrame(all_signals)

print("\n" + "=" * 80)
print("详细信号列表（假弱高开 + 真低开）")
print("=" * 80)

for open_type in ["假弱高开", "真低开A", "真低开B"]:
    subset = df[df["open_type"] == open_type]
    if len(subset) > 0:
        avg_ret = subset["intra_return"].mean()
        win_count = (subset["intra_return"] > 0).sum()
        win_rate = win_count / len(subset) * 100

        print(f"\n{open_type}: {len(subset)}个")
        print(f"  平均收益: {avg_ret:.2f}%")
        print(f"  胜率: {win_rate:.1f}%")
        print("\n  详细:")
        for idx, row in subset.iterrows():
            status = "✓" if row["intra_return"] > 0 else "✗"
            print(
                f"    {status} {row['date']} {row['stock']}: 开{row['open_pct']:+.2f}% 日内{row['intra_return']:+.2f}% 最高{row['max_return']:+.2f}%"
            )

print("\n完成！")
