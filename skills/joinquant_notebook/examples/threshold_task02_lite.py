#!/usr/bin/env python3
"""
阈值优化 - 基于task02简化版
只测试阈值对比，去掉策略回测框架
"""

from jqdata import *
import numpy as np
import json
from datetime import datetime, timedelta

print("=" * 60)
print("情绪开关阈值优化测试")
print("基于task02简化版")
print("=" * 60)

OOS_START = "2024-01-01"

thresholds = [0, 20, 30, 40, 50, 60, 80, 100]


def get_zt_count(date):
    stocks = get_all_securities("stock", date).index.tolist()[:1200]
    stocks = [
        s
        for s in stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    return len(df[df["close"] == df["high_limit"]])


def select_first_board_low_open(date, prev_date):
    prev_zt = get_zt_count(prev_date)

    prev_stocks = get_all_securities("stock", prev_date).index.tolist()[:1000]
    prev_stocks = [
        s
        for s in prev_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    prev_df = get_price(
        prev_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    prev_df = prev_df.dropna()
    zt_list = list(prev_df[prev_df["close"] == prev_df["high_limit"]]["code"])[:30]

    selected = []
    for stock in zt_list:
        try:
            prev_close_df = get_price(
                stock, end_date=prev_date, count=1, fields=["close"], panel=False
            )
            today_df = get_price(
                stock,
                end_date=date,
                count=1,
                fields=["open", "high_limit"],
                panel=False,
            )

            if len(prev_close_df) > 0 and len(today_df) > 0:
                prev_close = prev_close_df.iloc[0]["close"]
                today_open = today_df.iloc[0]["open"]

                open_ratio = (today_open / prev_close - 1) * 100

                if 0.5 <= open_ratio <= 1.5:
                    if today_open < today_df.iloc[0]["high_limit"]:
                        selected.append((stock, open_ratio))
        except:
            pass

    return [s[0] for s in selected]


def test_threshold(date_list, threshold, period_name):
    signal_count = 0
    trade_count = 0
    total_return = 0
    wins = 0

    for i in range(1, len(date_list)):
        date = date_list[i]
        prev = date_list[i - 1]

        date_str = str(date)[:10] if hasattr(date, "__str__") else date
        prev_str = str(prev)[:10] if hasattr(prev, "__str__") else prev

        try:
            zt = get_zt_count(prev_str)

            if threshold > 0 and zt < threshold:
                continue

            signal_count += 1

            selected = select_first_board_low_open(date_str, prev_str)

            if len(selected) == 0:
                continue

            next_dates = get_trade_days(
                date_str,
                (
                    datetime.strptime(date_str[:10], "%Y-%m-%d") + timedelta(days=10)
                ).strftime("%Y-%m-%d"),
            )
            if len(next_dates) < 2:
                continue
            next_date = (
                next_dates[1] if next_dates[0] == date_str[:10] else next_dates[0]
            )

            day_returns = []
            for stock in selected[:5]:
                try:
                    buy_df = get_price(
                        stock,
                        end_date=date_str[:10],
                        count=1,
                        fields=["open"],
                        panel=False,
                    )
                    sell_df = get_price(
                        stock, end_date=next_date, count=1, fields=["high"], panel=False
                    )

                    if len(buy_df) > 0 and len(sell_df) > 0:
                        buy = buy_df.iloc[0]["open"]
                        sell = sell_df.iloc[0]["high"]
                        ret = (sell / buy - 1) * 100
                        day_returns.append(ret)
                        trade_count += 1

                        if ret > 0:
                            wins += 1
                except:
                    pass

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                total_return += avg_ret

        except:
            pass

    if signal_count == 0:
        return None

    avg_return = total_return / signal_count
    win_rate = wins / trade_count * 100 if trade_count > 0 else 0

    return {
        "threshold": threshold,
        "period": period_name,
        "signals": signal_count,
        "trades": trade_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
    }


all_dates = get_trade_days("2021-01-01", "2025-03-28")
test_dates = all_dates[::15]

in_dates = [d for d in test_dates if str(d)[:10] < OOS_START]
oos_dates = [d for d in test_dates if str(d)[:10] >= OOS_START]

print(f"\n总日期: {len(test_dates)}, 样本内: {len(in_dates)}, 样本外: {len(oos_dates)}")

print("\n" + "=" * 60)
print("样本内测试 (2021-2023)")
print("=" * 60)

in_results = []
for t in thresholds:
    r = test_threshold(in_dates, t, "in")
    if r:
        in_results.append(r)
        print(
            f"阈值{t}: {r['signals']}信号, {r['trades']}交易, {r['avg_return']}%, 胜率{r['win_rate']}%"
        )

print("\n" + "=" * 60)
print("样本外测试 (2024-01-01后)")
print("=" * 60)

oos_results = []
for t in thresholds:
    r = test_threshold(oos_dates, t, "oos")
    if r:
        oos_results.append(r)
        print(
            f"阈值{t}: {r['signals']}信号, {r['trades']}交易, {r['avg_return']}%, 胜率{r['win_rate']}%"
        )

print("\n" + "=" * 60)
print("汇总对比")
print("=" * 60)

if len(in_results) > 0:
    print("\n【样本内】阈值 | 信号 | 收益 | 胜率")
    for r in in_results:
        print(
            f"  {r['threshold']} | {r['signals']} | {r['avg_return']}% | {r['win_rate']}%"
        )

if len(oos_results) > 0:
    print("\n【样本外】阈值 | 信号 | 收益 | 胜率")
    for r in oos_results:
        print(
            f"  {r['threshold']} | {r['signals']} | {r['avg_return']}% | {r['win_rate']}%"
        )

print("\n完成")
