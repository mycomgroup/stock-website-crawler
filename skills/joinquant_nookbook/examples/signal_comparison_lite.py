from jqdata import *
import pandas as pd
import numpy as np

"""
任务03v2：信号放宽版vs原版对比 - 简化版
只测试原版 vs 放宽D（最宽松版本）
"""


def classify_open_type(open_pct):
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -10 <= open_pct <= 10:
        return "其他"
    else:
        return "超出范围"


VERSIONS = {
    "原版": (50, 150, 0.30),
    "放宽D": (30, 300, 0.50),
}

print("=" * 80)
print("信号放宽版vs原版对比（简化版）")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
all_dates_2024 = [str(d) if hasattr(d, "strftime") else d for d in all_dates_2024]
start_idx = all_dates_2024.index("2024-01-02") if "2024-01-02" in all_dates_2024 else 0
test_dates = all_dates_2024[start_idx:]

oos_start = "2024-07-01"

print(f"测试期间：2024-01-02 到 2024-12-31，共 {len(test_dates)} 个交易日")

all_version_signals = {}

for version_name, (min_cap, max_cap, max_position) in VERSIONS.items():
    print(
        f"\n处理版本：{version_name} (市值{min_cap}-{max_cap}亿，位置<= {max_position * 100:.0f}%)"
    )

    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if i % 30 == 0:
            print(f"  进度：{i}/{len(test_dates)}")

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

            limit_stocks = price_prev[
                abs(price_prev["close"] - price_prev["high_limit"])
                / price_prev["high_limit"]
                < 0.01
            ]["code"].tolist()

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
            val_data = get_fundamentals(q, date=curr_date)

            if val_data.empty:
                continue

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])
                    curr_high = float(curr_row["high"])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if -10 <= open_pct <= 10:
                        val_row = val_data[val_data["code"] == stock]
                        if len(val_row) == 0:
                            continue

                        market_cap = float(val_row["circulating_market_cap"].iloc[0])

                        if not (min_cap <= market_cap <= max_cap):
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

                        if position > max_position:
                            continue

                        lb_data_2d = get_price(
                            stock,
                            end_date=prev_date,
                            count=2,
                            fields=["close", "high_limit"],
                            panel=False,
                        )

                        if len(lb_data_2d) >= 2:
                            prev_prev_close = float(lb_data_2d["close"].iloc[0])
                            prev_prev_limit = float(lb_data_2d["high_limit"].iloc[0])

                            if (
                                abs(prev_prev_close - prev_prev_limit) / prev_prev_limit
                                < 0.01
                            ):
                                continue

                        intra_return = (curr_close - curr_open) / curr_open * 100
                        max_return = (curr_high - curr_open) / curr_open * 100

                        signals.append(
                            {
                                "date": str(curr_date),
                                "stock": stock,
                                "open_pct": open_pct,
                                "intra_return": intra_return,
                                "max_return": max_return,
                                "open_type": classify_open_type(open_pct),
                                "is_win": intra_return > 0,
                            }
                        )
                except:
                    continue
        except:
            continue

    all_version_signals[version_name] = signals
    print(f"  完成：{len(signals)} 个信号")

print("\n" + "=" * 80)
print("汇总对比")
print("=" * 80)

summary_stats = []

for version_name, signals in all_version_signals.items():
    if len(signals) == 0:
        continue

    df = pd.DataFrame(signals)

    total_count = len(df)
    avg_daily = total_count / len(test_dates)
    avg_intra_return = df["intra_return"].mean()
    avg_max_return = df["max_return"].mean()
    win_rate = df["is_win"].sum() / total_count * 100

    oos_df = df[df["date"] >= oos_start]
    oos_count = len(oos_df)
    oos_avg_return = oos_df["intra_return"].mean() if len(oos_df) > 0 else 0
    oos_win_rate = oos_df["is_win"].sum() / len(oos_df) * 100 if len(oos_df) > 0 else 0

    max_loss = df["intra_return"].min()
    max_win = df["intra_return"].max()

    df_sorted = df.sort_values("date")
    df_sorted["cum_return"] = (1 + df_sorted["intra_return"] / 100).cumprod() - 1
    rolling_max = df_sorted["cum_return"].expanding().max()
    drawdown = rolling_max - df_sorted["cum_return"]
    max_drawdown_pct = drawdown.max() * 100 if len(drawdown) > 0 else 0

    df_sorted["is_loss"] = df_sorted["intra_return"] < 0
    consecutive_losses = []
    current_streak = 0
    for is_loss in df_sorted["is_loss"]:
        if is_loss:
            current_streak += 1
        else:
            if current_streak > 0:
                consecutive_losses.append(current_streak)
            current_streak = 0
    if current_streak > 0:
        consecutive_losses.append(current_streak)
    max_consecutive_loss = max(consecutive_losses) if len(consecutive_losses) > 0 else 0

    summary_stats.append(
        {
            "version": version_name,
            "total_signals": total_count,
            "avg_daily": round(avg_daily, 2),
            "avg_return": round(avg_intra_return, 2),
            "avg_max_return": round(avg_max_return, 2),
            "win_rate": round(win_rate, 1),
            "oos_count": oos_count,
            "oos_return": round(oos_avg_return, 2),
            "oos_win_rate": round(oos_win_rate, 1),
            "max_loss": round(max_loss, 2),
            "max_win": round(max_win, 2),
            "max_dd": round(max_drawdown_pct, 2),
            "max_consec_loss": max_consecutive_loss,
        }
    )

summary_df = pd.DataFrame(summary_stats)
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("关键指标对比")
print("=" * 80)

if len(summary_df) >= 2:
    orig = summary_df[summary_df["version"] == "原版"].iloc[0]
    relaxed = summary_df[summary_df["version"] == "放宽D"].iloc[0]

    signal_ratio = relaxed["total_signals"] / orig["total_signals"]
    return_ratio = (
        relaxed["avg_return"] / orig["avg_return"] if orig["avg_return"] != 0 else 0
    )
    winrate_ratio = (
        relaxed["win_rate"] / orig["win_rate"] if orig["win_rate"] != 0 else 0
    )

    print(f"\n放宽D vs 原版:")
    print(
        f"  信号数量：{relaxed['total_signals']} vs {orig['total_signals']} (提升 {signal_ratio:.2f}x)"
    )
    print(f"  日内收益：{relaxed['avg_return']}% vs {orig['avg_return']}%")
    print(f"  胜率：{relaxed['win_rate']}% vs {orig['win_rate']}%")
    print(f"  最大回撤：{relaxed['max_dd']}% vs {orig['max_dd']}%")
    print(f"  连续亏损：{relaxed['max_consec_loss']}次 vs {orig['max_consec_loss']}次")

    pass_signal = signal_ratio >= 2
    pass_return = return_ratio >= 0.5
    pass_winrate = winrate_ratio >= 0.8

    print(f"\n通过门槛检查:")
    print(f"  信号数量>=2倍: {'PASS' if pass_signal else 'FAIL'}")
    print(f"  收益>=50%: {'PASS' if pass_return else 'FAIL'}")
    print(f"  胜率>=80%: {'PASS' if pass_winrate else 'FAIL'}")

print("\n" + "=" * 80)
print("假弱高开专项对比")
print("=" * 80)

for version_name, signals in all_version_signals.items():
    df = pd.DataFrame(signals)
    jw_df = df[df["open_type"] == "假弱高开"]

    if len(jw_df) > 0:
        print(f"\n{version_name} 假弱高开:")
        print(f"  信号数: {len(jw_df)}")
        print(f"  日内收益均值: {jw_df['intra_return'].mean():.2f}%")
        print(f"  胜率: {jw_df['is_win'].sum() / len(jw_df) * 100:.1f}%")

        oos_jw = jw_df[jw_df["date"] >= oos_start]
        if len(oos_jw) > 0:
            print(
                f"  样本外: {len(oos_jw)}个, 收益 {oos_jw['intra_return'].mean():.2f}%, 胜率 {oos_jw['is_win'].sum() / len(oos_jw) * 100:.1f}%"
            )

print("\n" + "=" * 80)
print("月度收益对比")
print("=" * 80)

for version_name, signals in all_version_signals.items():
    df = pd.DataFrame(signals)
    monthly = df.groupby(df["date"].str[:7]).agg({"intra_return": ["sum", "count"]})
    monthly.columns = ["收益%", "信号数"]
    print(f"\n{version_name}:")
    print(monthly.round(2).to_string())

print("\n分析完成!")
