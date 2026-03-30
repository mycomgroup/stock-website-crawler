"""
任务04v2：二板2021-2023实测验证 - RiceQuant版本
RiceQuant API适配版本
"""

print("=" * 80)
print("任务04v2：二板策略2021-2023实测验证（RiceQuant版）")
print("=" * 80)

import numpy as np
from datetime import datetime


def get_zt_stocks(date):
    """获取涨停股票"""
    all_stocks = get_all_securities(["stock"])
    all_stocks = [
        s
        for s in all_stocks.index
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    zt_list = []
    for stock in all_stocks[:500]:  # RiceQuant批量查询限制
        try:
            prices = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=date)
            if prices is not None and len(prices) > 0:
                if prices[0]["close"] >= prices[0]["limit_up"] * 0.99:
                    zt_list.append(stock)
        except:
            pass
    return zt_list


def quick_backtest_year(year, threshold=10):
    """快速单年回测"""
    print(f"\n测试 {year} 年...")

    dates = get_trading_dates(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(dates)}")

    results = {
        "year": year,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "max_profits": [],
    }

    for i in range(len(dates) - 1):
        date = dates[i]
        next_date = dates[i + 1]

        try:
            zt_count = len(get_zt_stocks(date))
        except:
            zt_count = 0
            continue

        if zt_count < threshold:
            continue

        if i < 2:
            continue

        prev1 = dates[i - 1]
        prev2 = dates[i - 2]

        try:
            all_stocks = get_all_securities(["stock"])
            stocks_today = [
                s
                for s in all_stocks.index
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            def is_zt(stock, d):
                try:
                    bars = history_bars(
                        stock, 1, "1d", ["close", "limit_up"], end_date=d
                    )
                    if bars and len(bars) > 0:
                        return bars[0]["close"] >= bars[0]["limit_up"] * 0.99
                except:
                    return False

            zt_today = [s for s in stocks_today[:300] if is_zt(s, date)]
            zt_prev1 = [s for s in stocks_today[:300] if is_zt(s, prev1)]
            zt_prev2 = [s for s in stocks_today[:300] if is_zt(s, prev2)]

            second_board = list(set(zt_today) & set(zt_prev1) - set(zt_prev2))

            if len(second_board) == 0:
                continue

            results["signals"] += len(second_board)

            valid_stocks = []
            for s in second_board[:5]:
                try:
                    # 换手率检查（RiceQuant可能需要其他方式）
                    # 缩量检查
                    vol1 = history_bars(s, 1, "1d", ["volume"], end_date=date)
                    vol2 = history_bars(s, 1, "1d", ["volume"], end_date=prev1)

                    if vol1 and vol2 and len(vol1) > 0 and len(vol2) > 0:
                        vol_ratio = vol1[0]["volume"] / vol2[0]["volume"]
                        if vol_ratio <= 1.875:
                            # 市值获取
                            try:
                                cap_data = get_fundamentals(
                                    query(fundamentals.eod_market_cap).filter(
                                        fundamentals.stockcode == s
                                    ),
                                    date,
                                )
                                if cap_data:
                                    valid_stocks.append(
                                        (s, cap_data["eod_market_cap"].iloc[0])
                                    )
                            except:
                                valid_stocks.append((s, 0))
                except:
                    continue

            if len(valid_stocks) == 0:
                continue

            valid_stocks.sort(key=lambda x: x[1])
            target = valid_stocks[0][0]

            try:
                next_bars = history_bars(
                    target,
                    1,
                    "1d",
                    ["open", "high", "close", "limit_up"],
                    end_date=next_date,
                )
                if not next_bars or len(next_bars) == 0:
                    continue

                open_p = next_bars[0]["open"]
                high_p = next_bars[0]["high"]
                close_p = next_bars[0]["close"]
                limit_p = next_bars[0]["limit_up"]

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

                if i % 50 == 0:
                    print(f"已处理 {i}/{len(dates)} 天, 累计交易: {results['trades']}")

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
print("=" * 80)
