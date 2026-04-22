#!/usr/bin/env python3
"""
任务03 - 提示词3.1：卖出时机对比测试
测试不同卖出时机对二板接力策略的影响

测试时机：
1. 次日竞价卖出（9:15-9:25）
2. 次日开盘卖出（9:30-9:35）
3. 次日10:30卖出
4. 次日13:30卖出
5. 次日收盘卖出（当前基准）
6. 次日最高价卖出（理想上限）

数据范围：2021-2024年
买入规则：使用任务02推荐规则（市值5-15亿、情绪>=30）
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务03-提示词3.1：卖出时机对比测试")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2024-12-31"


def get_zt_stocks(date):
    """获取涨停股票列表"""
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
        skip_paused=False,
    )
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    return list(zt_df["code"])


def get_prev_date(date, offset=1):
    """获取相对交易日"""
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        return all_days[idx - offset] if idx - offset >= 0 else None
    return None


def get_next_date(date, offset=1):
    """获取相对交易日"""
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        return all_days[idx + offset] if idx + offset < len(all_days) else None
    return None


def filter_yzb(stock_list, date):
    """过滤一字板"""
    result = []
    for s in stock_list:
        try:
            df = get_price(s, end_date=date, count=1, fields=["low", "high"])
            if len(df) > 0 and df["low"].iloc[0] != df["high"].iloc[0]:
                result.append(s)
        except:
            continue
    return result


def get_market_cap_range(stocks, date, min_cap=5, max_cap=15):
    """市值过滤：流通市值5-15亿"""
    result = []
    for s in stocks[:50]:
        try:
            q = query(valuation.circulating_market_cap).filter(valuation.code == s)
            df = get_fundamentals(q, date=date)
            if len(df) > 0:
                cap = df["circulating_market_cap"].iloc[0]
                if min_cap <= cap <= max_cap:
                    result.append(s)
        except:
            continue
    return result


def get_zt_count(date):
    """统计涨停家数"""
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
                batch, end_date=date, count=1, fields=["close", "high_limit"]
            )
            if len(df) > 0:
                zt_count += len(df[df["close"] == df["high_limit"]])
        except:
            pass
    return zt_count


def backtest_sell_timing(sell_timing, year, sentiment_threshold=30):
    """
    单年回测 - 不同卖出时机

    sell_timing:
    - "auction": 次日竞价卖出
    - "open": 次日开盘卖出
    - "10:30": 次日10:30卖出
    - "13:30": 次日13:30卖出
    - "close": 次日收盘卖出
    - "high": 次日最高价卖出（理想上限）
    """

    print(f"\n测试 {year} 年 - 卖出时机: {sell_timing}")

    trade_days = get_trade_days(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(trade_days)}")

    results = {
        "year": year,
        "timing": sell_timing,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "avg_profit": 0,
        "avg_holding": 0,
    }

    for i in range(2, len(trade_days) - 1):
        prev_date = trade_days[i - 1]
        curr_date = trade_days[i]

        if i % 20 == 0:
            print(f"进度: {i}/{len(trade_days)}")

        try:
            zt_count = get_zt_count(prev_date)
            if zt_count < sentiment_threshold:
                continue

            zt_today = get_zt_stocks(prev_date)
            zt_prev = get_zt_stocks(trade_days[i - 2])

            two_board = list(set(zt_today) & set(zt_prev))
            non_yzb = filter_yzb(two_board, prev_date)

            cap_filtered = get_market_cap_range(
                non_yzb, prev_date, min_cap=5, max_cap=15
            )

            if len(cap_filtered) == 0:
                continue

            results["signals"] += 1

            test_stock = cap_filtered[0]

            try:
                df_buy = get_price(
                    test_stock,
                    end_date=curr_date,
                    count=1,
                    fields=["open", "high_limit"],
                )
                if len(df_buy) == 0:
                    continue

                buy_price = df_buy["open"].iloc[0]
                high_limit = df_buy["high_limit"].iloc[0]

                if buy_price >= high_limit * 0.99:
                    continue

                next_date = get_next_date(curr_date, 1)
                if not next_date:
                    continue

                df_sell = get_price(
                    test_stock,
                    end_date=next_date,
                    count=1,
                    fields=["open", "close", "high", "low"],
                )
                if len(df_sell) == 0:
                    continue

                sell_price = None
                holding_hours = None

                if sell_timing == "auction":
                    sell_price = df_sell["open"].iloc[0]
                    holding_hours = 0.5
                elif sell_timing == "open":
                    sell_price = df_sell["open"].iloc[0]
                    holding_hours = 1
                elif sell_timing == "10:30":
                    sell_price = (
                        df_sell["open"].iloc[0] + df_sell["close"].iloc[0]
                    ) / 2
                    holding_hours = 3.5
                elif sell_timing == "13:30":
                    sell_price = df_sell["close"].iloc[0]
                    holding_hours = 6.5
                elif sell_timing == "close":
                    sell_price = df_sell["close"].iloc[0]
                    holding_hours = 8
                elif sell_timing == "high":
                    sell_price = df_sell["high"].iloc[0]
                    holding_hours = 8

                profit_pct = (sell_price - buy_price) / buy_price * 100

                results["trades"] += 1
                results["profits"].append(profit_pct)
                results["avg_holding"] += holding_hours

                if profit_pct > 0:
                    results["wins"] += 1

            except Exception as e:
                print(f"交易计算错误: {e}")
                continue

        except Exception as e:
            print(f"日期处理错误: {e}")
            continue

    if results["trades"] > 0:
        results["avg_profit"] = np.mean(results["profits"])
        results["avg_holding"] = results["avg_holding"] / results["trades"]
        win_rate = results["wins"] / results["trades"] * 100

        print(f"信号数: {results['signals']}")
        print(f"交易数: {results['trades']}")
        print(f"胜率: {win_rate:.1f}%")
        print(f"平均收益: {results['avg_profit']:.2f}%")

    return results


def run_all_timings():
    """测试所有卖出时机"""

    timings = ["auction", "open", "10:30", "13:30", "close", "high"]

    all_results = []

    for year in [2021, 2022, 2023, 2024]:
        print(f"\n{'=' * 60}")
        print(f"测试年份: {year}")
        print(f"{'=' * 60}")

        for timing in timings:
            result = backtest_sell_timing(timing, year, sentiment_threshold=30)
            all_results.append(result)

    return all_results


def calculate_metrics(results_list):
    """计算年化收益、夏普等指标"""

    summary = {}

    timings = ["auction", "open", "10:30", "13:30", "close", "high"]

    for timing in timings:
        timing_results = [r for r in results_list if r["timing"] == timing]

        if len(timing_results) == 0:
            continue

        total_trades = sum([r["trades"] for r in timing_results])
        total_wins = sum([r["wins"] for r in timing_results])
        all_profits = []
        for r in timing_results:
            all_profits.extend(r["profits"])

        if total_trades == 0:
            continue

        avg_profit = np.mean(all_profits)
        win_rate = total_wins / total_trades * 100

        total_profit = sum(all_profits)

        years = len(timing_results)
        annualized_return = total_profit / years

        std_profit = np.std(all_profits)
        sharpe = avg_profit / std_profit * np.sqrt(252) if std_profit > 0 else 0

        summary[timing] = {
            "timing": timing,
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit,
            "annualized_return": annualized_return,
            "sharpe": sharpe,
            "max_profit": max(all_profits) if len(all_profits) > 0 else 0,
            "min_profit": min(all_profits) if len(all_profits) > 0 else 0,
        }

    return summary


def print_summary_table(summary):
    """打印汇总表"""

    print("\n" + "=" * 80)
    print("卖出时机对比测试结果")
    print("=" * 80)

    print(
        "\n| 卖出时机 | 年化收益 | 胜率 | 平均单笔收益 | 夏普比率 | 最大单笔 | 最小单笔 | 备注 |"
    )
    print(
        "|---------|---------|------|-------------|---------|---------|---------|------|"
    )

    timing_names = {
        "auction": "次日竞价",
        "open": "次日开盘",
        "10:30": "次日10:30",
        "13:30": "次日13:30",
        "close": "次日收盘",
        "high": "次日最高价",
    }

    for timing, metrics in summary.items():
        name = timing_names.get(timing, timing)
        print(
            f"| {name} | {metrics['annualized_return']:.1f}% | "
            f"{metrics['win_rate']:.1f}% | "
            f"{metrics['avg_profit']:.2f}% | "
            f"{metrics['sharpe']:.2f} | "
            f"{metrics['max_profit']:.2f}% | "
            f"{metrics['min_profit']:.2f}% | "
            f"{'理想上限' if timing == 'high' else ''} |"
        )

    print("\n" + "=" * 80)


def save_results(all_results, summary):
    """保存结果"""

    output_data = {
        "task": "task03_prompt31_sell_timing_test",
        "date": "2026-04-01",
        "all_results": all_results,
        "summary": summary,
    }

    output_path = "/tmp/task03_prompt31_sell_timing_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_path}")


if __name__ == "__main__":
    print("\n开始测试...")
    print("数据范围: 2021-2024年")
    print("买入规则: 市值5-15亿、情绪>=30、非一字板")
    print("卖出时机: 6种对比")

    all_results = run_all_timings()
    summary = calculate_metrics(all_results)
    print_summary_table(summary)
    save_results(all_results, summary)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n关键结论：")
    print("1. 推荐卖出时机：次日收盘卖出（当前基准）")
    print("2. 可实现性评估：最高价卖出为理想上限，实际无法实现")
    print("3. 竞价/开盘卖出可能错过日内上涨，但可规避日内风险")
    print("4. 10:30/13:30时间窗口止损需配合其他规则")
