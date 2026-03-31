#!/usr/bin/env python3
"""
任务07：情绪指标精细化阈值搜索 - 快速版
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务07：情绪指标精细化阈值搜索（快速版）")
print("=" * 80)

START_DATE = "2020-01-01"
END_DATE = "2025-03-30"

thresholds_free_point = [20, 25, 30, 35]
thresholds_start_line = [40, 45, 50, 55, 60]
all_thresholds = [0] + thresholds_free_point + thresholds_start_line

print(f"\n阈值范围: {all_thresholds}")


def get_zt_count_fast(date):
    """快速获取涨停家数"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ][:1000]

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
    except:
        return 0


def test_strategy_fast(strategy_name, threshold, sample_dates):
    """快速测试策略"""
    signal_count = 0
    returns = []
    wins = 0

    for i in range(len(sample_dates)):
        date_str = sample_dates[i]

        try:
            zt_count = get_zt_count_fast(date_str)

            if threshold > 0 and zt_count < threshold:
                continue

            signal_count += 1

            if strategy_name == "first_board":
                all_stocks = get_all_securities("stock", date_str).index.tolist()
                all_stocks = [
                    s
                    for s in all_stocks
                    if not (
                        s.startswith("68") or s.startswith("4") or s.startswith("8")
                    )
                ]

                df = get_price(
                    all_stocks,
                    end_date=date_str,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                zt_stocks = list(df[df["close"] == df["high_limit"]]["code"])[:5]

                if len(zt_stocks) > 0:
                    stock = zt_stocks[0]
                    price_df = get_price(
                        stock, end_date=date_str, count=1, fields=["close"]
                    )
                    if len(price_df) > 0:
                        close_price = price_df.iloc[0]["close"]
                        ret = (close_price / close_price - 1) * 100
                        returns.append(ret)
                        if ret > 0:
                            wins += 1

            elif strategy_name == "smallcap_defense":
                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.circulating_market_cap >= 15,
                    valuation.circulating_market_cap <= 60,
                )
                df = get_fundamentals(q, date=date_str)

                if not df.empty:
                    stock = df.iloc[0]["code"]
                    price_df = get_price(
                        stock, end_date=date_str, count=1, fields=["close"]
                    )
                    if len(price_df) > 0:
                        close_price = price_df.iloc[0]["close"]
                        ret = (close_price / close_price - 1) * 100
                        returns.append(ret)
                        if ret > 0:
                            wins += 1

        except:
            continue

    if signal_count == 0:
        return None

    avg_ret = np.mean(returns) if len(returns) > 0 else 0
    win_rate = wins / signal_count * 100 if signal_count > 0 else 0

    return {
        "threshold": threshold,
        "strategy": strategy_name,
        "signal_count": signal_count,
        "avg_return": round(avg_ret, 3),
        "win_rate": round(win_rate, 2),
    }


print("\n获取交易日...")
all_days = get_trade_days(START_DATE, END_DATE)
sample_days = all_days[::20]

print(f"采样天数: {len(sample_days)}")

results = {"first_board": [], "smallcap_defense": []}

print("\n" + "=" * 80)
print("阈值搜索")
print("=" * 80)

for threshold in all_thresholds:
    print(f"\n阈值 {threshold}:")

    r1 = test_strategy_fast("first_board", threshold, sample_days)
    if r1:
        results["first_board"].append(r1)
        print(f"  首板低开: 信号{r1['signal_count']}, 收益{r1['avg_return']}%")

    r2 = test_strategy_fast("smallcap_defense", threshold, sample_days)
    if r2:
        results["smallcap_defense"].append(r2)
        print(f"  小市值防守: 信号{r2['signal_count']}, 收益{r2['avg_return']}%")

print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

if len(results["first_board"]) > 0:
    fb_df = pd.DataFrame(results["first_board"])
    print("\n【首板低开】")
    print(fb_df.to_string(index=False))

if len(results["smallcap_defense"]) > 0:
    def_df = pd.DataFrame(results["smallcap_defense"])
    print("\n【小市值防守线】")
    print(def_df.to_string(index=False))

result_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/task07_threshold_quick.json"
with open(result_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n结果保存: {result_file}")
print("\n完成！")
