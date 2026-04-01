from jqdata import *
import pandas as pd
import numpy as np

"""
v2任务04: 二板2021-2023实测验证
验证二板策略的历史稳定性
"""

print("=" * 60)
print("v2任务04: 二板2021-2023实测验证")
print("=" * 60)


def test_year(year):
    print(f"\n测试年份: {year}")
    print("-" * 60)

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    test_dates = list(get_trade_days(end_date=end_date, count=250))
    test_dates = [str(d) for d in test_dates if str(d) >= start_date]

    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if i % 50 == 0:
            print(f"  进度: {i}/{len(test_dates)}")

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

                    if not (-3 <= open_pct <= 3):
                        continue

                    q = query(valuation.code, valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    )
                    val = get_fundamentals(q, date=curr_date)

                    if val.empty:
                        continue

                    market_cap = float(val["circulating_market_cap"].iloc[0])

                    if not (market_cap <= 500):
                        continue

                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "market_cap": market_cap,
                        }
                    )
                except:
                    continue
        except:
            continue

    if len(signals) == 0:
        return year, 0, 0, 0, 0, 0

    df = pd.DataFrame(signals)

    win_count = len(df[df["intra_return"] > 0])
    win_rate = win_count / len(df) * 100

    avg_return = df["intra_return"].mean()
    avg_max = df["max_return"].mean()

    profit_loss = df[df["intra_return"] > 0]["intra_return"].mean()
    loss = abs(df[df["intra_return"] < 0]["intra_return"].mean())
    profit_loss_ratio = profit_loss / loss if loss > 0 else 0

    print(f"  信号数: {len(df)}")
    print(f"  胜率: {win_rate:.1f}%")
    print(f"  日内收益: {avg_return:.2f}%")
    print(f"  盈亏比: {profit_loss_ratio:.2f}")

    return year, len(df), win_rate, avg_return, avg_max, profit_loss_ratio


years = [2021, 2022, 2023]

results = []

for year in years:
    result = test_year(year)
    results.append(result)

print("\n" + "=" * 60)
print("逐年对比")
print("=" * 60)
print(f"\n{'年份':<8} {'信号数':<10} {'胜率%':<10} {'日内收益%':<12} {'盈亏比':<10}")
print("-" * 60)
for r in results:
    print(f"{r[0]:<8} {r[1]:<10} {r[2]:<10.1f} {r[3]:<12.2f} {r[5]:<10.2f}")

print("\n" + "=" * 60)
print("稳定性分析")
print("=" * 60)

valid_results = [r for r in results if r[1] > 0]

if len(valid_results) >= 2:
    win_rates = [r[2] for r in valid_results]
    returns = [r[3] for r in valid_results]

    win_rate_std = np.std(win_rates)
    return_std = np.std(returns)

    positive_years = sum(1 for r in valid_results if r[3] > 0)

    print(f"\n胜率标准差: {win_rate_std:.2f}%")
    print(f"收益标准差: {return_std:.2f}%")
    print(f"正收益年数: {positive_years}/{len(valid_results)}")

    if win_rate_std < 15 and positive_years >= 2:
        print("\n结论: ✓ 策略跨周期稳定性良好")
    else:
        print("\n结论: ✗ 策略跨周期稳定性存疑")
else:
    print("\n数据不足，无法判断稳定性")

print("\n分析完成！")
