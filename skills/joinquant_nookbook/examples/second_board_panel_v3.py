#!/usr/bin/env python3
"""
任务04v2优化版v3：二板2021-2023实测验证（正确panel格式）
使用panel=True处理MultiIndex数据
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("二板2021-2023实测验证（panel格式修复版）")
print("=" * 80)


def batch_get_zt_info(start_date, end_date):
    """批量获取所有日期的涨停信息"""
    print(f"\n批量获取涨停数据: {start_date} 至 {end_date}")

    trade_days = get_trade_days(start_date, end_date)
    all_stocks = get_all_securities("stock", end_date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    print(f"股票数: {len(all_stocks)}, 交易日: {len(trade_days)}")

    prices = get_price(
        all_stocks,
        start_date=start_date,
        end_date=end_date,
        fields=["close", "high_limit"],
        panel=True,
        skip_paused=False,
    )

    print(f"价格数据shape: {prices.shape}")

    zt_info = {}
    for date in trade_days:
        try:
            day_prices = prices.loc[:, date]
            zt_mask = day_prices["close"] == day_prices["high_limit"]
            zt_stocks = day_prices.index[zt_mask].tolist()
            zt_info[date] = {"zt_count": len(zt_stocks), "zt_stocks": zt_stocks}
        except:
            zt_info[date] = {"zt_count": 0, "zt_stocks": []}

    return zt_info, trade_days


def quick_backtest_year(year, threshold=10):
    """单年回测"""
    print(f"\n{'=' * 60}")
    print(f"测试 {year} 年")
    print(f"{'=' * 60}")

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    zt_info, trade_days = batch_get_zt_info(start_date, end_date)

    results = {
        "year": year,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "max_profits": [],
    }

    print(f"\n开始逐日筛选...")

    for i in range(len(trade_days) - 1):
        date = trade_days[i]
        next_date = trade_days[i + 1]

        zt_count = zt_info.get(date, {}).get("zt_count", 0)

        if zt_count < threshold:
            continue

        if i < 2:
            continue

        prev1 = trade_days[i - 1]
        prev2 = trade_days[i - 2]

        zt_today = zt_info.get(date, {}).get("zt_stocks", [])
        zt_prev1 = zt_info.get(prev1, {}).get("zt_stocks", [])
        zt_prev2 = zt_info.get(prev2, {}).get("zt_stocks", [])

        second_board = list(set(zt_today) & set(zt_prev1) - set(zt_prev2))

        if len(second_board) == 0:
            continue

        results["signals"] += len(second_board)

        try:
            prices_3d = get_price(
                second_board[:50],
                start_date=prev2,
                end_date=next_date,
                fields=["close", "high_limit", "volume", "low", "high", "open"],
                panel=True,
                skip_paused=False,
            )

            valid_stocks = []
            for stock in second_board[:50]:
                try:
                    stock_prices = prices_3d.loc[stock]

                    vol_prev = stock_prices.loc[prev1, "volume"]
                    vol_prev2 = stock_prices.loc[prev2, "volume"]

                    if vol_prev / vol_prev2 > 1.875:
                        continue

                    low_prev = stock_prices.loc[prev1, "low"]
                    high_prev = stock_prices.loc[prev1, "high"]
                    if low_prev == high_prev:
                        continue

                    q = query(valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    )
                    cap = get_fundamentals(q, date=date)
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
                next_prices = prices_3d.loc[target, next_date]

                open_p = next_prices["open"]
                high_p = next_prices["high"]
                close_p = next_prices["close"]
                limit_p = next_prices["high_limit"]

                if open_p >= limit_p * 0.99:
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

        if i % 50 == 0:
            print(f"已处理 {i}/{len(trade_days)} 天, 交易: {results['trades']}")

    print(f"\n{year}年测试完成!")

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
            f"信号: {results['signals']}, 交易: {results['trades']}, 胜率: {results['win_rate']:.1f}%, 收益: {results['cumulative']:.1f}%"
        )
    else:
        print(f"未完成交易")

    return results


print("\n开始逐年测试...")
year_data = {}

for yr in [2021, 2022, 2023]:
    try:
        year_data[yr] = quick_backtest_year(yr)
    except Exception as e:
        print(f"{yr}年测试失败: {e}")
        year_data[yr] = {"year": yr, "trades": 0, "cumulative": 0}

print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)
print(f"年份  信号  交易  胜率    日均收益  最大收益  盈亏比  累计收益  最大回撤")
print("-" * 70)

for yr in [2021, 2022, 2023]:
    r = year_data[yr]
    if r.get("trades", 0) > 0:
        print(
            f"{yr}   {r['signals']}   {r['trades']}   {r['win_rate']:.1f}%  {r['avg_profit']:.2f}%  {r['avg_max_profit']:.2f}%  {r['pl_ratio']:.1f}  {r['cumulative']:.1f}%  {r['max_dd']:.1f}%"
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

output_path = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/second_board_2021_2023.json"
)
with open(output_path, "w") as f:
    json.dump(year_data, f, indent=2)
print(f"结果已保存: {output_path}")

print("=" * 80)
