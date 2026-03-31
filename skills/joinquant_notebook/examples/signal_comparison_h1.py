from jqdata import *
import pandas as pd

"""
任务03v2：信号放宽版vs原版对比 - 上半年测试
只测试2024年1-6月数据
"""

print("=" * 80)
print("信号放宽版vs原版对比（上半年测试）")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
all_dates_2024 = [str(d) if hasattr(d, "strftime") else d for d in all_dates_2024]
test_dates = all_dates_2024[
    all_dates_2024.index("2024-01-02") : all_dates_2024.index("2024-07-01")
]

print(f"测试期间：{test_dates[0]} ~ {test_dates[-1]}，共 {len(test_dates)} 个交易日")

VERSIONS = {
    "原版": (50, 150, 0.30),
    "放宽D": (30, 300, 0.50),
}

all_signals = {}

for version_name, (min_cap, max_cap, max_pos) in VERSIONS.items():
    print(f"\n{version_name}: 市值{min_cap}-{max_cap}亿, 位置<= {max_pos * 100:.0f}%")

    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if i % 20 == 0:
            print(f"  进度: {i}/{len(test_dates)} ({i * 100 / len(test_dates):.0f}%)")

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

            val_df = get_fundamentals(
                query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code.in_(limit_stocks)
                ),
                date=curr_date,
            )

            if val_df.empty:
                continue

            val_dict = dict(zip(val_df["code"], val_df["circulating_market_cap"]))

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
                    curr_high = float(
                        price_curr[price_curr["code"] == stock]["high"].iloc[0]
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
                    max_return = (curr_high - curr_open) / curr_open * 100

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": round(open_pct, 2),
                            "intra_return": round(intra_return, 2),
                            "max_return": round(max_return, 2),
                            "market_cap": round(mc, 1),
                            "position": round(position, 2),
                        }
                    )
                except:
                    continue
        except:
            continue

    all_signals[version_name] = signals
    print(f"  完成: {len(signals)} 个信号")

print("\n" + "=" * 80)
print("上半年统计")
print("=" * 80)

summary = []
for version_name, signals in all_signals.items():
    df = pd.DataFrame(signals)
    if len(df) == 0:
        continue

    total = len(df)
    avg_return = df["intra_return"].mean()
    avg_max = df["max_return"].mean()
    win_rate = (df["intra_return"] > 0).sum() / total * 100

    df_sorted = df.sort_values("date")
    df_sorted["cum"] = (1 + df_sorted["intra_return"] / 100).cumprod() - 1
    rolling_max = df_sorted["cum"].expanding().max()
    max_dd = (rolling_max - df_sorted["cum"]).max() * 100

    max_loss = df["intra_return"].min()
    max_win = df["intra_return"].max()

    df_sorted["is_loss"] = df_sorted["intra_return"] < 0
    consec_losses = []
    streak = 0
    for is_loss in df_sorted["is_loss"]:
        if is_loss:
            streak += 1
        else:
            if streak > 0:
                consec_losses.append(streak)
            streak = 0
    if streak > 0:
        consec_losses.append(streak)
    max_consec = max(consec_losses) if consec_losses else 0

    monthly = df.groupby(df["date"].str[:7])["intra_return"].sum()

    print(f"\n{version_name}:")
    print(f"  总信号: {total}")
    print(f"  日内收益均值: {avg_return:.2f}%")
    print(f"  最高收益均值: {avg_max:.2f}%")
    print(f"  胜率: {win_rate:.1f}%")
    print(f"  最大回撤: {max_dd:.2f}%")
    print(f"  最大亏损: {max_loss:.2f}%")
    print(f"  最大盈利: {max_win:.2f}%")
    print(f"  最大连续亏损: {max_consec}次")

    summary.append(
        {
            "版本": version_name,
            "信号数": total,
            "日内收益%": round(avg_return, 2),
            "胜率%": round(win_rate, 1),
            "最大回撤%": round(max_dd, 2),
            "最大亏损%": round(max_loss, 2),
            "最大连续亏损": max_consec,
        }
    )

summary_df = pd.DataFrame(summary)
print("\n汇总表:")
print(summary_df.to_string(index=False))

if len(summary) >= 2:
    orig = summary_df[summary_df["版本"] == "原版"].iloc[0]
    relaxed = summary_df[summary_df["版本"] == "放宽D"].iloc[0]

    signal_ratio = relaxed["信号数"] / orig["信号数"]
    return_ratio = (
        relaxed["日内收益%"] / orig["日内收益%"] if orig["日内收益%"] != 0 else 0
    )
    winrate_ratio = relaxed["胜率%"] / orig["胜率%"] if orig["胜率%"] != 0 else 0

    print(f"\n放宽D vs 原版:")
    print(f"  信号提升: {signal_ratio:.2f}x")
    print(f"  收益比: {return_ratio:.2f}")
    print(f"  胜率比: {winrate_ratio:.2f}")

    pass_signal = signal_ratio >= 2
    pass_return = return_ratio >= 0.5
    pass_winrate = winrate_ratio >= 0.8

    print(f"\n门槛检查:")
    print(f"  信号>=2倍: {'PASS' if pass_signal else 'FAIL'}")
    print(f"  收益>=50%: {'PASS' if pass_return else 'FAIL'}")
    print(f"  胜率>=80%: {'PASS' if pass_winrate else 'FAIL'}")

print("\n完成!")
