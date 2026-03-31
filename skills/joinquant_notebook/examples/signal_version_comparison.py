from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

"""
任务03v2：信号放宽版vs原版对比
测试原版与多个放宽版本的效果，包括：
- 原版：市值50-150亿 + 位置<=30% + 无连板
- 放宽A：市值40-200亿 + 位置<=30% + 无连板
- 放宽B：市值50-150亿 + 位置<=50% + 无连板
- 放宽C：市值40-200亿 + 位置<=50% + 无连板
- 放宽D：市值30-300亿 + 位置<=50% + 无连板
"""


def classify_open_type(open_pct):
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -1.0 <= open_pct < 0.0:
        return "真低开B"
    elif 0.0 <= open_pct < 0.5:
        return "边界A_平开附近"
    elif -5.0 <= open_pct < -3.0:
        return "边界B_深度低开"
    elif 1.5 <= open_pct <= 2.5:
        return "边界C_微高开"
    else:
        return "其他"


VERSIONS = {
    "原版": (50, 150, 0.30),
    "放宽A": (40, 200, 0.30),
    "放宽B": (50, 150, 0.50),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

print("=" * 80)
print("任务03v2：信号放宽版vs原版对比")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
all_dates_2024 = [str(d) if hasattr(d, "strftime") else d for d in all_dates_2024]
start_idx = all_dates_2024.index("2024-01-02") if "2024-01-02" in all_dates_2024 else 0
test_dates = all_dates_2024[start_idx:]

oos_start = "2024-07-01"
oos_dates = [d for d in test_dates if d >= oos_start]
train_dates = [d for d in test_dates if d < oos_start]

print(f"测试期间：2024-01-02 到 2024-12-31，共 {len(test_dates)} 个交易日")
print(f"训练期：2024-01-02 到 2024-06-30，共 {len(train_dates)} 个交易日")
print(f"样本外：2024-07-01 到 2024-12-31，共 {len(oos_dates)} 个交易日")

all_version_signals = {}

for version_name, (min_cap, max_cap, max_position) in VERSIONS.items():
    print(
        f"\n处理版本：{version_name} (市值{min_cap}-{max_cap}亿，位置<= {max_position * 100:.0f}%)"
    )

    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if i % 50 == 0:
            print(f"  进度：{i}/{len(test_dates)} ({i / len(test_dates) * 100:.1f}%)")

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
                fields=["open", "close", "high", "high_limit"],
                panel=False,
            )

            if price_curr.empty:
                continue

            q = query(
                valuation.code,
                valuation.circulating_market_cap,
            ).filter(valuation.code.in_(limit_stocks))

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
                                "market_cap": market_cap,
                                "position": position,
                                "version": version_name,
                            }
                        )
                except Exception as e:
                    continue
        except Exception as e:
            continue

    all_version_signals[version_name] = signals
    print(f"  完成：{len(signals)} 个信号")

print("\n" + "=" * 80)
print("各版本汇总对比")
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

    monthly_returns = df.groupby(df["date"].str[:7])["intra_return"].sum()

    summary_stats.append(
        {
            "version": version_name,
            "total_signals": total_count,
            "avg_daily_signals": avg_daily,
            "avg_intra_return": avg_intra_return,
            "avg_max_return": avg_max_return,
            "win_rate": win_rate,
            "oos_signals": oos_count,
            "oos_avg_return": oos_avg_return,
            "oos_win_rate": oos_win_rate,
            "max_loss": max_loss,
            "max_win": max_win,
            "max_drawdown": max_drawdown_pct,
            "max_consecutive_loss": max_consecutive_loss,
            "monthly_return_std": monthly_returns.std(),
            "positive_month_ratio": (monthly_returns > 0).sum()
            / len(monthly_returns)
            * 100,
        }
    )

summary_df = pd.DataFrame(summary_stats)
summary_df = summary_df.sort_values("total_signals", ascending=False)

print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("关键对比指标")
print("=" * 80)

original = (
    summary_df[summary_df["version"] == "原版"].iloc[0]
    if len(summary_df[summary_df["version"] == "原版"]) > 0
    else None
)

if original is not None:
    for row in summary_df.itertuples():
        if row.version == "原版":
            continue

        signal_ratio = row.total_signals / original.total_signals
        return_ratio = (
            row.avg_intra_return / original.avg_intra_return
            if original.avg_intra_return != 0
            else 0
        )
        winrate_ratio = (
            row.win_rate / original.win_rate if original.win_rate != 0 else 0
        )

        pass_signal = signal_ratio >= 2
        pass_return = return_ratio >= 0.5
        pass_winrate = winrate_ratio >= 0.8

        print(f"\n{row.version} vs 原版:")
        print(
            f"  信号数量比: {signal_ratio:.2f}x ({'PASS' if pass_signal else 'FAIL'})"
        )
        print(f"  收益比: {return_ratio:.2f} ({'PASS' if pass_return else 'FAIL'})")
        print(f"  胜率比: {winrate_ratio:.2f} ({'PASS' if pass_winrate else 'FAIL'})")

print("\n" + "=" * 80)
print("月度收益分布对比")
print("=" * 80)

for version_name, signals in all_version_signals.items():
    if len(signals) == 0:
        continue

    df = pd.DataFrame(signals)
    monthly = (
        df.groupby(df["date"].str[:7])
        .agg({"intra_return": ["sum", "count", lambda x: (x > 0).sum() / len(x) * 100]})
        .round(2)
    )
    monthly.columns = ["月度收益%", "信号数", "胜率%"]

    print(f"\n{version_name}:")
    print(monthly.to_string())

print("\n" + "=" * 80)
print("假弱高开结构专项对比")
print("=" * 80)

for version_name, signals in all_version_signals.items():
    if len(signals) == 0:
        continue

    df = pd.DataFrame(signals)
    jw_df = df[df["open_type"] == "假弱高开"]

    if len(jw_df) > 0:
        print(f"\n{version_name} 假弱高开:")
        print(f"  信号数: {len(jw_df)}")
        print(f"  日内收益均值: {jw_df['intra_return'].mean():.2f}%")
        print(f"  最高收益均值: {jw_df['max_return'].mean():.2f}%")
        print(f"  胜率: {jw_df['is_win'].sum() / len(jw_df) * 100:.1f}%")

        oos_jw = jw_df[jw_df["date"] >= oos_start]
        if len(oos_jw) > 0:
            print(f"  样本外信号: {len(oos_jw)}")
            print(f"  样本外收益: {oos_jw['intra_return'].mean():.2f}%")
            print(f"  样本外胜率: {oos_jw['is_win'].sum() / len(oos_jw) * 100:.1f}%")

print("\n" + "=" * 80)
print("最终推荐")
print("=" * 80)

best_version = None
best_score = -1

for row in summary_df.itertuples():
    score = (
        (row.total_signals * row.avg_intra_return * row.win_rate / 10000)
        if row.avg_intra_return > 0
        else 0
    )
    if score > best_score:
        best_score = score
        best_version = row.version

print(f"\n推荐版本: {best_version}")
print(f"推荐理由:")
if best_version and len(summary_df[summary_df["version"] == best_version]) > 0:
    best_row = summary_df[summary_df["version"] == best_version].iloc[0]
    print(
        f"  信号数量: {best_row['total_signals']} ({best_row['avg_daily_signals']:.2f}个/日)"
    )
    print(f"  日内收益: {best_row['avg_intra_return']:.2f}%")
    print(f"  胜率: {best_row['win_rate']:.1f}%")
    print(f"  最大回撤: {best_row['max_drawdown']:.2f}%")
    print(f"  样本外收益: {best_row['oos_avg_return']:.2f}%")

if original is not None and best_version != "原版":
    print(f"\n与原版对比:")
    best_row = summary_df[summary_df["version"] == best_version].iloc[0]
    print(
        f"  信号数量提升: {best_row['total_signals'] / original['total_signals']:.2f}x"
    )
    print(
        f"  收益变化: {best_row['avg_intra_return'] - original['avg_intra_return']:.2f}%"
    )
    print(f"  胜率变化: {best_row['win_rate'] - original['win_rate']:.1f}%")

print("\n分析完成!")
