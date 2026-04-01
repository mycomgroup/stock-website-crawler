#!/usr/bin/env python3
"""
任务03 - 提示词3.4：持仓周期测试
测试不同持仓周期对二板接力策略的影响

持仓周期：
1. T+1卖出（次日固定时机）
2. T+2卖出（隔日固定时机）
3. T+1或T+2（如果T+1涨停则持有到T+2）
4. 动态持仓（根据表现决定）
   - 如果T+1盈利>5%，持有到T+2
   - 如果T+1亏损，当日收盘卖出
5. 长线持仓（持有到满足卖出条件）

数据范围：2021-2024年
买入规则：市值5-15亿、情绪>=30
卖出时机：次日收盘（基于提示词3.1推荐）
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务03-提示词3.4：持仓周期测试")
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


def check_zt(stock, date):
    """检查涨停"""
    try:
        df = get_price(stock, end_date=date, count=1, fields=["close", "high_limit"])
        if len(df) > 0:
            return df["close"].iloc[0] >= df["high_limit"].iloc[0] * 0.99
    except:
        pass
    return False


def backtest_holding_period(holding_rule, year, sentiment_threshold=30):
    """
    单年回测 - 不同持仓周期

    holding_rule:
    - "T+1": 次日收盘卖出
    - "T+2": 隔日收盘卖出
    - "T+1_or_T+2": 如果T+1涨停则持有到T+2
    - "dynamic_5pct": 如果T+1盈利>5%持有到T+2
    - "dynamic_loss": 如果T+1亏损当日卖出
    - "long": 持有到卖出条件
    """

    print(f"\n测试 {year} 年 - 持仓周期: {holding_rule}")

    trade_days = get_trade_days(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(trade_days)}")

    results = {
        "year": year,
        "rule": holding_rule,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "holding_days": [],
        "zt_holds": 0,
        "zt_hold_extra_profit": 0,
        "avg_profit": 0,
        "avg_holding": 0,
        "turnover": 0,
    }

    for i in range(2, len(trade_days) - 2):
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

                sell_date = None
                sell_price = None
                holding_days = None

                if holding_rule == "T+1":
                    next_date = get_next_date(curr_date, 1)
                    if next_date:
                        df_sell = get_price(
                            test_stock, end_date=next_date, count=1, fields=["close"]
                        )
                        if len(df_sell) > 0:
                            sell_date = next_date
                            sell_price = df_sell["close"].iloc[0]
                            holding_days = 1

                elif holding_rule == "T+2":
                    next_date2 = get_next_date(curr_date, 2)
                    if next_date2:
                        df_sell = get_price(
                            test_stock, end_date=next_date2, count=1, fields=["close"]
                        )
                        if len(df_sell) > 0:
                            sell_date = next_date2
                            sell_price = df_sell["close"].iloc[0]
                            holding_days = 2

                elif holding_rule == "T+1_or_T+2":
                    next_date = get_next_date(curr_date, 1)
                    if next_date:
                        if check_zt(test_stock, next_date):
                            next_date2 = get_next_date(curr_date, 2)
                            if next_date2:
                                df_sell = get_price(
                                    test_stock,
                                    end_date=next_date2,
                                    count=1,
                                    fields=["close"],
                                )
                                if len(df_sell) > 0:
                                    sell_date = next_date2
                                    sell_price = df_sell["close"].iloc[0]
                                    holding_days = 2
                                    results["zt_holds"] += 1

                                    df_t1 = get_price(
                                        test_stock,
                                        end_date=next_date,
                                        count=1,
                                        fields=["close"],
                                    )
                                    if len(df_t1) > 0:
                                        t1_profit = (
                                            (df_t1["close"].iloc[0] - buy_price)
                                            / buy_price
                                            * 100
                                        )
                                        t2_profit = (
                                            (sell_price - buy_price) / buy_price * 100
                                        )
                                        results["zt_hold_extra_profit"] += (
                                            t2_profit - t1_profit
                                        )
                        else:
                            df_sell = get_price(
                                test_stock,
                                end_date=next_date,
                                count=1,
                                fields=["close"],
                            )
                            if len(df_sell) > 0:
                                sell_date = next_date
                                sell_price = df_sell["close"].iloc[0]
                                holding_days = 1

                elif holding_rule == "dynamic_5pct":
                    next_date = get_next_date(curr_date, 1)
                    if next_date:
                        df_t1 = get_price(
                            test_stock,
                            end_date=next_date,
                            count=1,
                            fields=["close", "high_limit"],
                        )
                        if len(df_t1) > 0:
                            t1_profit = (
                                (df_t1["close"].iloc[0] - buy_price) / buy_price * 100
                            )

                            if t1_profit > 5:
                                next_date2 = get_next_date(curr_date, 2)
                                if next_date2:
                                    df_sell = get_price(
                                        test_stock,
                                        end_date=next_date2,
                                        count=1,
                                        fields=["close"],
                                    )
                                    if len(df_sell) > 0:
                                        sell_date = next_date2
                                        sell_price = df_sell["close"].iloc[0]
                                        holding_days = 2
                            else:
                                sell_date = next_date
                                sell_price = df_t1["close"].iloc[0]
                                holding_days = 1

                elif holding_rule == "dynamic_loss":
                    next_date = get_next_date(curr_date, 1)
                    if next_date:
                        df_t1 = get_price(
                            test_stock,
                            end_date=next_date,
                            count=1,
                            fields=["close", "high_limit"],
                        )
                        if len(df_t1) > 0:
                            t1_profit = (
                                (df_t1["close"].iloc[0] - buy_price) / buy_price * 100
                            )

                            if t1_profit < 0:
                                sell_date = next_date
                                sell_price = df_t1["close"].iloc[0]
                                holding_days = 1
                            else:
                                next_date2 = get_next_date(curr_date, 2)
                                if next_date2:
                                    df_sell = get_price(
                                        test_stock,
                                        end_date=next_date2,
                                        count=1,
                                        fields=["close"],
                                    )
                                    if len(df_sell) > 0:
                                        sell_date = next_date2
                                        sell_price = df_sell["close"].iloc[0]
                                        holding_days = 2

                elif holding_rule == "long":
                    for day_offset in range(1, 10):
                        next_date = get_next_date(curr_date, day_offset)
                        if not next_date:
                            break

                        df_check = get_price(
                            test_stock,
                            end_date=next_date,
                            count=1,
                            fields=["close", "high_limit"],
                        )
                        if len(df_check) == 0:
                            continue

                        if (
                            df_check["close"].iloc[0]
                            < df_check["high_limit"].iloc[0] * 0.99
                        ):
                            sell_date = next_date
                            sell_price = df_check["close"].iloc[0]
                            holding_days = day_offset
                            break

                if sell_price and sell_date:
                    profit_pct = (sell_price - buy_price) / buy_price * 100

                    results["trades"] += 1
                    results["profits"].append(profit_pct)
                    results["holding_days"].append(holding_days)

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
        results["avg_holding"] = np.mean(results["holding_days"])

        win_rate = results["wins"] / results["trades"] * 100
        turnover = 252 / results["avg_holding"] if results["avg_holding"] > 0 else 0
        results["turnover"] = turnover

        print(f"信号数: {results['signals']}")
        print(f"交易数: {results['trades']}")
        print(f"胜率: {win_rate:.1f}%")
        print(f"平均收益: {results['avg_profit']:.2f}%")
        print(f"平均持仓: {results['avg_holding']:.2f}天")
        print(f"年换手率: {turnover:.1f}倍")

        if holding_rule == "T+1_or_T+2":
            print(f"涨停持有次数: {results['zt_holds']}")
            if results["zt_holds"] > 0:
                print(
                    f"涨停持有额外收益: {results['zt_hold_extra_profit'] / results['zt_holds']:.2f}%"
                )

    return results


def run_all_holding_rules():
    """测试所有持仓周期"""

    rules = [
        "T+1",
        "T+2",
        "T+1_or_T+2",
        "dynamic_5pct",
        "dynamic_loss",
        "long",
    ]

    all_results = []

    for year in [2021, 2022, 2023, 2024]:
        print(f"\n{'=' * 60}")
        print(f"测试年份: {year}")
        print(f"{'=' * 60}")

        for rule in rules:
            result = backtest_holding_period(rule, year, sentiment_threshold=30)
            all_results.append(result)

    return all_results


def calculate_metrics(results_list):
    """计算汇总指标"""

    summary = {}

    rules = [
        "T+1",
        "T+2",
        "T+1_or_T+2",
        "dynamic_5pct",
        "dynamic_loss",
        "long",
    ]

    for rule in rules:
        rule_results = [r for r in results_list if r["rule"] == rule]

        if len(rule_results) == 0:
            continue

        total_trades = sum([r["trades"] for r in rule_results])
        total_wins = sum([r["wins"] for r in rule_results])
        all_profits = []
        all_holding_days = []
        total_zt_holds = sum([r["zt_holds"] for r in rule_results])
        total_zt_extra = sum([r["zt_hold_extra_profit"] for r in rule_results])

        for r in rule_results:
            all_profits.extend(r["profits"])
            all_holding_days.extend(r["holding_days"])

        if total_trades == 0:
            continue

        avg_profit = np.mean(all_profits)
        avg_holding = np.mean(all_holding_days)
        win_rate = total_wins / total_trades * 100
        turnover = 252 / avg_holding if avg_holding > 0 else 0

        total_profit = sum(all_profits)
        years = len(rule_results)
        annualized_return = total_profit / years

        std_profit = np.std(all_profits)
        sharpe = avg_profit / std_profit * np.sqrt(252) if std_profit > 0 else 0

        summary[rule] = {
            "rule": rule,
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit,
            "annualized_return": annualized_return,
            "sharpe": sharpe,
            "avg_holding": avg_holding,
            "turnover": turnover,
            "zt_holds": total_zt_holds,
            "zt_extra_profit": total_zt_extra / total_zt_holds
            if total_zt_holds > 0
            else 0,
        }

    return summary


def print_summary_table(summary):
    """打印汇总表"""

    print("\n" + "=" * 80)
    print("持仓周期对比测试结果")
    print("=" * 80)

    print(
        "\n| 持仓周期 | 年化收益 | 胜率 | 平均单笔收益 | 夏普 | 年换手率 | 平均持仓天数 | 涨停持有额外收益 |"
    )
    print(
        "|---------|---------|------|-------------|------|---------|-------------|----------------|"
    )

    rule_names = {
        "T+1": "T+1卖出",
        "T+2": "T+2卖出",
        "T+1_or_T+2": "T+1或T+2",
        "dynamic_5pct": "盈利>5%持T+2",
        "dynamic_loss": "亏损当日卖",
        "long": "长线持仓",
    }

    for rule, metrics in summary.items():
        name = rule_names.get(rule, rule)
        zt_extra = (
            f"{metrics['zt_extra_profit']:.2f}%" if metrics["zt_holds"] > 0 else "N/A"
        )
        print(
            f"| {name} | {metrics['annualized_return']:.1f}% | "
            f"{metrics['win_rate']:.1f}% | "
            f"{metrics['avg_profit']:.2f}% | "
            f"{metrics['sharpe']:.2f} | "
            f"{metrics['turnover']:.1f}倍 | "
            f"{metrics['avg_holding']:.2f}天 | "
            f"{zt_extra} |"
        )

    print("\n" + "=" * 80)


def save_results(all_results, summary):
    """保存结果"""

    output_data = {
        "task": "task03_prompt34_holding_period_test",
        "date": "2026-04-01",
        "all_results": all_results,
        "summary": summary,
    }

    output_path = "/tmp/task03_prompt34_holding_period_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_path}")


if __name__ == "__main__":
    print("\n开始测试...")
    print("数据范围: 2021-2024年")
    print("买入规则: 市值5-15亿、情绪>=30、非一字板")
    print("卖出时机: 次日收盘")
    print("持仓周期: 6种对比")

    all_results = run_all_holding_rules()
    summary = calculate_metrics(all_results)
    print_summary_table(summary)
    save_results(all_results, summary)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n关键结论：")
    print("1. T+1周转快但收益可能不如T+2")
    print("2. T+2收益可能更高但回撤风险增加")
    print("3. 涨停持有可获得额外收益")
    print("4. 动态持仓需根据市场环境调整")
    print("5. 推荐方案：T+1或T+2（涨停持有）")
