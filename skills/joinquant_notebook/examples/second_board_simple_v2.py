#!/usr/bin/env python3
"""
任务04v2：二板2021-2023实测验证（简化版）
使用count参数 + panel=False，避免复杂数据格式问题
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("二板2021-2023实测验证（简化版）")
print("=" * 80)


def get_zt_count_simple(date):
    """获取涨停家数（简化版）"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        zt_count = 0
        for i in range(0, len(all_stocks), 500):
            batch = all_stocks[i : i + 500]
            try:
                df = get_price(
                    batch,
                    end_date=date,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                if len(df) > 0:
                    zt_count += len(df[df["close"] == df["high_limit"]])
            except:
                pass
        return zt_count
    except:
        return 0


def backtest_year_simple(year, threshold=10):
    """简化版单年回测"""
    print(f"\n{'=' * 60}")
    print(f"测试 {year} 年")
    print(f"{'=' * 60}")

    trade_days = get_trade_days(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(trade_days)}")

    results = {"year": year, "signals": 0, "trades": 0, "wins": 0, "profits": []}

    for i in range(len(trade_days) - 1):
        date = trade_days[i]
        next_date = trade_days[i + 1]

        if i % 50 == 0:
            print(f"处理 {date}...")

        try:
            zt_count = get_zt_count_simple(date)
        except:
            continue

        if zt_count < threshold:
            continue

        if i < 2:
            continue

        prev_date = trade_days[i - 1]
        prev2_date = trade_days[i - 2]

        try:
            all_stocks = get_all_securities("stock", date).index.tolist()
            all_stocks = [
                s
                for s in all_stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            def is_zt(stock, d):
                try:
                    df = get_price(
                        stock,
                        end_date=d,
                        count=1,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    if len(df) > 0:
                        return df.iloc[0]["close"] == df.iloc[0]["high_limit"]
                except:
                    pass
                return False

            zt_today = [s for s in all_stocks[:300] if is_zt(s, date)]
            zt_prev = [s for s in all_stocks[:300] if is_zt(s, prev_date)]
            zt_prev2 = [s for s in all_stocks[:300] if is_zt(s, prev2_date)]

            second_board = list(set(zt_today) & set(zt_prev) - set(zt_prev2))

            if len(second_board) == 0:
                continue

            results["signals"] += len(second_board)

            valid_stocks = []
            for stock in second_board[:20]:
                try:
                    vol_df = get_price(
                        stock, end_date=date, count=2, fields=["volume"], panel=False
                    )
                    if len(vol_df) >= 2:
                        vol_ratio = (
                            vol_df.iloc[-1]["volume"] / vol_df.iloc[-2]["volume"]
                        )
                        if vol_ratio > 1.875:
                            continue

                    low_high = get_price(
                        stock,
                        end_date=date,
                        count=1,
                        fields=["low", "high"],
                        panel=False,
                    )
                    if (
                        len(low_high) > 0
                        and low_high.iloc[0]["low"] == low_high.iloc[0]["high"]
                    ):
                        continue

                    cap = get_fundamentals(
                        query(valuation.circulating_market_cap).filter(
                            valuation.code == stock
                        ),
                        date,
                    )
                    if len(cap) > 0:
                        valid_stocks.append(
                            (stock, cap["circulating_market_cap"].iloc[0])
                        )
                except:
                    continue

            if len(valid_stocks) == 0:
                continue

            valid_stocks.sort(key=lambda x: x[1])
            target = valid_stocks[0][0]

            try:
                next_df = get_price(
                    target,
                    end_date=next_date,
                    count=1,
                    fields=["open", "high", "close", "high_limit"],
                    panel=False,
                )
                if len(next_df) == 0:
                    continue

                open_p = next_df.iloc[0]["open"]
                high_p = next_df.iloc[0]["high"]
                close_p = next_df.iloc[0]["close"]
                limit_p = next_df.iloc[0]["high_limit"]

                if open_p >= limit_p * 0.99:
                    continue

                buy_p = open_p * 1.005
                profit = (close_p / buy_p - 1) * 100

                results["trades"] += 1
                results["profits"].append(profit)
                if profit > 0:
                    results["wins"] += 1

            except:
                continue

        except:
            continue

    if results["trades"] > 0:
        results["win_rate"] = results["wins"] / results["trades"] * 100
        results["avg_profit"] = np.mean(results["profits"])
        cum = np.cumsum(results["profits"])
        results["cumulative"] = cum[-1]
        peak = np.maximum.accumulate(cum)
        results["max_dd"] = np.max(peak - cum)
        print(
            f"\n{year}年完成: 交易{results['trades']}次, 胜率{results['win_rate']:.1f}%, 收益{results['cumulative']:.1f}%"
        )
    else:
        print(f"\n{year}年未完成交易")

    return results


print("\n开始逐年测试...")
year_data = {}

for yr in [2021, 2022, 2023]:
    try:
        year_data[yr] = backtest_year_simple(yr)
    except Exception as e:
        print(f"{yr}年测试失败: {e}")
        year_data[yr] = {"year": yr, "trades": 0, "cumulative": 0}

print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)
print(f"年份  信号  交易  胜率    日均收益  累计收益  最大回撤")
print("-" * 60)

for yr in [2021, 2022, 2023]:
    r = year_data[yr]
    if r.get("trades", 0) > 0:
        print(
            f"{yr}   {r['signals']}   {r['trades']}   {r['win_rate']:.1f}%  {r['avg_profit']:.2f}%  {r['cumulative']:.1f}%  {r['max_dd']:.1f}%"
        )
    else:
        print(f"{yr}   {r.get('signals', 0)}   {r['trades']}   未完成")

win_rates = [r["win_rate"] for r in year_data.values() if r.get("trades", 0) > 0]
cumulative = [r["cumulative"] for r in year_data.values()]

positive_years = len([c for c in cumulative if c > 0])
win_diff = max(win_rates) - min(win_rates) if len(win_rates) >= 2 else 100

print("\n稳定性判定:")
print(f"正收益年份: {positive_years}/3 (需≥2)")
print(f"胜率差异: {win_diff:.1f}% (需<15%)")

if positive_years >= 2 and win_diff < 15:
    print("判定: 稳定 ✓")
    decision = "Go"
elif positive_years >= 1 or win_diff < 20:
    print("判定: 需观察")
    decision = "Watch"
else:
    print("判定: 不稳定")
    decision = "No-Go"

print(f"\n最终决策: {decision}")
print("=" * 80)
