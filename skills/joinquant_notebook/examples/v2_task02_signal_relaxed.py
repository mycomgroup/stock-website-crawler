from jqdata import *
import pandas as pd
import numpy as np

"""
v2任务02: 主线信号放宽测试
测试不同筛选条件组合的信号数量和收益
"""

print("=" * 60)
print("v2任务02: 主线信号放宽测试")
print("=" * 60)


def test_version(name, cap_min, cap_max, pos_limit, test_dates):
    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        try:
            all_stocks = get_all_securities("stock", prev_date).index.tolist()

            price_prev = get_price(
                all_stocks[:2000],
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
                limit_stocks[:100],
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )

            if price_curr.empty:
                continue

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(limit_stocks[:100])
            )
            val = get_fundamentals(q, date=curr_date)

            if val.empty:
                continue

            for stock in limit_stocks[:100]:
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

                    val_row = val[val["code"] == stock]
                    if len(val_row) == 0:
                        continue

                    market_cap = float(val_row["circulating_market_cap"].iloc[0])

                    if not (cap_min <= market_cap <= cap_max):
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

                    if position > pos_limit:
                        continue

                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100

                    signals.append(
                        {
                            "date": curr_date,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                        }
                    )
                except:
                    continue
        except:
            continue

    if len(signals) == 0:
        return name, 0, 0, 0, 0

    df = pd.DataFrame(signals)

    jw_stocks = df[(df["open_pct"] >= 0.5) & (df["open_pct"] <= 1.5)]

    if len(jw_stocks) == 0:
        return name, len(df), 0, 0, 0

    return (
        name,
        len(df),
        len(jw_stocks),
        jw_stocks["intra_return"].mean(),
        jw_stocks["intra_return"].std(),
    )


test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-01-02"]

print(f"\n研究期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"交易日数: {len(test_dates)}")

versions = [
    ("原版", 50, 150, 0.30),
    ("放宽A", 40, 200, 0.30),
    ("放宽B", 50, 150, 0.50),
    ("放宽C", 40, 200, 0.50),
    ("放宽D", 30, 300, 0.50),
]

results = []

for name, cap_min, cap_max, pos_limit in versions:
    print(f"\n测试版本: {name} (市值{cap_min}-{cap_max}亿, 位置<{pos_limit * 100}%)...")
    result = test_version(name, cap_min, cap_max, pos_limit, test_dates)
    results.append(result)
    print(
        f"  总信号: {result[1]}, 假弱高开: {result[2]}, 收益: {result[3]:.2f}%, 标准差: {result[4]:.2f}%"
    )

print("\n" + "=" * 60)
print("结果对比")
print("=" * 60)
print(f"\n{'版本':<10} {'总信号':<10} {'假弱高开':<10} {'收益%':<10} {'标准差%':<10}")
print("-" * 60)
for r in results:
    print(f"{r[0]:<10} {r[1]:<10} {r[2]:<10} {r[3]:<10.2f} {r[4]:<10.2f}")

print("\n" + "=" * 60)
print("推荐版本")
print("=" * 60)

valid_results = [r for r in results if r[1] > 0]
if valid_results:
    best = max(valid_results, key=lambda x: x[2])
    print(f"\n最优版本: {best[0]}")
    print(f"  信号数量: {best[2]}")
    print(f"  日均收益: {best[3]:.2f}%")
    print(f"  推荐理由: 信号数量与收益平衡最佳")

print("\n分析完成！")
