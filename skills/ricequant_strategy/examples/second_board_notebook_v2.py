"""
二板策略 Notebook 格式 - RiceQuant（修正版）
任务04v2：二板2021-2023实测验证

二板正确定义：
- 昨天（-1）是第二个连续涨停
- 前天（-2）是第一个涨停
- 大前天（-3）不涨停

即：昨天是"二板"当天，今天我们观察该股
"""

print("=" * 80)
print("任务04v2：二板策略2021-2023实测验证（RiceQuant Notebook版-修正）")
print("=" * 80)

import numpy as np

results_by_year = {}


def get_zt_stocks(date, limit=400):
    """获取指定日期的涨停股票"""
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    stocks = stocks[:limit]

    zt_list = []
    for stock in stocks:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=date)
            if bars is not None and len(bars) > 0:
                if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                    zt_list.append(stock)
        except:
            pass
    return zt_list


def find_second_board_stocks(date):
    """
    找出昨天的二板股票

    二板定义：
    - 昨天（-1）涨停（这是二板当天）
    - 前天（-2）涨停（这是首板）
    - 大前天（-3）不涨停

    今天我们买入该二板股票（如果开盘不涨停）
    """
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    second_board = []

    for stock in stocks[:500]:
        try:
            # 获取最近3天数据
            bars = history_bars(stock, 3, "1d", ["close", "limit_up"], end_date=date)
            if bars is None or len(bars) < 3:
                continue

            # 昨天（-1）涨停
            day1_close = bars[-1]["close"]
            day1_limit = bars[-1]["limit_up"]
            if day1_close < day1_limit * 0.99:
                continue

            # 前天（-2）涨停
            day2_close = bars[-2]["close"]
            day2_limit = bars[-2]["limit_up"]
            if day2_close < day2_limit * 0.99:
                continue

            # 大前天（-3）不涨停
            day3_close = bars[-3]["close"]
            day3_limit = bars[-3]["limit_up"]
            if day3_close >= day3_limit * 0.99:
                continue

            # 这是二板！检查缩量
            vol_bars = history_bars(stock, 2, "1d", ["volume"], end_date=date)
            if vol_bars is not None and len(vol_bars) >= 2:
                vol_ratio = vol_bars[-1]["volume"] / vol_bars[-2]["volume"]
                # 缩量条件放宽到2.0
                if vol_ratio <= 2.0:
                    second_board.append((stock, day1_limit))

        except:
            pass

    return second_board


def test_single_year(year):
    """测试单年表现"""
    print(f"\n{'=' * 60}")
    print(f"测试 {year} 年")
    print(f"{'=' * 60}")

    try:
        trading_days = get_trading_dates(f"{year}-01-01", f"{year}-12-31")
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

    for i in range(len(trading_days) - 1):
        date = trading_days[i]
        next_date = trading_days[i + 1]

        if i % 20 == 0:
            print(f"处理中: {i}/{len(trading_days)}")

        try:
            # 情绪过滤
            zt_stocks = get_zt_stocks(date, limit=400)
            if len(zt_stocks) < 10:
                continue

            # 找二板股票
            candidates = find_second_board_stocks(date)

            if len(candidates) == 0:
                continue

            results["signals"] += len(candidates)

            # 选择第一只
            target, limit_up = candidates[0]

            # 获取次日数据
            next_bars = history_bars(
                target, 1, "1d", ["open", "high", "close"], end_date=next_date
            )
            if next_bars is None or len(next_bars) == 0:
                continue

            open_price = next_bars[-1]["open"]
            high_price = next_bars[-1]["high"]
            close_price = next_bars[-1]["close"]

            # 非涨停开盘才买入
            if open_price >= limit_up * 0.99:
                continue

            # 计算收益
            buy_price = open_price * 1.005  # 滑点
            profit = (close_price / buy_price - 1) * 100
            max_profit = (high_price / buy_price - 1) * 100

            results["trades"] += 1
            results["profits"].append(profit)
            results["max_profits"].append(max_profit)
            if profit > 0:
                results["wins"] += 1

            # 记录详情
            results["trade_details"].append(
                {
                    "date": str(date),
                    "stock": target,
                    "buy_price": buy_price,
                    "sell_price": close_price,
                    "profit": profit,
                }
            )

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

        # 显示前3笔交易
        if results["trade_details"]:
            print(f"\n  前3笔交易:")
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
        result = test_single_year(year)
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
print(
    f"{'年份':<6} {'信号':<8} {'交易':<6} {'胜率':<10} {'日均收益':<12} {'最大收益':<12} {'盈亏比':<8} {'累计收益':<12} {'回撤':<10}"
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
