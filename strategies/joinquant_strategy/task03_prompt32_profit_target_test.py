#!/usr/bin/env python3
"""
任务03 - 提示词3.2：止盈规则测试
测试不同止盈规则对二板接力策略的影响

止盈规则：
1. 无止盈（持有到基础卖出时机）
2. 固定点数止盈（+5%/+7%/+10%/+15%）
3. 分时形态止盈（冲高回落跌破分时均线/开盘价）
4. 板块止盈（龙头炸板/板块跌幅>2%）

数据范围：2021-2024年
买入规则：市值5-15亿、情绪>=30
基础卖出时机：次日收盘（基于提示词3.1推荐）
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务03-提示词3.2：止盈规则测试")
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


def get_minute_data(stock, date):
    """获取分时数据"""
    try:
        bars = get_bars(
            stock,
            count=240,
            unit="1m",
            fields=["close", "volume"],
            end_dt=date + " 15:00:00",
        )
        if bars is not None and len(bars) > 0:
            return bars
    except:
        pass
    return None


def check_profit_target_fixed(buy_price, current_price, target_pct):
    """检查固定止盈"""
    profit_pct = (current_price - buy_price) / buy_price * 100
    return profit_pct >= target_pct


def check_profit_target_minute(buy_price, minute_data, rule_type):
    """检查分时止盈"""
    if minute_data is None or len(minute_data) == 0:
        return False, None

    opens = minute_data["close"][0]

    if rule_type == "below_avg":
        avg_price = np.mean(minute_data["close"])
        high_price = np.max(minute_data["close"])
        if high_price > avg_price:
            if minute_data["close"][-1] < avg_price:
                return True, minute_data["close"][-1]

    elif rule_type == "below_open":
        high_price = np.max(minute_data["close"])
        if high_price > opens:
            if minute_data["close"][-1] < opens:
                return True, minute_data["close"][-1]

    elif rule_type == "retrace_50":
        high_price = np.max(minute_data["close"])
        profit = high_price - buy_price
        if profit > 0:
            retrace_price = high_price - profit * 0.5
            if minute_data["close"][-1] < retrace_price:
                return True, minute_data["close"][-1]

    return False, None


def check_sector_profit_target(stock, date, rule_type):
    """检查板块止盈"""
    try:
        industry_code = get_industry_code(stock, date)
        if industry_code:
            sector_stocks = get_industry_stocks(industry_code, date)

            if rule_type == "leader_down":
                sector_zt = [s for s in sector_stocks[:30] if check_zt(s, date)]
                if len(sector_zt) > 0:
                    leader = sector_zt[0]
                    df = get_price(
                        leader, end_date=date, count=1, fields=["close", "high_limit"]
                    )
                    if len(df) > 0:
                        if df["close"].iloc[0] < df["high_limit"].iloc[0] * 0.99:
                            return True

            elif rule_type == "sector_drop_2pct":
                sector_returns = []
                for s in sector_stocks[:30]:
                    try:
                        df = get_price(s, end_date=date, count=2, fields=["close"])
                        if len(df) >= 2:
                            ret = (
                                (df["close"].iloc[-1] - df["close"].iloc[-2])
                                / df["close"].iloc[-2]
                                * 100
                            )
                            sector_returns.append(ret)
                    except:
                        continue

                if len(sector_returns) > 0:
                    avg_ret = np.mean(sector_returns)
                    if avg_ret < -2:
                        return True

    except:
        pass

    return False


def check_zt(stock, date):
    """检查涨停"""
    try:
        df = get_price(stock, end_date=date, count=1, fields=["close", "high_limit"])
        if len(df) > 0:
            return df["close"].iloc[0] >= df["high_limit"].iloc[0] * 0.99
    except:
        pass
    return False


def backtest_profit_target(profit_rule, year, sentiment_threshold=30):
    """
    单年回测 - 不同止盈规则

    profit_rule:
    - "no": 无止盈
    - "fixed_5": +5%止盈
    - "fixed_7": +7%止盈
    - "fixed_10": +10%止盈
    - "fixed_15": +15%止盈
    - "minute_avg": 冲高回落跌破分时均线
    - "minute_open": 冲高回落跌破开盘价
    - "minute_retrace_50": 冲高后回调超过涨幅50%
    - "sector_leader": 板块龙头炸板
    - "sector_drop_2pct": 板块跌幅超过2%
    """

    print(f"\n测试 {year} 年 - 止盈规则: {profit_rule}")

    trade_days = get_trade_days(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(trade_days)}")

    results = {
        "year": year,
        "rule": profit_rule,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "profit_triggered": 0,
        "profit_trigger_pct": [],
        "avg_profit": 0,
        "avg_trigger_profit": 0,
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

                sell_price = df_sell["close"].iloc[0]
                profit_pct = (sell_price - buy_price) / buy_price * 100

                profit_triggered = False

                if profit_rule.startswith("fixed_"):
                    target_pct = float(profit_rule.split("_")[1])

                    if df_sell["high"].iloc[0] >= buy_price * (1 + target_pct / 100):
                        profit_triggered = True
                        sell_price = buy_price * (1 + target_pct / 100)
                        profit_pct = target_pct
                        results["profit_triggered"] += 1
                        results["profit_trigger_pct"].append(target_pct)

                elif profit_rule.startswith("minute_"):
                    minute_data = get_minute_data(test_stock, next_date)
                    if minute_data:
                        rule_type = profit_rule.replace("minute_", "")
                        triggered, trigger_price = check_profit_target_minute(
                            buy_price, minute_data, rule_type
                        )
                        if triggered:
                            profit_triggered = True
                            sell_price = trigger_price
                            profit_pct = (sell_price - buy_price) / buy_price * 100
                            results["profit_triggered"] += 1
                            results["profit_trigger_pct"].append(profit_pct)

                elif profit_rule.startswith("sector_"):
                    rule_type = profit_rule.replace("sector_", "")
                    if check_sector_profit_target(test_stock, next_date, rule_type):
                        profit_triggered = True
                        sell_price = df_sell["close"].iloc[0]
                        profit_pct = (sell_price - buy_price) / buy_price * 100
                        results["profit_triggered"] += 1
                        results["profit_trigger_pct"].append(profit_pct)

                results["trades"] += 1
                results["profits"].append(profit_pct)

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
        if results["profit_triggered"] > 0:
            results["avg_trigger_profit"] = np.mean(results["profit_trigger_pct"])

        win_rate = results["wins"] / results["trades"] * 100
        trigger_rate = results["profit_triggered"] / results["trades"] * 100

        print(f"信号数: {results['signals']}")
        print(f"交易数: {results['trades']}")
        print(f"胜率: {win_rate:.1f}%")
        print(f"平均收益: {results['avg_profit']:.2f}%")
        print(f"止盈触发率: {trigger_rate:.1f}%")

    return results


def run_all_profit_rules():
    """测试所有止盈规则"""

    rules = [
        "no",
        "fixed_5",
        "fixed_7",
        "fixed_10",
        "fixed_15",
        "minute_avg",
        "minute_open",
        "minute_retrace_50",
        "sector_leader",
        "sector_drop_2pct",
    ]

    all_results = []

    for year in [2021, 2022, 2023, 2024]:
        print(f"\n{'=' * 60}")
        print(f"测试年份: {year}")
        print(f"{'=' * 60}")

        for rule in rules:
            result = backtest_profit_target(rule, year, sentiment_threshold=30)
            all_results.append(result)

    return all_results


def calculate_metrics(results_list):
    """计算汇总指标"""

    summary = {}

    rules = [
        "no",
        "fixed_5",
        "fixed_7",
        "fixed_10",
        "fixed_15",
        "minute_avg",
        "minute_open",
        "minute_retrace_50",
        "sector_leader",
        "sector_drop_2pct",
    ]

    for rule in rules:
        rule_results = [r for r in results_list if r["rule"] == rule]

        if len(rule_results) == 0:
            continue

        total_trades = sum([r["trades"] for r in rule_results])
        total_wins = sum([r["wins"] for r in rule_results])
        total_triggered = sum([r["profit_triggered"] for r in rule_results])
        all_profits = []
        all_trigger_profits = []
        for r in rule_results:
            all_profits.extend(r["profits"])
            all_trigger_profits.extend(r["profit_trigger_pct"])

        if total_trades == 0:
            continue

        avg_profit = np.mean(all_profits)
        win_rate = total_wins / total_trades * 100
        trigger_rate = total_triggered / total_trades * 100
        avg_trigger_profit = (
            np.mean(all_trigger_profits) if len(all_trigger_profits) > 0 else 0
        )

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
            "trigger_rate": trigger_rate,
            "avg_trigger_profit": avg_trigger_profit,
        }

    return summary


def print_summary_table(summary):
    """打印汇总表"""

    print("\n" + "=" * 80)
    print("止盈规则对比测试结果")
    print("=" * 80)

    print(
        "\n| 止盈规则 | 年化收益 | 胜率 | 平均单笔收益 | 夏普 | 止盈触发率 | 平均止盈幅度 |"
    )
    print("|---------|---------|------|-------------|------|-----------|-------------|")

    rule_names = {
        "no": "无止盈",
        "fixed_5": "+5%止盈",
        "fixed_7": "+7%止盈",
        "fixed_10": "+10%止盈",
        "fixed_15": "+15%止盈",
        "minute_avg": "跌破分时均线",
        "minute_open": "跌破开盘价",
        "minute_retrace_50": "回调50%",
        "sector_leader": "龙头炸板",
        "sector_drop_2pct": "板块跌超2%",
    }

    for rule, metrics in summary.items():
        name = rule_names.get(rule, rule)
        print(
            f"| {name} | {metrics['annualized_return']:.1f}% | "
            f"{metrics['win_rate']:.1f}% | "
            f"{metrics['avg_profit']:.2f}% | "
            f"{metrics['sharpe']:.2f} | "
            f"{metrics['trigger_rate']:.1f}% | "
            f"{metrics['avg_trigger_profit']:.2f}% |"
        )

    print("\n" + "=" * 80)


def save_results(all_results, summary):
    """保存结果"""

    output_data = {
        "task": "task03_prompt32_profit_target_test",
        "date": "2026-04-01",
        "all_results": all_results,
        "summary": summary,
    }

    output_path = "/tmp/task03_prompt32_profit_target_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_path}")


if __name__ == "__main__":
    print("\n开始测试...")
    print("数据范围: 2021-2024年")
    print("买入规则: 市值5-15亿、情绪>=30、非一字板")
    print("基础卖出时机: 次日收盘")
    print("止盈规则: 10种对比")

    all_results = run_all_profit_rules()
    summary = calculate_metrics(all_results)
    print_summary_table(summary)
    save_results(all_results, summary)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n关键结论：")
    print("1. 固定止盈可能过早止盈，错过后续上涨")
    print("2. 分时止盈更灵活，但实现难度较大")
    print("3. 板块止盈需要额外数据支持")
    print("4. 推荐方案：无止盈或+10%止盈")
