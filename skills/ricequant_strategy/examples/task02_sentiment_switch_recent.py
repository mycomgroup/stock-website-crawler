"""
任务02补充：情绪开关最近日期实测（2024H2-2025）
测试涨停家数硬开关在最近时期的表现
"""

print("=" * 80)
print("任务02补充：情绪开关最近日期实测（RiceQuant版）")
print("测试期间：2024-07-01 至 2025-03-28")
print("=" * 80)

import numpy as np
from datetime import datetime


def get_zt_count(date):
    """获取涨停家数"""
    all_stocks = get_all_securities(["stock"])
    stocks = [
        s
        for s in all_stocks.index
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    zt_count = 0
    sample_size = min(len(stocks), 400)  # 采样限制

    for stock in stocks[:sample_size]:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=date)
            if bars is not None and len(bars) > 0:
                if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                    zt_count += 1
        except:
            pass

    return zt_count, sample_size


def get_first_board_low_open(prev_date, curr_date):
    """首板低开选股（假弱高开版本）"""
    all_stocks = get_all_securities(["stock"])
    stocks = [
        s
        for s in all_stocks.index
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    zt_prev = []
    for stock in stocks[:300]:
        try:
            bars = history_bars(
                stock, 1, "1d", ["close", "limit_up"], end_date=prev_date
            )
            if bars and len(bars) > 0:
                if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                    zt_prev.append(stock)
        except:
            pass

    if len(zt_prev) == 0:
        return []

    selected = []
    for stock in zt_prev[:30]:
        try:
            prev_bars = history_bars(stock, 1, "1d", ["close"], end_date=prev_date)
            curr_bars = history_bars(
                stock, 1, "1d", ["open", "limit_up"], end_date=curr_date
            )

            if (
                not prev_bars
                or not curr_bars
                or len(prev_bars) == 0
                or len(curr_bars) == 0
            ):
                continue

            prev_close = prev_bars[0]["close"]
            curr_open = curr_bars[0]["open"]
            limit_up = curr_bars[0]["limit_up"]

            open_pct = (curr_open / prev_close - 1) * 100

            if 0.5 <= open_pct <= 1.5 and curr_open < limit_up * 0.99:
                selected.append(
                    {"code": stock, "open_pct": open_pct, "open_price": curr_open}
                )
        except:
            pass

    return selected


def backtest_sentiment_switch(start_date, end_date, zt_threshold=30, use_switch=True):
    """回测情绪开关"""
    print(f"\n回测期间: {start_date} 至 {end_date}")
    print(f"情绪阈值: {zt_threshold}, 使用开关: {use_switch}")

    dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(dates)}")

    results = {
        "total_days": len(dates),
        "trade_days": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "zt_counts": [],
        "skipped_by_switch": 0,
    }

    for i in range(1, len(dates)):
        prev_date = dates[i - 1]
        curr_date = dates[i]

        try:
            zt_count, sample_size = get_zt_count(prev_date)
            zt_adjusted = int(zt_count * (4000 / sample_size))  # 调整为全市场估计
            results["zt_counts"].append(zt_adjusted)

            if use_switch and zt_adjusted < zt_threshold:
                results["skipped_by_switch"] += 1
                continue

            selected = get_first_board_low_open(prev_date, curr_date)

            if len(selected) == 0:
                continue

            results["trade_days"] += 1

            next_date = dates[i + 1] if i + 1 < len(dates) else curr_date

            for stock_info in selected[:3]:
                try:
                    next_bars = history_bars(
                        stock_info["code"],
                        1,
                        "1d",
                        ["open", "high", "close"],
                        end_date=next_date,
                    )

                    if not next_bars or len(next_bars) == 0:
                        continue

                    buy_price = stock_info["open_price"] * 1.005
                    sell_price = next_bars[0]["close"]
                    max_price = next_bars[0]["high"]

                    profit = (sell_price / buy_price - 1) * 100
                    max_profit = (max_price / buy_price - 1) * 100

                    results["trades"] += 1
                    results["profits"].append(profit)

                    if profit > 0:
                        results["wins"] += 1

                except:
                    pass

            if i % 10 == 0:
                print(
                    f"已处理 {i}/{len(dates)} 天, ZT={zt_adjusted}, 累计交易={results['trades']}"
                )

        except Exception as e:
            pass

    if results["trades"] > 0:
        results["win_rate"] = results["wins"] / results["trades"] * 100
        results["avg_profit"] = np.mean(results["profits"])
        results["total_profit"] = np.sum(results["profits"])

        wins = [p for p in results["profits"] if p > 0]
        losses = [p for p in results["profits"] if p <= 0]
        results["avg_win"] = np.mean(wins) if wins else 0
        results["avg_loss"] = np.mean(losses) if losses else 0
        results["pl_ratio"] = (
            abs(results["avg_win"] / results["avg_loss"])
            if results["avg_loss"] != 0
            else 0
        )

        cum = np.cumsum(results["profits"])
        peak = np.maximum.accumulate(cum)
        dd = peak - cum
        results["max_dd"] = np.max(dd) if len(dd) > 0 else 0

        if len(results["zt_counts"]) > 0:
            results["avg_zt"] = np.mean(results["zt_counts"])
            results["min_zt"] = np.min(results["zt_counts"])
            results["max_zt"] = np.max(results["zt_counts"])

    return results


print("\n" + "=" * 80)
print("测试1: 无情绪开关（基准）")
print("=" * 80)
result_no_switch = backtest_sentiment_switch(
    "2024-07-01", "2025-03-28", zt_threshold=0, use_switch=False
)

print("\n" + "=" * 80)
print("测试2: 情绪硬开关（阈值=30）")
print("=" * 80)
result_switch_30 = backtest_sentiment_switch(
    "2024-07-01", "2025-03-28", zt_threshold=30, use_switch=True
)

print("\n" + "=" * 80)
print("测试3: 情绪硬开关（阈值=50）")
print("=" * 80)
result_switch_50 = backtest_sentiment_switch(
    "2024-07-01", "2025-03-28", zt_threshold=50, use_switch=True
)

print("\n" + "=" * 80)
print("对照表汇总")
print("=" * 80)
print(
    f"{'方案':<20} {'交易次数':<10} {'胜率':<10} {'平均收益':<12} {'累计收益':<12} {'最大回撤':<10} {'盈亏比':<10}"
)
print("-" * 80)


def print_result(name, r):
    if r["trades"] > 0:
        print(
            f"{name:<20} {r['trades']:<10} {r['win_rate']:<10.1f}% {r['avg_profit']:<12.2f}% {r['total_profit']:<12.1f}% {r['max_dd']:<10.1f}% {r['pl_ratio']:<10.2f}"
        )
    else:
        print(f"{name:<20} 未完成")


print_result("无开关（基准）", result_no_switch)
print_result("硬开关(阈值=30)", result_switch_30)
print_result("硬开关(阈值=50)", result_switch_50)

print("\n" + "=" * 80)
print("情绪统计")
print("=" * 80)
if result_no_switch.get("zt_counts"):
    print(f"平均涨停家数: {result_no_switch['avg_zt']:.1f}")
    print(f"最低涨停家数: {result_no_switch['min_zt']}")
    print(f"最高涨停家数: {result_no_switch['max_zt']}")
    print(
        f"阈值30过滤天数: {result_switch_30['skipped_by_switch']}/{result_no_switch['total_days']}"
    )
    print(
        f"阈值50过滤天数: {result_switch_50['skipped_by_switch']}/{result_no_switch['total_days']}"
    )

print("\n" + "=" * 80)
print("结论")
print("=" * 80)

if result_no_switch["trades"] > 0 and result_switch_30["trades"] > 0:
    improvement_30 = result_switch_30["win_rate"] - result_no_switch["win_rate"]
    dd_improvement_30 = result_no_switch["max_dd"] - result_switch_30["max_dd"]

    print(f"阈值30改善:")
    print(f"  胜率变化: {improvement_30:+.1f}%")
    print(f"  回撤变化: {dd_improvement_30:+.1f}%")

    if result_switch_50["trades"] > 0:
        improvement_50 = result_switch_50["win_rate"] - result_no_switch["win_rate"]
        dd_improvement_50 = result_no_switch["max_dd"] - result_switch_50["max_dd"]

        print(f"\n阈值50改善:")
        print(f"  胜率变化: {improvement_50:+.1f}%")
        print(f"  回撤变化: {dd_improvement_50:+.1f}%")
        print(
            f"  信号减少: {(result_no_switch['trades'] - result_switch_50['trades']) / result_no_switch['trades'] * 100:.1f}%"
        )

print("\n最终建议: 涨停家数 >= 30 作为硬开关阈值")
print("=" * 80)
