"""
二板策略2021-2023实测验证 - RiceQuant Notebook（最终正确版）
使用正确的Timestamp索引和API
"""

print("=" * 80)
print("任务04v2：二板策略2021-2023实测验证（RiceQuant Notebook版-最终修正）")
print("=" * 80)

import pandas as pd
import numpy as np

results_by_year = {}


def test_year(year):
    """测试单年表现"""
    print(f"\n{'=' * 60}")
    print(f"测试 {year} 年")
    print(f"{'=' * 60}")

    year_start = f"{year}-01-01"
    year_end = f"{year}-12-31"

    try:
        trading_days = get_trading_dates(year_start, year_end)
        dates_ts = [pd.Timestamp(str(d)[:10]) for d in trading_days]
    except:
        print(f"无法获取{year}年交易日")
        return None

    print(f"交易日数: {len(trading_days)}")

    results = {
        "year": year,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "max_profits": [],
        "trade_details": [],
    }

    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    print(f"股票池: {len(stocks)}只，每日检查前500只")

    for i in range(len(dates_ts) - 1):
        test_date = dates_ts[i]
        next_date = dates_ts[i + 1]

        if i % 20 == 0:
            print(f"处理中: {i}/{len(dates_ts)}")

        try:
            # 获取当日涨停股票
            prices_today = get_price(
                stocks[:500],
                start_date=str(test_date)[:10],
                end_date=str(test_date)[:10],
                frequency="1d",
                fields=["close", "limit_up"],
            )

            if prices_today is None or prices_today.empty:
                continue

            # 找涨停股票
            zt_stocks = []

            for stock in stocks[:500]:
                try:
                    key = (stock, test_date)

                    if key in prices_today.index:
                        close = float(prices_today.loc[key, "close"])
                        limit_up = float(prices_today.loc[key, "limit_up"])

                        if pd.notna(close) and pd.notna(limit_up) and limit_up > 0:
                            if close >= limit_up * 0.99:
                                zt_stocks.append(stock)
                except:
                    pass

            if len(zt_stocks) == 0:
                continue

            results["signals"] += len(zt_stocks)

            # 找二板（需要最近3天数据）
            if i >= 2:
                prev_date = dates_ts[i - 1]
                prev2_date = dates_ts[i - 2]

                prices_3d = get_price(
                    zt_stocks[:20],
                    start_date=str(prev2_date)[:10],
                    end_date=str(test_date)[:10],
                    frequency="1d",
                    fields=["close", "limit_up", "open", "high"],
                )

                if prices_3d is None or prices_3d.empty:
                    continue

                for stock in zt_stocks[:20]:
                    try:
                        # 今天涨停
                        key_today = (stock, test_date)
                        if key_today not in prices_3d.index:
                            continue

                        today_close = float(prices_3d.loc[key_today, "close"])
                        today_limit = float(prices_3d.loc[key_today, "limit_up"])

                        # 昨天涨停
                        key_prev = (stock, prev_date)
                        if key_prev not in prices_3d.index:
                            continue

                        yesterday_close = float(prices_3d.loc[key_prev, "close"])
                        yesterday_limit = float(prices_3d.loc[key_prev, "limit_up"])

                        # 前天不涨停
                        key_prev2 = (stock, prev2_date)
                        if key_prev2 not in prices_3d.index:
                            continue

                        prev2_close = float(prices_3d.loc[key_prev2, "close"])
                        prev2_limit = float(prices_3d.loc[key_prev2, "limit_up"])

                        # 判断二板
                        if today_close >= today_limit * 0.99:
                            if yesterday_close >= yesterday_limit * 0.99:
                                if prev2_close < prev2_limit * 0.99:
                                    # 这是二板！检查次日开盘
                                    next_key = (stock, next_date)
                                    if next_key not in prices_3d.index:
                                        continue

                                    # 需要重新获取次日数据
                                    next_prices = get_price(
                                        stock,
                                        start_date=str(next_date)[:10],
                                        end_date=str(next_date)[:10],
                                        frequency="1d",
                                        fields=["open", "close", "high"],
                                    )

                                    if next_prices is None or next_prices.empty:
                                        continue

                                    next_key = (stock, next_date)
                                    if next_key not in next_prices.index:
                                        continue

                                    open_price = float(
                                        next_prices.loc[next_key, "open"]
                                    )
                                    close_price = float(
                                        next_prices.loc[next_key, "close"]
                                    )
                                    high_price = float(
                                        next_prices.loc[next_key, "high"]
                                    )

                                    # 非涨停开盘才买入
                                    if open_price >= today_limit * 0.99:
                                        continue

                                    # 计算收益（用涨停价买入）
                                    buy_price = today_limit * 1.005
                                    profit = (close_price / buy_price - 1) * 100
                                    max_profit = (high_price / buy_price - 1) * 100

                                    results["trades"] += 1
                                    results["profits"].append(profit)
                                    results["max_profits"].append(max_profit)

                                    if profit > 0:
                                        results["wins"] += 1

                                    results["trade_details"].append(
                                        {
                                            "date": str(test_date)[:10],
                                            "stock": stock,
                                            "buy_price": buy_price,
                                            "sell_price": close_price,
                                            "profit": profit,
                                        }
                                    )

                    except:
                        pass

        except Exception as e:
            continue

    # 统计
    if results["trades"] > 0:
        results["win_rate"] = results["wins"] / results["trades"] * 100
        results["avg_profit"] = np.mean(results["profits"])
        results["avg_max_profit"] = np.mean(results["max_profits"])

        wins = [p for p in results["profits"] if p > 0]
        losses = [p for p in results["profits"] if p <= 0]
        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(np.abs(losses)) if losses else 1
        results["pl_ratio"] = avg_win / avg_loss if avg_loss > 0 else 0

        cum = np.cumsum(results["profits"])
        results["cumulative"] = cum[-1]
        peak = np.maximum.accumulate(cum)
        results["max_dd"] = np.max(peak - cum) if len(cum) > 0 else 0

        print(f"\n{year}年结果:")
        print(f"  二板信号: {results['signals']}")
        print(f"  交易数: {results['trades']}")
        print(f"  胜率: {results['win_rate']:.2f}%")
        print(f"  平均收益: {results['avg_profit']:.2f}%")
        print(f"  平均最大收益: {results['avg_max_profit']:.2f}%")
        print(f"  盈亏比: {results['pl_ratio']:.2f}")
        print(f"  累计收益: {results['cumulative']:.2f}%")
        print(f"  最大回撤: {results['max_dd']:.2f}%")

        if results["trade_details"]:
            print(f"\n前3笔交易:")
            for t in results["trade_details"][:3]:
                print(f"    {t['date']}: {t['stock']} 收益 {t['profit']:.2f}%")
    else:
        print(f"\n{year}年: 无交易")
        for k in [
            "win_rate",
            "avg_profit",
            "avg_max_profit",
            "pl_ratio",
            "cumulative",
            "max_dd",
        ]:
            results[k] = 0

    return results


print("\n开始逐年测试...")

for year in [2021, 2022, 2023]:
    try:
        result = test_year(year)
        if result:
            results_by_year[year] = result
    except Exception as e:
        print(f"{year}年测试失败: {e}")
        import traceback

        traceback.print_exc()

# 汇总
print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)

total_signals = sum(r.get("signals", 0) for r in results_by_year.values())
total_trades = sum(r.get("trades", 0) for r in results_by_year.values())

print(f"总信号数: {total_signals}")
print(f"总交易数: {total_trades}")

print(
    f"\n{'年份':<6} {'信号':<8} {'交易':<6} {'胜率':<10} {'日均收益':<12} {'最大收益':<12} {'盈亏比':<8} {'累计收益':<12} {'回撤':<10}"
)
print("-" * 90)

for year in [2021, 2022, 2023]:
    r = results_by_year.get(year)
    if r and r.get("trades", 0) > 0:
        print(
            f"{year:<6} {r['signals']:<8} {r['trades']:<6} {r['win_rate']:<10.2f}% {r['avg_profit']:<12.2f}% {r['avg_max_profit']:<12.2f}% {r['pl_ratio']:<8.2f} {r['cumulative']:<12.2f}% {r['max_dd']:<10.2f}%"
        )
    else:
        print(f"{year:<6} {'-':<8} {'0':<6} {'未完成':<10}")

# 判定
print("\n" + "=" * 80)
print("稳定性判定")
print("=" * 80)

win_rates = [r["win_rate"] for r in results_by_year.values() if r.get("trades", 0) > 0]
cumulative = [r["cumulative"] for r in results_by_year.values()]

positive_years = len([c for c in cumulative if c > 0])
win_diff = max(win_rates) - min(win_rates) if len(win_rates) >= 2 else 100

print(f"正收益年份: {positive_years}/3 (需≥2)")
print(f"胜率差异: {win_diff:.2f}% (需<15%)")

if positive_years >= 2 and win_diff < 15:
    print("\n判定: 稳定 ✓")
    decision = "Go"
elif positive_years >= 1 or (len(win_rates) > 0 and win_diff < 20):
    print("\n判定: 需观察 ⚠️")
    decision = "Watch"
else:
    print("\n判定: 不稳定 ✗")
    decision = "No-Go"

print(f"\n最终决策: {decision}")
print("=" * 80)
