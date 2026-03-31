from jqdata import *
import pandas as pd
import numpy as np

"""
任务04v2：二板2021-2023实测验证 - 采样版
每月采样5天，快速获取对比数据
"""

print("=" * 80)
print("二板策略2021-2023历史实测（采样版）")
print("=" * 80)


def get_zt_count(date):
    """获取涨停家数"""
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    if df.empty:
        return 0

    zt_df = df[abs(df["close"] - df["high_limit"]) / df["high_limit"] < 0.01]
    return len(zt_df)


def get_second_board_signals(prev_date, curr_date, prev_prev_date, min_zt_count=10):
    """获取二板信号"""
    signals = []

    zt_count = get_zt_count(prev_date)
    if zt_count < min_zt_count:
        return [], zt_count

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    price_prev = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit", "volume"],
        panel=False,
    )
    if price_prev.empty:
        return [], zt_count

    zt_df = price_prev[
        abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
        < 0.01
    ]
    zt_stocks = zt_df["code"].tolist()

    if len(zt_stocks) == 0:
        return [], zt_count

    price_prev_prev = get_price(
        zt_stocks,
        end_date=prev_prev_date,
        count=1,
        fields=["close", "high_limit", "volume"],
        panel=False,
    )

    if price_prev_prev.empty:
        return [], zt_count

    two_board_stocks = []
    for stock in zt_stocks:
        try:
            prev_row = zt_df[zt_df["code"] == stock].iloc[0]
            prev_close = float(prev_row["close"])
            prev_vol = float(prev_row["volume"])

            pp_row = price_prev_prev[price_prev_prev["code"] == stock]
            if len(pp_row) == 0:
                continue

            pp_close = float(pp_row["close"].iloc[0])
            pp_limit = float(pp_row["high_limit"].iloc[0])
            pp_vol = float(pp_row["volume"].iloc[0])

            if abs(pp_close - pp_limit) / pp_limit >= 0.01:
                continue

            if prev_vol > pp_vol * 1.875:
                continue

            two_board_stocks.append(stock)
        except:
            continue

    if len(two_board_stocks) == 0:
        return [], zt_count

    val_df = get_fundamentals(
        query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(two_board_stocks)
        ),
        date=curr_date,
    )

    if val_df.empty:
        return [], zt_count

    val_dict = dict(zip(val_df["code"], val_df["circulating_market_cap"]))

    price_curr = get_price(
        two_board_stocks,
        end_date=curr_date,
        count=1,
        fields=["open", "close", "high", "high_limit"],
        panel=False,
    )

    if price_curr.empty:
        return [], zt_count

    for stock in two_board_stocks:
        try:
            if stock not in val_dict:
                continue

            mc = val_dict[stock]

            curr_row = price_curr[price_curr["code"] == stock]
            if len(curr_row) == 0:
                continue

            curr_open = float(curr_row["open"].iloc[0])
            curr_close = float(curr_row["close"].iloc[0])
            curr_high = float(curr_row["high"].iloc[0])
            curr_limit = float(curr_row["high_limit"].iloc[0])

            if abs(curr_open - curr_limit) / curr_limit < 0.01:
                continue

            intra_return = (curr_close - curr_open) / curr_open * 100
            max_return = (curr_high - curr_open) / curr_open * 100

            signals.append(
                {
                    "stock": stock,
                    "market_cap": round(mc, 1),
                    "intra_return": round(intra_return, 2),
                    "max_return": round(max_return, 2),
                    "is_win": intra_return > 0,
                }
            )
        except:
            continue

    return signals, zt_count


YEARS = [2021, 2022, 2023]
all_results = {}

for year in YEARS:
    print(f"\n{'=' * 60}")
    print(f"处理 {year} 年")
    print(f"{'=' * 60}")

    all_dates = list(
        get_trade_days(start_date=f"{year}-01-01", end_date=f"{year}-12-31")
    )
    all_dates = [str(d) if hasattr(d, "strftime") else d for d in all_dates]

    months = [
        f"{year}-01",
        f"{year}-02",
        f"{year}-03",
        f"{year}-04",
        f"{year}-05",
        f"{year}-06",
        f"{year}-07",
        f"{year}-08",
        f"{year}-09",
        f"{year}-10",
        f"{year}-11",
        f"{year}-12",
    ]

    sample_dates = []
    for m in months:
        m_dates = [d for d in all_dates if d.startswith(m)]
        if len(m_dates) >= 5:
            sample_dates.extend(m_dates[:: len(m_dates) // 5][:5])

    print(f"采样日期数: {len(sample_dates)}")

    all_signals = []
    total_zt = 0
    triggered_days = 0

    for i in range(2, len(sample_dates)):
        prev_prev_date = sample_dates[i - 2]
        prev_date = sample_dates[i - 1]
        curr_date = sample_dates[i]

        print(f"  {prev_date} -> {curr_date}", end="")

        signals, zt_count = get_second_board_signals(
            prev_date, curr_date, prev_prev_date, min_zt_count=10
        )
        total_zt += zt_count

        if zt_count >= 10:
            triggered_days += 1
            print(f" | ZT:{zt_count} | 信号:{len(signals)}")
        else:
            print(f" | ZT:{zt_count} | 情绪不足")

        for s in signals:
            s["date"] = curr_date
            all_signals.append(s)

    if len(all_signals) == 0:
        print(f"\n{year}年无信号")
        all_results[year] = {"total": 0, "avg_return": 0, "win_rate": 0}
        continue

    df = pd.DataFrame(all_signals)

    total = len(df)
    avg_return = df["intra_return"].mean()
    avg_max = df["max_return"].mean()
    win_rate = df["is_win"].sum() / total * 100
    max_loss = df["intra_return"].min()
    max_win = df["intra_return"].max()

    df_sorted = df.sort_values("date")
    df_sorted["cum"] = (1 + df_sorted["intra_return"] / 100).cumprod() - 1
    rolling_max = df_sorted["cum"].expanding().max()
    max_dd = (rolling_max - df_sorted["cum"]).max() * 100

    wins = df[df["intra_return"] > 0]["intra_return"]
    losses = df[df["intra_return"] <= 0]["intra_return"]
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = abs(losses.mean()) if len(losses) > 0 else 0
    pl_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    monthly = df.groupby(df["date"].str[:7])["intra_return"].sum()

    all_results[year] = {
        "sample_signals": total,
        "est_annual": int(total * 12),
        "avg_return": round(avg_return, 2),
        "avg_max": round(avg_max, 2),
        "win_rate": round(win_rate, 1),
        "max_dd": round(max_dd, 2),
        "max_loss": round(max_loss, 2),
        "max_win": round(max_win, 2),
        "pl_ratio": round(pl_ratio, 2),
        "triggered_days": triggered_days,
        "avg_zt": round(total_zt / len(sample_dates), 1),
        "monthly_std": round(monthly.std(), 2),
        "positive_months": (monthly > 0).sum(),
        "negative_months": (monthly < 0).sum(),
    }

    print(f"\n{year}年统计:")
    print(f"  样本信号: {total}")
    print(f"  推算全年: ~{int(total * 12)}")
    print(f"  平均收益: {avg_return:.2f}%")
    print(f"  胜率: {win_rate:.1f}%")
    print(f"  最大回撤: {max_dd:.2f}%")
    print(f"  盈亏比: {pl_ratio:.2f}")

print("\n" + "=" * 80)
print("年度对比汇总")
print("=" * 80)

summary_df = pd.DataFrame(all_results).T
summary_df.index.name = "年份"
print(summary_df.to_string())

print("\n" + "=" * 80)
print("稳定性分析")
print("=" * 80)

if len(all_results) >= 2:
    returns = [all_results[y]["avg_return"] for y in YEARS if y in all_results]
    winrates = [all_results[y]["win_rate"] for y in YEARS if y in all_results]

    positive_years = sum(1 for r in returns if r > 0)
    winrate_range = max(winrates) - min(winrates) if winrates else 0

    print(f"\n收益分析:")
    print(f"  正收益年数: {positive_years}/{len(returns)}")
    print(f"  收益范围: {min(returns):.2f}% ~ {max(returns):.2f}%")

    print(f"\n胜率分析:")
    print(f"  胜率范围: {min(winrates):.1f}% ~ {max(winrates):.1f}%")
    print(f"  胜率差异: {winrate_range:.1f}%")

    print(f"\n通过门槛检查:")
    print(
        f"  至少2年正收益: {'PASS' if positive_years >= 2 else 'FAIL'} ({positive_years}年)"
    )
    print(
        f"  胜率差异<15%: {'PASS' if winrate_range < 15 else 'FAIL'} ({winrate_range:.1f}%)"
    )

    if positive_years >= 2 and winrate_range < 15:
        print(f"\n稳定性判定: 稳定")
        print(f"决策: Go")
    elif positive_years >= 1 or winrate_range < 20:
        print(f"\n稳定性判定: 部分稳定")
        print(f"决策: Watch")
    else:
        print(f"\n稳定性判定: 不稳定")
        print(f"决策: No-Go")

print("\n完成!")
