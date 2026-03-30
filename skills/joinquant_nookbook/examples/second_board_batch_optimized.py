#!/usr/bin/env python3
"""
任务04v2优化版：二板2021-2023实测验证（批量查询版）
使用批量查询减少API调用次数
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("二板2021-2023实测验证（批量查询优化版）")
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
        fields=["close", "high_limit", "volume", "low", "high"],
        panel=False,
        skip_paused=True,
    )

    print(f"价格数据shape: {prices.shape if hasattr(prices, 'shape') else len(prices)}")

    zt_info = {}
    for date in trade_days:
        day_data = (
            prices[prices.index.get_level_values(1) == date]
            if hasattr(prices.index, "get_level_values")
            else prices[prices["time"] == date]
        )

        if len(day_data) == 0:
            zt_info[date] = {"zt_count": 0, "zt_stocks": []}
            continue

        zt_stocks = (
            day_data[day_data["close"] == day_data["high_limit"]]["code"].tolist()
            if "code" in day_data.columns
            else []
        )
        zt_info[date] = {"zt_count": len(zt_stocks), "zt_stocks": zt_stocks}

    return zt_info, trade_days


def quick_backtest_year_batch(year, threshold=10):
    """批量版单年回测"""
    print(f"\n{'=' * 60}")
    print(f"测试 {year} 年（批量查询）")
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
            prices_df = get_price(
                second_board,
                start_date=prev2,
                end_date=next_date,
                fields=["close", "high_limit", "volume", "low", "high", "open"],
                panel=False,
                skip_paused=True,
            )

            if prices_df is None or len(prices_df) == 0:
                continue

            valid_stocks = []
            for stock in second_board:
                try:
                    stock_data = (
                        prices_df[prices_df["code"] == stock]
                        if "code" in prices_df.columns
                        else prices_df.loc[stock]
                    )

                    if len(stock_data) < 3:
                        continue

                    vol_data = stock_data["volume"].values
                    if len(vol_data) >= 2:
                        vol_ratio = vol_data[-2] / vol_data[-3]
                        if vol_ratio > 1.875:
                            continue

                    low_high = stock_data[["low", "high"]].values
                    if low_high[-2][0] == low_high[-2][1]:
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
                target_data = (
                    prices_df[prices_df["code"] == target]
                    if "code" in prices_df.columns
                    else prices_df.loc[target]
                )
                next_day = (
                    target_data[target_data.index.get_level_values(0) == next_date]
                    if hasattr(target_data.index, "get_level_values")
                    else target_data.iloc[-1]
                )

                if len(next_day) == 0:
                    continue

                open_p = (
                    next_day["open"].iloc[0]
                    if hasattr(next_day, "iloc")
                    else next_day["open"]
                )
                high_p = (
                    next_day["high"].iloc[0]
                    if hasattr(next_day, "iloc")
                    else next_day["high"]
                )
                close_p = (
                    next_day["close"].iloc[0]
                    if hasattr(next_day, "iloc")
                    else next_day["close"]
                )
                limit_p = (
                    next_day["high_limit"].iloc[0]
                    if hasattr(next_day, "iloc")
                    else next_day["high_limit"]
                )

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

        except Exception as e:
            print(f"日期{date}处理失败: {e}")
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
        year_data[yr] = quick_backtest_year_batch(yr)
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

output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output/second_board_2021_2023_batch.json"
with open(output_path, "w") as f:
    json.dump(year_data, f, indent=2)
print(f"结果已保存: {output_path}")

print("=" * 80)
