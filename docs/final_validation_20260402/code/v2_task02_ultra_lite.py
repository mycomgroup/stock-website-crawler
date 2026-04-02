from jqdata import *
import pandas as pd

print("任务02: 信号放宽测试 (简化版)")

sample_dates = [
    "2024-02-01",
    "2024-03-01",
    "2024-04-01",
    "2024-05-01",
    "2024-06-01",
    "2024-07-01",
]

results = {}

for test_date in sample_dates:
    print(f"\n测试日期: {test_date}")

    try:
        prev_date = get_trade_days(end_date=test_date, count=2)[0]

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
        ]["code"].tolist()[:30]

        if not limit_stocks:
            continue

        price_curr = get_price(
            limit_stocks,
            end_date=test_date,
            count=1,
            fields=["open", "close"],
            panel=False,
        )

        if price_curr.empty:
            continue

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(limit_stocks)
        )
        val = get_fundamentals(q, date=test_date)

        if val.empty:
            continue

        original_count = 0
        relaxed_count = 0
        original_returns = []
        relaxed_returns = []

        for stock in limit_stocks:
            try:
                prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                curr_row = price_curr[price_curr["code"] == stock].iloc[0]
                val_row = val[val["code"] == stock]

                if len(prev_row) == 0 or len(curr_row) == 0 or len(val_row) == 0:
                    continue

                prev_close = float(prev_row["close"])
                curr_open = float(curr_row["open"])
                curr_close = float(curr_row["close"])
                market_cap = float(val_row["circulating_market_cap"].iloc[0])

                open_pct = (curr_open - prev_close) / prev_close * 100

                if not (0.5 <= open_pct <= 1.5):
                    continue

                intra_return = (curr_close - curr_open) / curr_open * 100

                if 50 <= market_cap <= 150:
                    original_count += 1
                    original_returns.append(intra_return)

                if 40 <= market_cap <= 200:
                    relaxed_count += 1
                    relaxed_returns.append(intra_return)

            except:
                continue

        print(f"  原版信号: {original_count}, 放宽版信号: {relaxed_count}")
        if original_returns:
            print(f"  原版收益: {sum(original_returns) / len(original_returns):.2f}%")
        if relaxed_returns:
            print(f"  放宽版收益: {sum(relaxed_returns) / len(relaxed_returns):.2f}%")

    except Exception as e:
        print(f"  错误: {e}")
        continue

print("\n分析完成！")
