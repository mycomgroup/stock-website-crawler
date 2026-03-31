"""
任务02补充：情绪开关最近日期实测（简化版）
只测试2025年1-3月数据
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务02补充：情绪开关最近日期实测（简化版）")
print("测试期间：2025-01-01 至 2025-03-28")
print("=" * 80)


def get_zt_count(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    return len(zt_df)


def backtest_simple(start_date, end_date, zt_threshold=30, use_switch=True):
    print(f"\n回测: {start_date} 至 {end_date}, 阈值={zt_threshold}")

    all_dates = get_trade_days(start_date, end_date)
    print(f"交易日数: {len(all_dates)}")

    trades = 0
    wins = 0
    profits = []
    zt_list = []
    skipped = 0

    for i in range(1, len(all_dates) - 1):
        prev_date = all_dates[i - 1]
        curr_date = all_dates[i]
        next_date = all_dates[i + 1]

        try:
            zt_count = get_zt_count(prev_date)
            zt_list.append(zt_count)

            if use_switch and zt_count < zt_threshold:
                skipped += 1
                continue

            all_stocks = get_all_securities("stock", prev_date).index.tolist()
            all_stocks = [
                s
                for s in all_stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            df = get_price(
                all_stocks,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                fill_paused=False,
            )
            df = df.dropna()
            prev_zt = list(df[df["close"] == df["high_limit"]]["code"])

            if len(prev_zt) == 0:
                continue

            for stock in prev_zt[:10]:
                try:
                    prev_p = get_price(
                        stock,
                        end_date=prev_date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    curr_p = get_price(
                        stock,
                        end_date=curr_date,
                        count=1,
                        fields=["open", "high_limit"],
                        panel=False,
                    )

                    if len(prev_p) == 0 or len(curr_p) == 0:
                        continue

                    open_pct = (
                        curr_p.iloc[0]["open"] / prev_p.iloc[0]["close"] - 1
                    ) * 100

                    if (
                        0.5 <= open_pct <= 1.5
                        and curr_p.iloc[0]["open"] < curr_p.iloc[0]["high_limit"]
                    ):
                        next_p = get_price(
                            stock,
                            end_date=next_date,
                            count=1,
                            fields=["high", "close"],
                            panel=False,
                        )

                        if len(next_p) > 0:
                            buy_p = curr_p.iloc[0]["open"] * 1.005
                            profit = (next_p.iloc[0]["close"] / buy_p - 1) * 100
                            profits.append(profit)
                            trades += 1
                            if profit > 0:
                                wins += 1
                            break
                except:
                    pass

        except:
            pass

    if trades > 0:
        print(
            f"交易: {trades}, 胜率: {wins / trades * 100:.1f}%, 平均收益: {np.mean(profits):.2f}%, 累计: {np.sum(profits):.1f}%"
        )
        print(f"平均涨停: {np.mean(zt_list):.1f}, 范围: {min(zt_list)}-{max(zt_list)}")
        print(f"过滤天数: {skipped}/{len(all_dates)}")

    return {
        "trades": trades,
        "wins": wins,
        "profits": profits,
        "avg_zt": np.mean(zt_list) if zt_list else 0,
    }


print("\n测试1: 无开关")
r1 = backtest_simple("2025-01-01", "2025-03-28", 0, False)

print("\n测试2: 阈值30")
r2 = backtest_simple("2025-01-01", "2025-03-28", 30, True)

print("\n测试3: 阈值50")
r3 = backtest_simple("2025-01-01", "2025-03-28", 50, True)

print("\n" + "=" * 80)
print("结论")
print("=" * 80)

if r1["trades"] > 0 and r2["trades"] > 0:
    print(
        f"阈值30: 胜率 {r2['wins'] / r2['trades'] * 100:.1f}% vs 基准 {r1['wins'] / r1['trades'] * 100:.1f}%"
    )
if r1["trades"] > 0 and r3["trades"] > 0:
    print(
        f"阈值50: 胜率 {r3['wins'] / r3['trades'] * 100:.1f}% vs 基准 {r1['wins'] / r1['trades'] * 100:.1f}%"
    )

print("\n完成!")
