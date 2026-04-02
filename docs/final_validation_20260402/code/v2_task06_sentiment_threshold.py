from jqdata import *
import pandas as pd
import numpy as np

"""
v2任务06: 情绪开关阈值优化
测试不同涨停家数阈值对信号的影响
"""

print("=" * 60)
print("v2任务06: 情绪开关阈值优化")
print("=" * 60)


def get_zt_count(date):
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()

        price = get_price(
            all_stocks[:2000],
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )

        if price.empty:
            return 0

        zt_count = len(
            price[
                abs(price["close"] - price["high_limit"]) / price["high_limit"] < 0.01
            ]
        )

        return zt_count
    except:
        return 0


def test_threshold(threshold, test_dates):
    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if threshold > 0:
            zt_count = get_zt_count(prev_date)
            if zt_count < threshold:
                continue

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

            for stock in limit_stocks[:100]:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])
                    curr_high = float(curr_row["high"])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if not (0.5 <= open_pct <= 1.5):
                        continue

                    q = query(valuation.code, valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    )
                    val = get_fundamentals(q, date=curr_date)

                    if val.empty:
                        continue

                    market_cap = float(val["circulating_market_cap"].iloc[0])

                    if not (50 <= market_cap <= 150):
                        continue

                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "intra_return": intra_return,
                            "max_return": max_return,
                        }
                    )
                except:
                    continue
        except:
            continue

    if len(signals) == 0:
        return threshold, 0, 0, 0, 0

    df = pd.DataFrame(signals)

    win_count = len(df[df["intra_return"] > 0])
    win_rate = win_count / len(df) * 100

    return (
        threshold,
        len(df),
        win_rate,
        df["intra_return"].mean(),
        df["max_return"].mean(),
    )


test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-01-02"]

print(f"\n研究期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"交易日数: {len(test_dates)}")

thresholds = [0, 20, 30, 40, 50, 60, 80, 100]

results = []

for threshold in thresholds:
    label = "无过滤" if threshold == 0 else f"阈值{threshold}"
    print(f"\n测试阈值: {label}...")
    result = test_threshold(threshold, test_dates)
    results.append(result)
    if result[1] > 0:
        print(f"  信号数: {result[1]}, 胜率: {result[2]:.1f}%, 收益: {result[3]:.2f}%")
    else:
        print(f"  信号数: 0")

print("\n" + "=" * 60)
print("阈值对比结果")
print("=" * 60)
print(
    f"\n{'阈值':<12} {'信号数':<10} {'胜率%':<10} {'日内收益%':<12} {'最高收益%':<12}"
)
print("-" * 60)
for r in results:
    label = "无过滤" if r[0] == 0 else f"≥{r[0]}"
    print(f"{label:<12} {r[1]:<10} {r[2]:<10.1f} {r[3]:<12.2f} {r[4]:<12.2f}")

print("\n" + "=" * 60)
print("最优阈值推荐")
print("=" * 60)

valid_results = [r for r in results if r[1] >= 10]

if valid_results:
    best_by_return = max(valid_results, key=lambda x: x[3])
    best_by_winrate = max(valid_results, key=lambda x: x[2])

    print(f"\n按收益最优: 阈值{best_by_return[0]} (收益{best_by_return[3]:.2f}%)")
    print(f"按胜率最优: 阈值{best_by_winrate[0]} (胜率{best_by_winrate[2]:.1f}%)")

    if best_by_return[0] == best_by_winrate[0]:
        print(f"\n综合推荐: 阈值{best_by_return[0]}")
    else:
        print(f"\n推荐: 阈值30 (平衡信号数量与收益)")

print("\n分析完成！")
