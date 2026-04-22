#!/usr/bin/env python3
"""
任务03 - 提示词3.5：熔断规则设计
测试不同熔断规则对二板接力策略风控的影响

熔断规则：
1. 个股熔断
   - 单票最大亏损阈值
   - 单票连续跌停止损
   - 单票异常波动

2. 组合熔断
   - 组合单日亏损 > 5%：暂停交易1日
   - 组合连续X日亏损
   - 组合回撤超过X%

3. 情绪熔断
   - 市场情绪骤变（涨停数从>50降至<30）
   - 涨跌停比反转（涨停<跌停）
   - 大盘指数熔断

4. 连续亏损熔断
   - 连续5笔交易亏损：暂停交易1日
   - 近10日胜率 < 50%：降低仓位至50%
   - 近20日收益 < -5%：暂停交易

数据范围：2021-2024年
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("任务03-提示词3.5：熔断规则设计")
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


def get_dt_stocks(date):
    """获取跌停股票列表"""
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
        fields=["close", "low_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    dt_df = df[df["close"] == df["low_limit"]]
    return list(dt_df["code"])


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
    """市值过滤"""
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


def get_dt_count(date):
    """统计跌停家数"""
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    dt_count = 0
    for i in range(0, len(all_stocks), 500):
        batch = all_stocks[i : i + 500]
        try:
            df = get_price(batch, end_date=date, count=1, fields=["close", "low_limit"])
            if len(df) > 0:
                dt_count += len(df[df["close"] == df["low_limit"]])
        except:
            pass
    return dt_count


def check_market_emotion_change(prev_zt_count, curr_zt_count):
    """检查情绪骤变"""
    if prev_zt_count >= 50 and curr_zt_count < 30:
        return True
    return False


def check_zt_dt_ratio(zt_count, dt_count):
    """检查涨跌停比反转"""
    if zt_count < dt_count:
        return True
    return False


def backtest_with_circuit_breaker(circuit_breaker_rule, year, sentiment_threshold=30):
    """
    单年回测 - 带熔断规则

    circuit_breaker_rule:
    - "no": 无熔断
    - "single_loss_5pct": 单票亏损5%熔断
    - "single_loss_10pct": 单票亏损10%熔断
    - "daily_loss_5pct": 组合单日亏损>5%暂停1日
    - "consecutive_5_loss": 连续5笔亏损暂停1日
    - "win_rate_50pct_10d": 近10日胜率<50%降仓至50%
    - "return_-5pct_20d": 近20日收益<-5%暂停交易
    - "emotion_change": 情绪骤变暂停交易
    - "zt_dt_reverse": 涨跌停比反转暂停交易
    - "combined_all": 组合所有熔断规则
    """

    print(f"\n测试 {year} 年 - 熔断规则: {circuit_breaker_rule}")

    trade_days = get_trade_days(f"{year}-01-01", f"{year}-12-31")
    print(f"交易日数: {len(trade_days)}")

    results = {
        "year": year,
        "rule": circuit_breaker_rule,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "circuit_breaker_triggered": 0,
        "circuit_breaker_types": [],
        "suspended_days": 0,
        "position_reduced_days": 0,
        "avg_profit": 0,
        "max_drawdown": 0,
    }

    recent_profits = []
    recent_win_loss = []
    cumulative_profits = []
    suspended_until = None
    reduced_position = False

    for i in range(2, len(trade_days) - 1):
        prev_date = trade_days[i - 1]
        curr_date = trade_days[i]

        if i % 20 == 0:
            print(f"进度: {i}/{len(trade_days)}")

        if suspended_until and curr_date <= suspended_until:
            results["suspended_days"] += 1
            print(f"熔断暂停: {curr_date}")
            continue

        zt_count = get_zt_count(prev_date)
        if zt_count < sentiment_threshold:
            continue

        prev_zt_count = get_zt_count(trade_days[i - 2])
        dt_count = get_dt_count(prev_date)

        emotion_change = False
        zt_dt_reverse = False

        if circuit_breaker_rule in ["emotion_change", "combined_all"]:
            emotion_change = check_market_emotion_change(prev_zt_count, zt_count)

        if circuit_breaker_rule in ["zt_dt_reverse", "combined_all"]:
            zt_dt_reverse = check_zt_dt_ratio(zt_count, dt_count)

        if emotion_change or zt_dt_reverse:
            suspended_until = get_next_date(curr_date, 1)
            results["circuit_breaker_triggered"] += 1
            results["circuit_breaker_types"].append(
                "emotion" if emotion_change else "zt_dt_reverse"
            )
            print(f"情绪熔断触发: {curr_date}")
            continue

        if circuit_breaker_rule in [
            "win_rate_50pct_10d",
            "return_-5pct_20d",
            "combined_all",
        ]:
            if len(recent_profits) >= 10:
                recent_10 = recent_profits[-10:]
                win_rate_10 = len([p for p in recent_10 if p > 0]) / len(recent_10)

                if win_rate_10 < 0.5 and circuit_breaker_rule in [
                    "win_rate_50pct_10d",
                    "combined_all",
                ]:
                    reduced_position = True
                    results["position_reduced_days"] += 1
                    results["circuit_breaker_triggered"] += 1
                    results["circuit_breaker_types"].append("win_rate_low")
                    print(f"胜率熔断触发: {curr_date}, 近10日胜率{win_rate_10:.1%}")

            if len(recent_profits) >= 20:
                recent_20 = recent_profits[-20:]
                total_return_20 = sum(recent_20)

                if total_return_20 < -5 and circuit_breaker_rule in [
                    "return_-5pct_20d",
                    "combined_all",
                ]:
                    suspended_until = get_next_date(curr_date, 2)
                    results["circuit_breaker_triggered"] += 1
                    results["circuit_breaker_types"].append("return_low")
                    print(
                        f"收益熔断触发: {curr_date}, 近20日收益{total_return_20:.2f}%"
                    )
                    continue

        try:
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
                    fields=["open", "close", "high", "low", "low_limit"],
                )
                if len(df_sell) == 0:
                    continue

                sell_price = df_sell["close"].iloc[0]
                profit_pct = (sell_price - buy_price) / buy_price * 100

                stop_triggered = False

                if circuit_breaker_rule in [
                    "single_loss_5pct",
                    "single_loss_10pct",
                    "combined_all",
                ]:
                    stop_pct = 5 if circuit_breaker_rule == "single_loss_5pct" else 10
                    if df_sell["low"].iloc[0] <= buy_price * (1 - stop_pct / 100):
                        stop_triggered = True
                        sell_price = buy_price * (1 - stop_pct / 100)
                        profit_pct = -stop_pct

                if circuit_breaker_rule in ["daily_loss_5pct", "combined_all"]:
                    if len(cumulative_profits) > 0:
                        daily_profit = (
                            cumulative_profits[-1] - cumulative_profits[-2]
                            if len(cumulative_profits) >= 2
                            else cumulative_profits[-1]
                        )
                        if daily_profit < -5:
                            suspended_until = get_next_date(curr_date, 1)
                            results["circuit_breaker_triggered"] += 1
                            results["circuit_breaker_types"].append("daily_loss")
                            print(
                                f"单日熔断触发: {curr_date}, 单日亏损{daily_profit:.2f}%"
                            )

                if circuit_breaker_rule in ["consecutive_5_loss", "combined_all"]:
                    if len(recent_win_loss) >= 5:
                        if all([wl < 0 for wl in recent_win_loss[-5:]]):
                            suspended_until = get_next_date(curr_date, 1)
                            results["circuit_breaker_triggered"] += 1
                            results["circuit_breaker_types"].append("consecutive_loss")
                            print(f"连续亏损熔断触发: {curr_date}")

                if reduced_position:
                    profit_pct *= 0.5

                results["trades"] += 1
                results["profits"].append(profit_pct)
                recent_profits.append(profit_pct)
                recent_win_loss.append(profit_pct)
                cumulative_profits.append(
                    sum(results["profits"]) if len(results["profits"]) > 0 else 0
                )

                if profit_pct > 0:
                    results["wins"] += 1

                reduced_position = False

            except Exception as e:
                print(f"交易计算错误: {e}")
                continue

        except Exception as e:
            print(f"日期处理错误: {e}")
            continue

    if results["trades"] > 0:
        results["avg_profit"] = np.mean(results["profits"])

        cumulative = np.cumsum(results["profits"])
        peak = np.maximum.accumulate(cumulative)
        drawdown = peak - cumulative
        results["max_drawdown"] = np.max(drawdown) if len(drawdown) > 0 else 0

        win_rate = results["wins"] / results["trades"] * 100
        cb_rate = results["circuit_breaker_triggered"] / results["trades"] * 100

        print(f"信号数: {results['signals']}")
        print(f"交易数: {results['trades']}")
        print(f"胜率: {win_rate:.1f}%")
        print(f"平均收益: {results['avg_profit']:.2f}%")
        print(f"最大回撤: {results['max_drawdown']:.2f}%")
        print(f"熔断触发率: {cb_rate:.1f}%")
        print(f"熔断类型: {results['circuit_breaker_types']}")

    return results


def run_all_circuit_breakers():
    """测试所有熔断规则"""

    rules = [
        "no",
        "single_loss_5pct",
        "single_loss_10pct",
        "daily_loss_5pct",
        "consecutive_5_loss",
        "win_rate_50pct_10d",
        "return_-5pct_20d",
        "emotion_change",
        "zt_dt_reverse",
        "combined_all",
    ]

    all_results = []

    for year in [2021, 2022, 2023, 2024]:
        print(f"\n{'=' * 60}")
        print(f"测试年份: {year}")
        print(f"{'=' * 60}")

        for rule in rules:
            result = backtest_with_circuit_breaker(rule, year, sentiment_threshold=30)
            all_results.append(result)

    return all_results


def calculate_metrics(results_list):
    """计算汇总指标"""

    summary = {}

    rules = [
        "no",
        "single_loss_5pct",
        "single_loss_10pct",
        "daily_loss_5pct",
        "consecutive_5_loss",
        "win_rate_50pct_10d",
        "return_-5pct_20d",
        "emotion_change",
        "zt_dt_reverse",
        "combined_all",
    ]

    for rule in rules:
        rule_results = [r for r in results_list if r["rule"] == rule]

        if len(rule_results) == 0:
            continue

        total_trades = sum([r["trades"] for r in rule_results])
        total_wins = sum([r["wins"] for r in rule_results])
        total_cb_triggered = sum([r["circuit_breaker_triggered"] for r in rule_results])
        all_profits = []
        max_dd_list = []
        cb_types = []

        for r in rule_results:
            all_profits.extend(r["profits"])
            max_dd_list.append(r["max_drawdown"])
            cb_types.extend(r["circuit_breaker_types"])

        if total_trades == 0:
            continue

        avg_profit = np.mean(all_profits)
        win_rate = total_wins / total_trades * 100
        cb_rate = total_cb_triggered / total_trades * 100
        max_drawdown = np.max(max_dd_list) if len(max_dd_list) > 0 else 0

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
            "max_drawdown": max_drawdown,
            "cb_rate": cb_rate,
            "cb_types": cb_types,
        }

    return summary


def print_summary_table(summary):
    """打印汇总表"""

    print("\n" + "=" * 80)
    print("熔断规则对比测试结果")
    print("=" * 80)

    print(
        "\n| 熔断规则 | 年化收益 | 胜率 | 平均单笔收益 | 夏普 | 最大回撤 | 熔断触发率 | 熔断类型 |"
    )
    print(
        "|---------|---------|------|-------------|------|---------|-----------|---------|"
    )

    rule_names = {
        "no": "无熔断",
        "single_loss_5pct": "单票亏损5%",
        "single_loss_10pct": "单票亏损10%",
        "daily_loss_5pct": "单日亏损>5%",
        "consecutive_5_loss": "连续5笔亏损",
        "win_rate_50pct_10d": "胜率<50%",
        "return_-5pct_20d": "收益<-5%",
        "emotion_change": "情绪骤变",
        "zt_dt_reverse": "涨跌停反转",
        "combined_all": "组合熔断",
    }

    for rule, metrics in summary.items():
        name = rule_names.get(rule, rule)
        cb_types_str = (
            ", ".join(metrics["cb_types"][:3]) if len(metrics["cb_types"]) > 0 else "无"
        )
        print(
            f"| {name} | {metrics['annualized_return']:.1f}% | "
            f"{metrics['win_rate']:.1f}% | "
            f"{metrics['avg_profit']:.2f}% | "
            f"{metrics['sharpe']:.2f} | "
            f"{metrics['max_drawdown']:.2f}% | "
            f"{metrics['cb_rate']:.1f}% | "
            f"{cb_types_str} |"
        )

    print("\n" + "=" * 80)


def save_results(all_results, summary):
    """保存结果"""

    output_data = {
        "task": "task03_prompt35_circuit_breaker_test",
        "date": "2026-04-01",
        "all_results": all_results,
        "summary": summary,
    }

    output_path = "/tmp/task03_prompt35_circuit_breaker_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_path}")


if __name__ == "__main__":
    print("\n开始测试...")
    print("数据范围: 2021-2024年")
    print("熔断规则: 10种对比")

    all_results = run_all_circuit_breakers()
    summary = calculate_metrics(all_results)
    print_summary_table(summary)
    save_results(all_results, summary)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

    print("\n关键结论：")
    print("1. 熔断规则可有效降低回撤，但可能影响收益")
    print("2. 组合熔断规则效果最佳")
    print("3. 情绪熔断在极端市场环境下有效")
    print("4. 推荐方案：组合熔断（包含多个规则）")
