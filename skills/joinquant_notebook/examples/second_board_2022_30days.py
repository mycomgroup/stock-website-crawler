from jqdata import *
import pandas as pd

print("二板2022年测试（30天样本）")

year = 2022
all_dates = list(get_trade_days(start_date=f"{year}-01-01", end_date=f"{year}-12-31"))
all_dates = [str(d) if hasattr(d, "strftime") else d for d in all_dates]

print(f"交易日数: {len(all_dates)}")

signals = []

for i in range(2, min(30, len(all_dates))):
    prev_prev = all_dates[i - 2]
    prev = all_dates[i - 1]
    curr = all_dates[i]

    print(f"{prev} -> {curr}")

    try:
        all_stocks = get_all_securities("stock", prev).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        price_prev = get_price(
            all_stocks,
            end_date=prev,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if price_prev.empty:
            continue

        zt_df = price_prev[
            abs(price_prev["close"] - price_prev["high_limit"])
            / price_prev["high_limit"]
            < 0.01
        ]
        zt_stocks = zt_df["code"].tolist()

        zt_count = len(zt_stocks)
        print(f"  涨停数: {zt_count}")

        if zt_count < 10:
            continue

        price_pp = get_price(
            zt_stocks,
            end_date=prev_prev,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if price_pp.empty:
            continue

        for stock in zt_stocks[:30]:
            try:
                prev_row = zt_df[zt_df["code"] == stock].iloc[0]
                prev_close = float(prev_row["close"])

                pp_row = price_pp[price_pp["code"] == stock]
                if len(pp_row) == 0:
                    continue

                pp_close = float(pp_row["close"].iloc[0])
                pp_limit = float(pp_row["high_limit"].iloc[0])

                if abs(pp_close - pp_limit) / pp_limit >= 0.01:
                    continue

                price_curr = get_price(
                    stock,
                    end_date=curr,
                    count=1,
                    fields=["open", "close", "high_limit"],
                    panel=False,
                )
                if price_curr.empty:
                    continue

                curr_open = float(price_curr["open"].iloc[0])
                curr_close = float(price_curr["close"].iloc[0])
                curr_limit = float(price_curr["high_limit"].iloc[0])

                if abs(curr_open - curr_limit) / curr_limit < 0.01:
                    continue

                ret = (curr_close - curr_open) / curr_open * 100
                signals.append({"date": curr, "return": ret, "win": ret > 0})

            except:
                continue
    except:
        continue

if len(signals) > 0:
    df = pd.DataFrame(signals)
    print(f"\n2022年样本统计:")
    print(f"  信号数: {len(df)}")
    print(f"  平均收益: {df['return'].mean():.2f}%")
    print(f"  胜率: {df['win'].sum() / len(df) * 100:.1f}%")
else:
    print("\n无信号")

print("\n2022年测试完成")
