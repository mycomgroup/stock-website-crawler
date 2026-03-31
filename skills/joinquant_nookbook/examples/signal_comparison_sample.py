from jqdata import *
import pandas as pd

"""
任务03v2：信号放宽版vs原版对比 - 采样测试
每月采样5天，快速获取对比数据
"""

print("=" * 80)
print("信号放宽版vs原版对比（采样测试）")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
all_dates_2024 = [str(d) if hasattr(d, "strftime") else d for d in all_dates_2024]

months = [
    "2024-01",
    "2024-02",
    "2024-03",
    "2024-04",
    "2024-05",
    "2024-06",
    "2024-07",
    "2024-08",
    "2024-09",
    "2024-10",
    "2024-11",
    "2024-12",
]

sample_dates = []
for m in months:
    m_dates = [d for d in all_dates_2024 if d.startswith(m)]
    if len(m_dates) >= 5:
        sample_dates.extend(m_dates[:: len(m_dates) // 5][:5])

print(f"采样日期数: {len(sample_dates)} 个")

VERSIONS = {
    "原版": (50, 150, 0.30),
    "放宽D": (30, 300, 0.50),
}

all_results = {}

for version_name, (min_cap, max_cap, max_pos) in VERSIONS.items():
    print(f"\n{version_name}: 市值{min_cap}-{max_cap}亿, 位置<= {max_pos * 100:.0f}%")

    signals = []

    for i in range(1, len(sample_dates)):
        prev_date = sample_dates[i - 1]
        curr_date = sample_dates[i]

        print(f"  处理: {prev_date} -> {curr_date}")

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

            limit_df = price_prev[
                abs(price_prev["close"] - price_prev["high_limit"])
                / price_prev["high_limit"]
                < 0.01
            ]
            limit_stocks = limit_df["code"].tolist()

            if len(limit_stocks) == 0:
                print(f"    涨停数: 0")
                continue

            print(f"    涨停数: {len(limit_stocks)}")

            price_curr = get_price(
                limit_stocks,
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )

            if price_curr.empty:
                continue

            val_df = get_fundamentals(
                query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code.in_(limit_stocks)
                ),
                date=curr_date,
            )

            if val_df.empty:
                continue

            val_dict = dict(zip(val_df["code"], val_df["circulating_market_cap"]))

            count = 0
            returns = []

            for stock in limit_stocks:
                try:
                    if stock not in val_dict:
                        continue

                    mc = val_dict[stock]
                    if not (min_cap <= mc <= max_cap):
                        continue

                    prev_close = float(
                        limit_df[limit_df["code"] == stock]["close"].iloc[0]
                    )
                    curr_open = float(
                        price_curr[price_curr["code"] == stock]["open"].iloc[0]
                    )
                    curr_close = float(
                        price_curr[price_curr["code"] == stock]["close"].iloc[0]
                    )

                    open_pct = (curr_open - prev_close) / prev_close * 100
                    if not (-10 <= open_pct <= 10):
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

                    high_15 = float(prices_15d["close"].max())
                    low_15 = float(prices_15d["close"].min())
                    if high_15 == low_15:
                        continue

                    position = (prev_close - low_15) / (high_15 - low_15)
                    if position > max_pos:
                        continue

                    lb_2d = get_price(
                        stock,
                        end_date=prev_date,
                        count=2,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    if len(lb_2d) >= 2:
                        pp_close = float(lb_2d["close"].iloc[0])
                        pp_limit = float(lb_2d["high_limit"].iloc[0])
                        if abs(pp_close - pp_limit) / pp_limit < 0.01:
                            continue

                    intra_return = (curr_close - curr_open) / curr_open * 100

                    count += 1
                    returns.append(intra_return)
                    signals.append({"date": curr_date, "return": intra_return})
                except:
                    continue

            print(
                f"    信号数: {count}, 平均收益: {sum(returns) / len(returns):.2f}% if returns else 0"
            )
        except Exception as e:
            print(f"    错误: {e}")
            continue

    all_results[version_name] = signals
    print(f"\n  总信号: {len(signals)}")

print("\n" + "=" * 80)
print("汇总")
print("=" * 80)

for version_name, signals in all_results.items():
    df = pd.DataFrame(signals)
    if len(df) == 0:
        continue

    avg_return = df["return"].mean()
    win_rate = (df["return"] > 0).sum() / len(df) * 100
    max_loss = df["return"].min()

    est_full_year = len(signals) * 12 / len(months)

    print(f"\n{version_name}:")
    print(f"  样本信号: {len(signals)}")
    print(f"  推算全年: ~{est_full_year:.0f}")
    print(f"  平均收益: {avg_return:.2f}%")
    print(f"  胜率: {win_rate:.1f}%")
    print(f"  最大亏损: {max_loss:.2f}%")

if len(all_results) >= 2:
    orig_df = pd.DataFrame(all_results["原版"])
    relaxed_df = pd.DataFrame(all_results["放宽D"])

    signal_ratio = len(relaxed_df) / len(orig_df)
    return_ratio = (
        relaxed_df["return"].mean() / orig_df["return"].mean()
        if orig_df["return"].mean() != 0
        else 0
    )
    winrate_ratio = (
        (relaxed_df["return"] > 0).sum()
        / len(relaxed_df)
        / ((orig_df["return"] > 0).sum() / len(orig_df))
    )

    print(f"\n放宽D vs 原版:")
    print(f"  信号提升: {signal_ratio:.2f}x")
    print(f"  收益比: {return_ratio:.2f}")
    print(f"  胜率比: {winrate_ratio:.2f}")

print("\n完成!")
