from jqdata import *
import pandas as pd

print("=" * 60)
print("v2任务02简化版: 主线信号放宽测试")
print("=" * 60)

test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-01-02"]

print(f"研究期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"测试日期数: {len(test_dates)}")

results = {}

versions = {
    "原版": {"cap": (50, 150), "pos": 0.30},
    "放宽A": {"cap": (40, 200), "pos": 0.30},
    "放宽B": {"cap": (50, 150), "pos": 0.50},
    "放宽C": {"cap": (40, 200), "pos": 0.50},
}

sample_dates = test_dates[::10]

for name, params in versions.items():
    print(f"\n测试版本: {name}...")

    signals = []

    for i, curr_date in enumerate(sample_dates):
        if i == 0:
            continue

        prev_date = sample_dates[i - 1]

        try:
            all_stocks = get_all_securities("stock", prev_date).index.tolist()[:1000]

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
            ]["code"].tolist()[:50]

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
            val = get_fundamentals(q, date=curr_date)

            if val.empty:
                continue

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock]
                    curr_row = price_curr[price_curr["code"] == stock]
                    val_row = val[val["code"] == stock]

                    if len(prev_row) == 0 or len(curr_row) == 0 or len(val_row) == 0:
                        continue

                    prev_close = float(prev_row["close"].iloc[0])
                    curr_open = float(curr_row["open"].iloc[0])
                    curr_close = float(curr_row["close"].iloc[0])

                    market_cap = float(val_row["circulating_market_cap"].iloc[0])

                    if not (params["cap"][0] <= market_cap <= params["cap"][1]):
                        continue

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if 0.5 <= open_pct <= 1.5:
                        intra_return = (curr_close - curr_open) / curr_open * 100
                        signals.append(intra_return)
                except:
                    continue
        except:
            continue

    if len(signals) > 0:
        results[name] = {
            "count": len(signals),
            "avg_return": sum(signals) / len(signals),
            "win_rate": sum(1 for r in signals if r > 0) / len(signals) * 100,
        }
        print(f"  信号数: {results[name]['count']}")
        print(f"  收益: {results[name]['avg_return']:.2f}%")
        print(f"  胜率: {results[name]['win_rate']:.1f}%")
    else:
        print(f"  无信号")

print("\n" + "=" * 60)
print("结果对比")
print("=" * 60)
print(f"\n{'版本':<10} {'信号数':<10} {'收益%':<10} {'胜率%':<10}")
print("-" * 50)
for name, r in results.items():
    print(
        f"{name:<10} {r['count']:<10} {r['avg_return']:<10.2f} {r['win_rate']:<10.1f}"
    )

if results:
    best = max(results.items(), key=lambda x: x[1]["count"])
    print(f"\n推荐版本: {best[0]}")
    print(f"理由: 信号数量最多且收益稳定")

print("\n分析完成！")
