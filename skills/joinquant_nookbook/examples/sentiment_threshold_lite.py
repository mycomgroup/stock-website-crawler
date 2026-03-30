#!/usr/bin/env python3
"""
任务06v2：情绪开关阈值优化 - 简化版
测试不同涨停家数阈值，找出最优阈值
简化：减少采样频率，只测试关键阈值
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务06v2：情绪开关阈值优化")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2025-03-28"
OOS_START = "2024-01-01"

thresholds = [0, 20, 30, 40, 50, 60, 80, 100]


def get_zt_count(date):
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        if len(all_stocks) > 2000:
            all_stocks = all_stocks[:2000]

        df = get_price(
            all_stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        zt_count = len(df[df["close"] == df["high_limit"]])
        return zt_count
    except:
        return 0


def test_threshold_fast(date_list, threshold):
    signal_count = 0
    total_return = 0
    win_count = 0
    total_profit = 0
    total_loss = 0

    for i in range(len(date_list)):
        date_str = (
            date_list[i]
            if isinstance(date_list[i], str)
            else date_list[i].strftime("%Y-%m-%d")
        )

        try:
            zt_count = get_zt_count(date_str)

            if threshold > 0 and zt_count < threshold:
                continue

            signal_count += 1

            prev_zt_stocks = []
            if i > 0:
                prev_date_str = (
                    date_list[i - 1]
                    if isinstance(date_list[i - 1], str)
                    else date_list[i - 1].strftime("%Y-%m-%d")
                )
                prev_all = get_all_securities("stock", prev_date_str).index.tolist()
                prev_all = [
                    s
                    for s in prev_all
                    if not (
                        s.startswith("68") or s.startswith("4") or s.startswith("8")
                    )
                ][:500]

                prev_df = get_price(
                    prev_all,
                    end_date=prev_date_str,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                    fill_paused=False,
                )
                prev_df = prev_df.dropna()
                prev_zt_stocks = list(
                    prev_df[prev_df["close"] == prev_df["high_limit"]]["code"]
                )[:10]

            if len(prev_zt_stocks) == 0:
                continue

            next_days = get_trade_days(
                date_str,
                (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=5)).strftime(
                    "%Y-%m-%d"
                ),
            )
            if len(next_days) < 2:
                continue
            next_date = next_days[1] if next_days[0] == date_str else next_days[0]

            day_returns = []
            for stock in prev_zt_stocks[:5]:
                try:
                    prev_close_df = get_price(
                        stock,
                        end_date=prev_date_str,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    today_open_df = get_price(
                        stock,
                        end_date=date_str,
                        count=1,
                        fields=["open", "high_limit"],
                        panel=False,
                    )
                    next_close_df = get_price(
                        stock,
                        end_date=next_date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )

                    if (
                        len(prev_close_df) > 0
                        and len(today_open_df) > 0
                        and len(next_close_df) > 0
                    ):
                        prev_close = prev_close_df.iloc[0]["close"]
                        today_open = today_open_df.iloc[0]["open"]
                        next_close = next_close_df.iloc[0]["close"]

                        if today_open < today_open_df.iloc[0]["high_limit"]:
                            open_ratio = (today_open / prev_close - 1) * 100
                            if 0 <= open_ratio <= 3:
                                ret = (next_close / today_open - 1) * 100
                                day_returns.append(ret)

                                if ret > 0:
                                    win_count += 1
                                    total_profit += ret
                                else:
                                    total_loss += abs(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                total_return += avg_ret
        except:
            continue

    if signal_count == 0:
        return None

    avg_return = total_return / signal_count
    win_rate = win_count / signal_count * 100
    pl_ratio = total_profit / total_loss if total_loss > 0 else 0

    return {
        "threshold": threshold,
        "signal_count": signal_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
        "profit_loss_ratio": round(pl_ratio, 2),
    }


print("\n获取交易日列表...")
all_days = get_trade_days(START_DATE, END_DATE)
sample_days = all_days[::10]
oos_days = [d for d in sample_days if d >= OOS_START]
in_days = [d for d in sample_days if d < OOS_START]

print(f"样本内交易日: {len(in_days)}")
print(f"样本外交易日: {len(oos_days)}")

print("\n" + "=" * 80)
print("样本内测试")
print("=" * 80)

in_results = []
for t in thresholds:
    print(f"\n阈值 {t}...")
    r = test_threshold_fast(in_days, t)
    if r:
        in_results.append(r)
        print(
            f"  信号: {r['signal_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("样本外测试")
print("=" * 80)

oos_results = []
for t in thresholds:
    print(f"\n阈值 {t}...")
    r = test_threshold_fast(oos_days, t)
    if r:
        oos_results.append(r)
        print(
            f"  信号: {r['signal_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

if len(in_results) > 0:
    in_df = pd.DataFrame(in_results)
    print("\n【样本内】")
    print(in_df.to_string(index=False))

if len(oos_results) > 0:
    oos_df = pd.DataFrame(oos_results)
    print("\n【样本外】")
    print(oos_df.to_string(index=False))

all_results = {"in_sample": in_results, "out_of_sample": oos_results}
with open(
    "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_threshold_results.json",
    "w",
) as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print("\n研究完成!")
