from jqdata import *
import pandas as pd

print("=" * 80)
print("首板信号收敛 - 极简对比版（只测试2024-12-01）")
print("=" * 80)

curr_date = "2024-12-01"
trade_days = get_trade_days(end_date=curr_date, count=2)
prev_date = str(trade_days[0])

print(f"\n测试日期: {prev_date} -> {curr_date}")

all_stocks = get_all_securities("stock", curr_date).index.tolist()[:500]
print(f"测试股票数: {len(all_stocks)}")

price_prev = get_price(
    all_stocks, end_date=prev_date, count=1, fields=["close", "high_limit"], panel=False
)

limit_stocks = price_prev[
    abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
    < 0.01
]["code"].tolist()

print(f"涨停板股票: {len(limit_stocks)}")

if len(limit_stocks) == 0:
    print("未找到涨停板股票")
    exit()

price_curr = get_price(
    limit_stocks,
    end_date=curr_date,
    count=1,
    fields=["open", "close", "high"],
    panel=False,
)

signals = []

for stock in limit_stocks:
    try:
        prev_row = price_prev[price_prev["code"] == stock].iloc[0]
        curr_row = price_curr[price_curr["code"] == stock].iloc[0]

        prev_close = float(prev_row["close"])
        curr_open = float(curr_row["open"])
        curr_close = float(curr_row["close"])

        open_pct = (curr_open - prev_close) / prev_close * 100
        intra_return = (curr_close - curr_open) / curr_open * 100

        if -10 <= open_pct <= 10:
            if 0.5 <= open_pct <= 1.5:
                open_type = "假弱高开"
            elif -3.0 <= open_pct < -1.0:
                open_type = "真低开A"
            elif -1.0 <= open_pct < 0.0:
                open_type = "真低开B"
            else:
                open_type = "其他"

            signals.append(
                {
                    "stock": stock,
                    "open_pct": open_pct,
                    "intra_return": intra_return,
                    "open_type": open_type,
                }
            )
    except:
        continue

df = pd.DataFrame(signals)

print(f"\n找到 {len(df)} 个信号")

if len(df) > 0:
    for open_type in ["假弱高开", "真低开A", "真低开B"]:
        subset = df[df["open_type"] == open_type]
        if len(subset) > 0:
            avg_ret = subset["intra_return"].mean()
            print(f"{open_type}: {len(subset)}个, 收益 {avg_ret:.2f}%")

print("\n完成！")
