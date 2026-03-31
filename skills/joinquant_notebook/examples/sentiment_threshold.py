#!/usr/bin/env python3
"""
任务06v2：情绪开关阈值优化
测试不同涨停家数阈值，找出最优阈值
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务06v2：情绪开关阈值优化")
print("测试阈值：0(基准), 20, 30, 40, 50, 60, 80, 100")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2025-03-28"
OOS_START = "2024-01-01"

thresholds = [0, 20, 30, 40, 50, 60, 80, 100]


def get_zt_stocks(date):
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
    return list(zt_df["code"])


def select_first_board_low_open(date, prev_date):
    prev_zt = get_zt_stocks(prev_date)
    if len(prev_zt) == 0:
        return []

    selected = []
    for stock in prev_zt[:30]:
        try:
            prev_price = get_price(
                stock, end_date=prev_date, count=1, fields=["close"], panel=False
            )
            today_price = get_price(
                stock,
                end_date=date,
                count=1,
                fields=["open", "close", "high_limit"],
                panel=False,
            )

            if len(prev_price) == 0 or len(today_price) == 0:
                continue

            prev_close = prev_price.iloc[0]["close"]
            today_open = today_price.iloc[0]["open"]

            open_ratio = (today_open / prev_close - 1) * 100

            if 0.5 <= open_ratio <= 1.5:
                if today_open < today_price.iloc[0]["high_limit"]:
                    q = query(valuation.code, valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    )
                    val_df = get_fundamentals(q, date=date)
                    if len(val_df) > 0:
                        market_cap = val_df.iloc[0]["circulating_market_cap"]
                        if 50 <= market_cap <= 150:
                            selected.append(stock)
        except:
            continue

    return selected


def backtest_threshold(date_list, threshold, period_name="样本内"):
    results = []
    signal_count = 0
    win_count = 0
    total_profit = 0
    total_loss = 0
    max_profit_sum = 0
    daily_returns = []

    for i in range(1, len(date_list)):
        date = date_list[i]
        prev_date = date_list[i - 1]
        date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else date
        prev_date_str = (
            prev_date.strftime("%Y-%m-%d")
            if hasattr(prev_date, "strftime")
            else prev_date
        )

        try:
            zt_count = len(get_zt_stocks(prev_date_str))

            if threshold > 0 and zt_count < threshold:
                continue

            selected = select_first_board_low_open(date_str, prev_date_str)

            if len(selected) == 0:
                continue

            signal_count += 1

            next_days = get_trade_days(
                date_str,
                (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=10)).strftime(
                    "%Y-%m-%d"
                ),
            )
            if len(next_days) < 2:
                continue
            next_date = next_days[1] if next_days[0] == date_str else next_days[0]

            day_returns = []
            day_max_returns = []
            for stock in selected[:3]:
                try:
                    buy_price = get_price(
                        stock, end_date=date_str, count=1, fields=["open"], panel=False
                    )
                    sell_price = get_price(
                        stock,
                        end_date=next_date,
                        count=1,
                        fields=["close", "high"],
                        panel=False,
                    )

                    if len(buy_price) > 0 and len(sell_price) > 0:
                        buy_open = buy_price.iloc[0]["open"]
                        sell_close = sell_price.iloc[0]["close"]
                        sell_high = sell_price.iloc[0]["high"]

                        ret = (sell_close / buy_open - 1) * 100
                        max_ret = (sell_high / buy_open - 1) * 100

                        day_returns.append(ret)
                        day_max_returns.append(max_ret)

                        if ret > 0:
                            win_count += 1
                            total_profit += ret
                        else:
                            total_loss += abs(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                avg_max_ret = np.mean(day_max_returns)

                daily_returns.append(avg_ret)
                max_profit_sum += avg_max_ret

                results.append(
                    {
                        "date": date_str,
                        "zt_count": zt_count,
                        "avg_return": avg_ret,
                        "avg_max_return": avg_max_ret,
                        "stocks": len(day_returns),
                    }
                )
        except:
            continue

    if signal_count == 0:
        return None

    avg_return = np.mean(daily_returns) if len(daily_returns) > 0 else 0
    win_rate = (
        win_count / (win_count + (signal_count - win_count)) if signal_count > 0 else 0
    )
    profit_loss_ratio = total_profit / total_loss if total_loss > 0 else 0
    avg_max_profit = max_profit_sum / signal_count if signal_count > 0 else 0

    return {
        "threshold": threshold,
        "period": period_name,
        "signal_count": signal_count,
        "avg_return": avg_return,
        "win_rate": win_rate * 100,
        "avg_max_profit": avg_max_profit,
        "profit_loss_ratio": profit_loss_ratio,
        "total_profit": total_profit,
        "total_loss": total_loss,
    }


all_trade_days = get_trade_days(START_DATE, END_DATE)
sample_days = all_trade_days[::3]
oos_days = [
    d
    for d in sample_days
    if (d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else d) >= OOS_START
]

print(f"\n采样交易日数: {len(sample_days)}")
print(f"样本外交易日数: {len(oos_days)}")

print("\n" + "=" * 80)
print("样本内测试 (2021-01-01 ~ 2023-12-31)")
print("=" * 80)

sample_in_days = [
    d
    for d in sample_days
    if (d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else d) < OOS_START
]
print(f"样本内交易日数: {len(sample_in_days)}")

in_sample_results = []
for threshold in thresholds:
    print(f"\n测试阈值: {threshold}")
    result = backtest_threshold(sample_in_days, threshold, "样本内")
    if result:
        in_sample_results.append(result)
        print(f"  信号数量: {result['signal_count']}")
        print(f"  日内收益均值: {result['avg_return']:.3f}%")
        print(f"  胜率: {result['win_rate']:.2f}%")
        print(f"  最大收益均值: {result['avg_max_profit']:.3f}%")
        print(f"  盈亏比: {result['profit_loss_ratio']:.2f}")

print("\n" + "=" * 80)
print("样本外测试 (2024-01-01 ~ 2025-03-28)")
print("=" * 80)

oos_results = []
for threshold in thresholds:
    print(f"\n测试阈值: {threshold}")
    result = backtest_threshold(oos_days, threshold, "样本外")
    if result:
        oos_results.append(result)
        print(f"  信号数量: {result['signal_count']}")
        print(f"  日内收益均值: {result['avg_return']:.3f}%")
        print(f"  胜率: {result['win_rate']:.2f}%")
        print(f"  最大收益均值: {result['avg_max_profit']:.3f}%")
        print(f"  盈亏比: {result['profit_loss_ratio']:.2f}")

print("\n" + "=" * 80)
print("阈值对比汇总表")
print("=" * 80)

if len(in_sample_results) > 0:
    in_df = pd.DataFrame(in_sample_results)
    print("\n【样本内结果】")
    print(
        in_df[
            [
                "threshold",
                "signal_count",
                "avg_return",
                "win_rate",
                "avg_max_profit",
                "profit_loss_ratio",
            ]
        ].to_string(index=False)
    )

if len(oos_results) > 0:
    oos_df = pd.DataFrame(oos_results)
    print("\n【样本外结果】")
    print(
        oos_df[
            [
                "threshold",
                "signal_count",
                "avg_return",
                "win_rate",
                "avg_max_profit",
                "profit_loss_ratio",
            ]
        ].to_string(index=False)
    )

print("\n" + "=" * 80)
print("阈值-收益曲线分析")
print("=" * 80)

if len(in_sample_results) > 0:
    best_return_in = max(in_sample_results, key=lambda x: x["avg_return"])
    best_winrate_in = max(in_sample_results, key=lambda x: x["win_rate"])
    best_plratio_in = max(in_sample_results, key=lambda x: x["profit_loss_ratio"])

    print(f"\n【样本内最优阈值】")
    print(
        f"  收益最优: 阈值{best_return_in['threshold']} (收益{best_return_in['avg_return']:.3f}%)"
    )
    print(
        f"  胜率最优: 阈值{best_winrate_in['threshold']} (胜率{best_winrate_in['win_rate']:.2f}%)"
    )
    print(
        f"  盈亏比最优: 阈值{best_plratio_in['threshold']} (盈亏比{best_plratio_in['profit_loss_ratio']:.2f})"
    )

if len(oos_results) > 0:
    best_return_oos = max(oos_results, key=lambda x: x["avg_return"])
    best_winrate_oos = max(oos_results, key=lambda x: x["win_rate"])
    best_plratio_oos = max(oos_results, key=lambda x: x["profit_loss_ratio"])

    print(f"\n【样本外最优阈值】")
    print(
        f"  收益最优: 阈值{best_return_oos['threshold']} (收益{best_return_oos['avg_return']:.3f}%)"
    )
    print(
        f"  胜率最优: 阈值{best_winrate_oos['threshold']} (胜率{best_winrate_oos['win_rate']:.2f}%)"
    )
    print(
        f"  盈亏比最优: 阈值{best_plratio_oos['threshold']} (盈亏比{best_plratio_oos['profit_loss_ratio']:.2f})"
    )

all_results = {
    "in_sample": in_sample_results,
    "out_of_sample": oos_results,
}

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_threshold_results.json"
)
with open(result_file, "w") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n结果已保存至: {result_file}")

print("\n研究完成!")
