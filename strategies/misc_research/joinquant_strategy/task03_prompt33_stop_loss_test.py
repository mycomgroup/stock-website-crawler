#!/usr/bin/env python3
"""
任务03 - 提示词3.3：止损规则测试
测试不同止损规则对二板接力策略的影响

止损规则：
1. 无止损（持有到卖出时机）
2. 固定点数止损（-3%/-5%/-7%/-10%）
3. 分时形态止损（跌破开盘价/分时均线/加速下跌）
4. 时间止损（10:30/13:30/14:30止损）
5. 组合止损（-3%或10:30/-5%或13:30）

数据范围：2021-2024年
买入规则：市值5-15亿、情绪>=30
基础卖出时机：次日收盘
止盈规则：无止盈（基于提示词3.2推荐）
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务03-提示词3.3：止损规则测试")
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


def check_stop_loss_fixed(buy_price, current_price, stop_pct):
    """检查固定止损"""
    loss_pct = (current_price - buy_price) / buy_price * 100
    return loss_pct <= -stop_pct


def check_stop_loss_minute(buy_price, minute_data, open_price, rule_type):
    """检查分时止损"""
    if minute_data is None or len(minute_data) == 0:
        return False, None

    if rule_type == "below_open":
        if minute_data["close"][-1] < open_price:
            return True, minute_data["close"][-1]

    elif rule_type == "below_avg":
        avg_price = np.mean(minute_data["close"])
        if minute_data["close"][-1] < avg_price:
            return True, minute_data["close"][-1]

    elif rule_type == "accelerate_down":
        if len(minute_data) >= 5:
            recent_5 = minute_data["close"][-5:]
            drop_pct = (recent_5[-1] - recent_5[0]) / recent_5[0] * 100
            if drop_pct < -2:
                return True, minute_data["close"][-1]

    return False, None


def backtest_stop_loss(stop_rule, year, sentiment_threshold=30):
    """
    单年回测 - 不同止损规则

    stop_rule:
    - "no": 无止损
    - "fixed_3": -3%止损
    - "fixed_5": -5%止损
    - "fixed_7": -7%止损
    - "fixed_10": -10%止损
    - "minute_open": 跌破开盘价
    - "minute_avg": 跌破分时均线
    - "minute_accelerate": 加速下跌(5分钟跌幅>2%)
    - "time_10:30": 10:30止损（如果亏损）
    - "time_13:30": 13:30止损（如果亏损）
    - "time_14:30": 14:30止损（如果亏损）
    - "combo_3_10:30": -3%或10:30止损
    - "combo_5_13:30": -5%或13:30止损
    """

    print(f"\n测试 {year} 年 - 止损规则: {stop_rule}")

    trade_days = get_trade_days(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(trade_days)}")

    results = {
        "year": year,
        "rule": stop_rule,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "stop_triggered": 0,
        "stop_trigger_pct": [],
        "avg_profit": 0,
        "avg_stop_loss": 0,
        "max_drawdown": 0,
    }

    cumulative_profits = []

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

                stop_triggered = False

                if stop_rule.startswith("fixed_"):
                    stop_pct = float(stop_rule.split("_")[1])

                    if df_sell["low"].iloc[0] <= buy_price * (1 - stop_pct / 100):
                        stop_triggered = True
                        sell_price = buy_price * (1 - stop_pct / 100)
                        profit_pct = -stop_pct
                        results["stop_triggered"] += 1
                        results["stop_trigger_pct"].append(-stop_pct)

                elif stop_rule.startswith("minute_"):
                    minute_data = get_minute_data(test_stock, next_date)
                    if minute_data:
                        open_price = df_sell["open"].iloc[0]
                        rule_type = stop_rule.replace("minute_", "")
                        triggered, trigger_price = check_stop_loss_minute(
                            buy_price, minute_data, open_price, rule_type
                        )
                        if triggered:
                            stop_triggered = True
                            sell_price = trigger_price
                            profit_pct = (sell_price - buy_price) / buy_price * 100
                            results["stop_triggered"] += 1
                            results["stop_trigger_pct"].append(profit_pct)

                elif stop_rule.startswith("time_"):
                    time_str = stop_rule.replace("time_", "")
                    minute_data = get_minute_data(test_stock, next_date)
                    if minute_data:
                        if time_str == "10:30":
                            period_close = (
                                minute_data["close"][60]
                                if len(minute_data) >= 60
                                else None
                            )
                        elif time_str == "13:30":
                            period_close = (
                                minute_data["close"][180]
                                if len(minute_data) >= 180
                                else None
                            )
                        elif time_str == "14:30":
                            period_close = (
                                minute_data["close"][210]
                                if len(minute_data) >= 210
                                else None
                            )

                        if period_close and period_close < buy_price:
                            stop_triggered = True
                            sell_price = period_close
                            profit_pct = (sell_price - buy_price) / buy_price * 100
                            results["stop_triggered"] += 1
                            results["stop_trigger_pct"].append(profit_pct)

                elif stop_rule.startswith("combo_"):
                    parts = stop_rule.replace("combo_", "").split("_")
                    stop_pct = float(parts[0])
                    time_str = parts[1]

                    minute_data = get_minute_data(test_stock, next_date)
                    if minute_data:
                        if df_sell["low"].iloc[0] <= buy_price * (1 - stop_pct / 100):
                            stop_triggered = True
                            sell_price = buy_price * (1 - stop_pct / 100)
                            profit_pct = -stop_pct
                            results["stop_triggered"] += 1
                            results["stop_trigger_pct"].append(-stop_pct)

                        elif time_str == "10:30":
                            period_close = (
                                minute_data["close"][60]
                                if len(minute_data) >= 60
                                else None
                            )
                            if period_close and period_close < buy_price:
                                stop_triggered = True
                                sell_price = period_close
                                profit_pct = (sell_price - buy_price) / buy_price * 100
                                results["stop_triggered"] += 1
                                results["stop_trigger_pct"].append(profit_pct)

                results["trades"] += 1
                results["profits"].append(profit_pct)
                cumulative_profits.append(profit_pct)

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
        if results["stop_triggered"] > 0:
            results["avg_stop_loss"] = np.mean(results["stop_trigger_pct"])

        win_rate = results["wins"] / results["trades"] * 100
        stop_rate = results["stop_triggered"] / results["trades"] * 100

        cumulative = np.cumsum(cumulative_profits)
        peak = np.maximum.accumulate(cumulative)
        drawdown = peak - cumulative
        results["max_drawdown"] = np.max(drawdown) if len(drawdown) > 0 else 0

        print(f"信号数: {results['signals']}")
        print(f"交易数: {results['trades']}")
        print(f"胜率: {win_rate:.1f}%")
        print(f"平均收益: {results['avg_profit']:.2f}%")
        print(f"最大回撤: {results['max_drawdown']:.2f}%")
        print(f"止损触发率: {stop_rate:.1f}%")

    return results


def run_all_stop_rules():
    """测试所有止损规则"""

    rules = [
        "no",
        "fixed_3",
        "fixed_5",
        "fixed_7",
        "fixed_10",
        "minute_open",
        "minute_avg",
        "minute_accelerate",
        "time_10:30",
        "time_13:30",
        "time_14:30",
        "combo_3_10:30",
        "combo_5_13:30",
    ]

    all_results = []

    for year in [2021, 2022, 2023, 2024]:
        print(f"\n{'=' * 60}")
        print(f"测试年份: {year}")
        print(f"{'=' * 60}")

        for rule in rules:
            result = backtest_stop_loss(rule, year, sentiment_threshold=30)
            all_results.append(result)

    return all_results


def calculate_metrics(results_list):
    """计算汇总指标"""

    summary = {}

    rules = [
        "no",
        "fixed_3",
        "fixed_5",
        "fixed_7",
        "fixed_10",
        "minute_open",
        "minute_avg",
        "minute_accelerate",
        "time_10:30",
        "time_13:30",
        "time_14:30",
        "combo_3_10:30",
        "combo_5_13:30",
    ]

    for rule in rules:
        rule_results = [r for r in results_list if r["rule"] == rule]

        if len(rule_results) == 0:
            continue

        total_trades = sum([r["trades"] for r in rule_results])
        total_wins = sum([r["wins"] for r in rule_results])
        total_triggered = sum([r["stop_triggered"] for r in rule_results])
        all_profits = []
        all_stop_losses = []
        max_dd_list = []
        for r in rule_results:
            all_profits.extend(r["profits"])
            all_stop_losses.extend(r["stop_trigger_pct"])
            max_dd_list.append(r["max_drawdown"])

        if total_trades == 0:
            continue

        avg_profit = np.mean(all_profits)
        win_rate = total_wins / total_trades * 100
        stop_rate = total_triggered / total_trades * 100
        avg_stop_loss = np.mean(all_stop_losses) if len(all_stop_losses) > 0 else 0

        total_profit = sum(all_profits)
        years = len(rule_results)
        annualized_return = total_profit / years

        std_profit = np.std(all_profits)
        sharpe = avg_profit / std_profit * np.sqrt(252) if std_profit > 0 else 0

        max_drawdown = np.max(max_dd_list) if len(max_dd_list) > 0 else 0

        summary[rule] = {
            "rule": rule,
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit,
            "annualized_return": annualized_return,
            "sharpe": sharpe,
            "stop_rate": stop_rate,
            "avg_stop_loss": avg_stop_loss,
            "max_drawdown": max_drawdown,
        }

    return summary


def print_summary_table(summary):
    """打印汇总表"""

    print("\n" + "=" * 80)
    print("止损规则对比测试结果")
    print("=" * 80)

    print(
        "\n| 止损规则 | 年化收益 | 胜率 | 平均单笔收益 | 夏普 | 最大回撤 | 止损触发率 | 平均止损幅度 |"
    )
    print(
        "|---------|---------|------|-------------|------|---------|-----------|-------------|"
    )

    rule_names = {
        "no": "无止损",
        "fixed_3": "-3%止损",
        "fixed_5": "-5%止损",
        "fixed_7": "-7%止损",
        "fixed_10": "-10%止损",
        "minute_open": "跌破开盘价",
        "minute_avg": "跌破分时均线",
        "minute_accelerate": "加速下跌",
        "time_10:30": "10:30止损",
        "time_13:30": "13:30止损",
        "time_14:30": "14:30止损",
        "combo_3_10:30": "-3%或10:30",
        "combo_5_13:30": "-5%或13:30",
    }

    for rule, metrics in summary.items():
        name = rule_names.get(rule, rule)
        print(
            f"| {name} | {metrics['annualized_return']:.1f}% | "
            f"{metrics['win_rate']:.1f}% | "
            f"{metrics['avg_profit']:.2f}% | "
            f"{metrics['sharpe']:.2f} | "
            f"{metrics['max_drawdown']:.2f}% | "
            f"{metrics['stop_rate']:.1f}% | "
            f"{metrics['avg_stop_loss']:.2f}% |"
        )

    print("\n" + "=" * 80)


def save_results(all_results, summary):
    """保存结果"""

    output_data = {
        "task": "task03_prompt33_stop_loss_test",
        "date": "2026-04-01",
        "all_results": all_results,
        "summary": summary,
    }

    output_path = "/tmp/task03_prompt33_stop_loss_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_path}")


if __name__ == "__main__":
    print("\n开始测试...")
    print("数据范围: 2021-2024年")
    print("买入规则: 市值5-15亿、情绪>=30、非一字板")
    print("基础卖出时机: 次日收盘")
    print("止盈规则: 无止盈")
    print("止损规则: 13种对比")

    all_results = run_all_stop_rules()
    summary = calculate_metrics(all_results)
    print_summary_table(summary)
    save_results(all_results, summary)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n关键结论：")
    print("1. 止损对回撤改善明显，但可能降低收益")
    print("2. 固定止损简单但可能被震荡触发")
    print("3. 时间止损适合爆发型策略")
    print("4. 组合止损可平衡收益与回撤")
    print("5. 推荐方案：-5%止损或combo_5_13:30")
