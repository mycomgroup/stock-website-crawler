from jqdata import *

print("快速信号测试")

test_date = "2024-03-20"
prev_date = "2024-03-19"

print(f"测试日期: {prev_date} -> {test_date}")

all_stocks = get_all_securities("stock", prev_date).index.tolist()
print(f"股票总数: {len(all_stocks)}")

price_prev = get_price(
    all_stocks, end_date=prev_date, count=1, fields=["close", "high_limit"], panel=False
)
limit_stocks = price_prev[
    abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
    < 0.01
]["code"].tolist()
print(f"涨停股票数: {len(limit_stocks)}")

price_curr = get_price(
    limit_stocks, end_date=test_date, count=1, fields=["open", "close"], panel=False
)
print(f"获取当日数据: {len(price_curr)}")

q = query(valuation.code, valuation.circulating_market_cap).filter(
    valuation.code.in_(limit_stocks)
)
val_data = get_fundamentals(q, date=test_date)
print(f"市值数据: {len(val_data)}")

VERSIONS = {
    "原版": (50, 150, 0.30),
    "放宽D": (30, 300, 0.50),
}

for v_name, (min_cap, max_cap, max_pos) in VERSIONS.items():
    count = 0
    for stock in limit_stocks[:100]:
        try:
            prev_row = price_prev[price_prev["code"] == stock].iloc[0]
            curr_row = price_curr[price_curr["code"] == stock].iloc[0]
            val_row = val_data[val_data["code"] == stock]

            if len(val_row) == 0:
                continue

            prev_close = float(prev_row["close"])
            curr_open = float(curr_row["open"])
            curr_close = float(curr_row["close"])
            mc = float(val_row["circulating_market_cap"].iloc[0])

            open_pct = (curr_open - prev_close) / prev_close * 100

            if not (min_cap <= mc <= max_cap):
                continue

            if not (-10 <= open_pct <= 10):
                continue

            count += 1
        except:
            continue

    print(f"{v_name}: {count} 个信号")

print("完成")
