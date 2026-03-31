#!/usr/bin/env python3
"""
任务04v2：二板2021-2023实测验证（最小版）
仅统计关键指标，不保存详细交易
"""

from jqdata import *
import numpy as np

print("=" * 60)
print("二板2021-2023实测验证（最小版）")
print("=" * 60)


def quick_backtest_year(year, threshold=10):
    """快速单年回测"""
    print(f"\n测试 {year} 年...")

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    trade_days = get_trade_days(start_date, end_date)

    results = {
        "year": year,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "max_profits": [],
    }

    for i in range(len(trade_days) - 1):
        date = trade_days[i]
        next_date = trade_days[i + 1]

        try:
            zt_count = len(
                [
                    s
                    for s in get_all_securities("stock", date).index
                    if not s.startswith(("68", "4", "8"))
                    and get_price(
                        s, date, count=1, fields=["close", "high_limit"], panel=False
                    ).iloc[0]["close"]
                    == get_price(
                        s, date, count=1, fields=["close", "high_limit"], panel=False
                    ).iloc[0]["high_limit"]
                ]
            )
        except:
            continue

        if zt_count < threshold:
            continue

        try:
            prev1 = trade_days[i - 1] if i > 0 else None
            prev2 = trade_days[i - 2] if i > 1 else None

            if not prev1 or not prev2:
                continue

            stocks_today = get_all_securities("stock", date).index
            stocks_today = [
                s for s in stocks_today if not s.startswith(("68", "4", "8"))
            ]

            def is_zt(stock, d):
                try:
                    df = get_price(
                        stock, d, count=1, fields=["close", "high_limit"], panel=False
                    )
                    return (
                        len(df) > 0 and df.iloc[0]["close"] == df.iloc[0]["high_limit"]
                    )
                except:
                    return False

            zt_today = [s for s in stocks_today if is_zt(s, date)]
            zt_prev1 = [s for s in stocks_today if is_zt(s, prev1)]
            zt_prev2 = [s for s in stocks_today if is_zt(s, prev2)]

            second_board = list(set(zt_today) & set(zt_prev1) - set(zt_prev2))

            if len(second_board) == 0:
                continue

            results["signals"] += len(second_board)

            valid_stocks = []
            for s in second_board[:10]:
                try:
                    hsl = HSL([s], date)
                    if s in hsl[0] and hsl[0][s] < 30:
                        vol_df = get_price(
                            s, date, count=2, fields=["volume"], panel=False
                        )
                        if len(vol_df) >= 2:
                            vol_ratio = (
                                vol_df.iloc[-1]["volume"] / vol_df.iloc[-2]["volume"]
                            )
                            if vol_ratio <= 1.875:
                                cap = get_fundamentals(
                                    query(valuation.circulating_market_cap).filter(
                                        valuation.code == s
                                    ),
                                    date,
                                )
                                if len(cap) > 0:
                                    valid_stocks.append(
                                        (s, cap.iloc[0]["circulating_market_cap"])
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
                    next_date,
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

                if open_p == limit_p:
                    continue

                buy_p = open_p * 1.005
                profit = (close_p / buy_p - 1) * 100
                max_profit = (high_p / buy_p - 1) * 100

                results["trades"] += 1
                results["profits"].append(profit)
                results["max_profits"].append(max_profit)
                if profit > 0:
                    results["wins"] += 1

            except:
                continue

        except:
            continue

    if results["trades"] > 0:
        results["win_rate"] = results["wins"] / results["trades"] * 100
        results["avg_profit"] = np.mean(results["profits"])
        results["avg_max_profit"] = np.mean(results["max_profits"])
        wins_list = [p for p in results["profits"] if p > 0]
        losses_list = [p for p in results["profits"] if p <= 0]
        avg_win = np.mean(wins_list) if wins_list else 0
        avg_loss = np.mean(losses_list) if losses_list else 1
        results["pl_ratio"] = abs(avg_win / avg_loss)

        cum = np.cumsum(results["profits"])
        results["cumulative"] = cum[-1]
        peak = np.maximum.accumulate(cum)
        results["max_dd"] = np.max(peak - cum)

    print(
        f"完成! 信号:{results['signals']} 交易:{results['trades']} 胜率:{results.get('win_rate', 0):.1f}% 收益:{results.get('cumulative', 0):.1f}%"
    )
    return results


print("\n开始逐年测试...")
year_data = {}
for yr in [2021, 2022, 2023]:
    try:
        year_data[yr] = quick_backtest_year(yr)
    except Exception as e:
        print(f"{yr}年测试失败: {e}")
        year_data[yr] = {"year": yr, "trades": 0, "cumulative": 0}

print("\n" + "=" * 60)
print("汇总结果")
print("=" * 60)
print(f"年份  信号  交易  胜率    日均收益  最大收益  盈亏比  累计收益  最大回撤")
print("-" * 70)
for yr in [2021, 2022, 2023]:
    r = year_data[yr]
    if r.get("trades", 0) > 0:
        print(
            f"{yr}   {r['signals']}   {r['trades']}   {r['win_rate']:.1f}%  {r['avg_profit']:.2f}%  {r['avg_max_profit']:.2f}%  {r['pl_ratio']:.1f}  {r['cumulative']:.1f}%  {r['max_dd']:.1f}%"
        )
    else:
        print(f"{yr}   {r['signals']}   {r['trades']}   未完成")

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
print("=" * 60)
