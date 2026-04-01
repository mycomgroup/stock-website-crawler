#!/usr/bin/env python3
"""
任务06v2：情绪开关阈值优化 - Notebook格式v3
修复选股逻辑：测试情绪开关的真实效果
"""

from jqdata import *
import numpy as np
import json
from datetime import datetime, timedelta

print("=" * 80)
print("任务06v2：情绪开关阈值优化")
print("修复选股逻辑，测试真实收益")
print("=" * 80)

thresholds = [0, 20, 30, 40, 50, 60, 80, 100]

all_dates = get_trade_days("2021-01-01", "2025-03-28")
test_dates = all_dates[::10]

OOS_START = "2024-01-01"

print(f"\n总交易日数: {len(all_dates)}")
print(f"采样日期数: {len(test_dates)}")

in_dates = [d for d in test_dates if str(d) < OOS_START]
oos_dates = [d for d in test_dates if str(d) >= OOS_START]

print(f"样本内日期: {len(in_dates)}")
print(f"样本外日期: {len(oos_dates)}")


def get_zt_count(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ][:1500]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    return len(df[df["close"] == df["high_limit"]])


def get_zt_stocks(date, limit=20):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ][:1500]

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
    return list(zt_df["code"])[:limit]


def test_threshold_simple(date_list, threshold, period_name):
    signal_count = 0
    total_return = 0
    total_trades = 0
    wins = 0

    for i in range(1, len(date_list)):
        prev_date = date_list[i - 1]
        date = date_list[i]

        try:
            zt_count = get_zt_count(prev_date)

            if threshold > 0 and zt_count < threshold:
                continue

            signal_count += 1

            zt_stocks = get_zt_stocks(prev_date, limit=10)

            if len(zt_stocks) == 0:
                continue

            day_returns = []
            for stock in zt_stocks:
                try:
                    prev_close_df = get_price(
                        stock,
                        end_date=prev_date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    today_df = get_price(
                        stock,
                        end_date=date,
                        count=1,
                        fields=["open", "close", "high_limit"],
                        panel=False,
                    )

                    if len(prev_close_df) > 0 and len(today_df) > 0:
                        prev_close = prev_close_df.iloc[0]["close"]
                        today_open = today_df.iloc[0]["open"]
                        today_close = today_df.iloc[0]["close"]
                        high_limit = today_df.iloc[0]["high_limit"]

                        open_pct = (today_open / prev_close - 1) * 100

                        if 0 <= open_pct <= 5 and today_open < high_limit:
                            ret = (today_close / today_open - 1) * 100
                            day_returns.append(ret)
                            total_trades += 1

                            if ret > 0:
                                wins += 1
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                total_return += avg_ret

        except Exception as e:
            continue

    if signal_count == 0:
        return None

    avg_return = total_return / signal_count
    win_rate = wins / total_trades * 100 if total_trades > 0 else 0

    return {
        "threshold": threshold,
        "period": period_name,
        "signal_count": signal_count,
        "trade_count": total_trades,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
    }


print("\n" + "=" * 80)
print("样本内测试 (2021-2023)")
print("=" * 80)

in_results = []
for t in thresholds:
    print(f"\n阈值 {t}...")
    r = test_threshold_simple(in_dates, t, "样本内")
    if r:
        in_results.append(r)
        print(
            f"  信号: {r['signal_count']}, 交易: {r['trade_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("样本外测试 (2024-01-01后)")
print("=" * 80)

oos_results = []
for t in thresholds:
    print(f"\n阈值 {t}...")
    r = test_threshold_simple(oos_dates, t, "样本外")
    if r:
        oos_results.append(r)
        print(
            f"  信号: {r['signal_count']}, 交易: {r['trade_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("阈值对比汇总")
print("=" * 80)

if len(in_results) > 0:
    print("\n【样本内】")
    for r in in_results:
        print(
            f"阈值{r['threshold']}: {r['signal_count']}信号, {r['avg_return']}%收益, {r['win_rate']}%胜率"
        )

if len(oos_results) > 0:
    print("\n【样本外】")
    for r in oos_results:
        print(
            f"阈值{r['threshold']}: {r['signal_count']}信号, {r['avg_return']}%收益, {r['win_rate']}%胜率"
        )

if len(in_results) > 0:
    best_in = max(in_results, key=lambda x: x["avg_return"])
    print(f"\n【样本内最优】阈值{best_in['threshold']}: {best_in['avg_return']}%收益")

if len(oos_results) > 0:
    best_oos = max(oos_results, key=lambda x: x["avg_return"])
    print(f"\n【样本外最优】阈值{best_oos['threshold']}: {best_oos['avg_return']}%收益")

output_data = {
    "in_sample": in_results,
    "out_of_sample": oos_results,
}

import os

os.makedirs("/Users/fengzhi/Downloads/git/testlixingren/output", exist_ok=True)

output_path = "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_threshold_results_v3.json"
try:
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存: {output_path}")
except Exception as e:
    print(f"\n保存失败: {e}")

print("\n=== 测试完成 ===")
