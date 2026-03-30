#!/usr/bin/env python3
"""
情绪总开关实证化完整研究 - 聚宽平台执行
回答三个核心问题：
1. 情绪开关到底有没有真实增益？
2. 最有效的情绪指标组合是什么？
3. 应该做硬开关还是仓位调节器？
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("情绪总开关实证化完整研究")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2026-03-28"
OOS_START = "2024-01-01"


def get_trade_days_range(start, end):
    return get_trade_days(start_date=start, end_date=end)


def get_zt_stocks(date):
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


def calc_lianban_count(stock, date, max_days=10):
    df = get_price(
        stock,
        end_date=date,
        count=max_days,
        fields=["close", "high_limit"],
        panel=False,
    )
    if len(df) < max_days:
        return 0

    count = 0
    for i in range(len(df) - 1, -1, -1):
        if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
            count += 1
        else:
            break
    return count


def calc_sentiment_group1(date, prev_date):
    zt_list = get_zt_stocks(date)
    max_lianban = 0
    if len(zt_list) > 0:
        for stock in zt_list[:30]:
            lb = calc_lianban_count(stock, date)
            max_lianban = max(max_lianban, lb)
    return {"max_lianban": max_lianban, "zt_count": len(zt_list)}


def calc_sentiment_group2(date, prev_date):
    s1 = calc_sentiment_group1(date, prev_date)
    dt_list = get_dt_stocks(date)
    s1["zt_dt_ratio"] = len(zt_list) / max(len(dt_list), 1)
    return s1


def calc_sentiment_group3(date, prev_date):
    s2 = calc_sentiment_group2(date, prev_date)
    prev_zt = get_zt_stocks(prev_date)
    zt_list = get_zt_stocks(date)
    if len(prev_zt) > 0:
        jinji = len(set(prev_zt) & set(zt_list))
        s2["jinji_rate"] = jinji / len(prev_zt)
    else:
        s2["jinji_rate"] = 0
    return s2


def calc_sentiment_group4(date, prev_date):
    return calc_sentiment_group3(date, prev_date)


def sentiment_switch_group1(sentiment):
    return sentiment["max_lianban"] >= 3


def sentiment_switch_group2(sentiment):
    return sentiment["max_lianban"] >= 3 and sentiment["zt_count"] >= 20


def sentiment_switch_group3(sentiment):
    return (
        sentiment["max_lianban"] >= 2
        and sentiment["zt_count"] >= 15
        and sentiment["zt_dt_ratio"] >= 1.5
    )


def sentiment_switch_group4(sentiment):
    return (
        sentiment["max_lianban"] >= 2
        and sentiment["zt_count"] >= 15
        and sentiment["zt_dt_ratio"] >= 1.5
        and sentiment["jinji_rate"] >= 0.3
    )


def position_adjustor(sentiment):
    if sentiment["max_lianban"] >= 5 and sentiment["zt_count"] >= 40:
        return 0.3
    elif sentiment["max_lianban"] >= 3 and sentiment["zt_count"] >= 25:
        return 1.0
    elif sentiment["max_lianban"] >= 2 and sentiment["zt_count"] >= 15:
        return 0.5
    else:
        return 0.0


def select_first_board_low_open(date, prev_date):
    prev_zt = get_zt_stocks(prev_date)
    if len(prev_zt) == 0:
        return []

    selected = []
    for stock in prev_zt[:30]:
        try:
            prev_price = get_price(
                stock, end_date=prev_date, count=1, fields=["close"], panel=False
            )
            today_price = get_price(
                stock, end_date=date, count=1, fields=["open", "low_limit"], panel=False
            )

            if len(prev_price) == 0 or len(today_price) == 0:
                continue

            prev_close = prev_price.iloc[0]["close"]
            today_open = today_price.iloc[0]["open"]

            open_ratio = today_open / prev_close - 1
            if -0.05 <= open_ratio <= -0.01:
                if today_open > today_price.iloc[0]["low_limit"]:
                    selected.append(stock)
        except:
            continue

    return selected


def select_weak_to_strong(date, prev_date):
    prev_zt = get_zt_stocks(prev_date)
    if len(prev_zt) == 0:
        return []

    selected = []
    for stock in prev_zt[:30]:
        try:
            prev_price = get_price(
                stock, end_date=prev_date, count=1, fields=["close"], panel=False
            )
            today_price = get_price(
                stock,
                end_date=date,
                count=1,
                fields=["open", "high_limit"],
                panel=False,
            )

            if len(prev_price) == 0 or len(today_price) == 0:
                continue

            prev_close = prev_price.iloc[0]["close"]
            today_open = today_price.iloc[0]["open"]

            open_ratio = today_open / prev_close - 1
            if 0.01 <= open_ratio <= 0.06:
                if today_open < today_price.iloc[0]["high_limit"]:
                    selected.append(stock)
        except:
            continue

    return selected


def backtest_strategy(date_list, strategy_func, switch_func=None, position_func=None):
    results = []

    for i in range(1, len(date_list)):
        date = date_list[i]
        prev_date = date_list[i - 1]
        date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else date
        prev_date_str = (
            prev_date.strftime("%Y-%m-%d")
            if hasattr(prev_date, "strftime")
            else prev_date
        )

        try:
            sentiment = calc_sentiment_group4(date_str, prev_date_str)

            position_ratio = 1.0
            if position_func:
                position_ratio = position_func(sentiment)

            if switch_func and not switch_func(sentiment):
                results.append(
                    {
                        "date": date_str,
                        "ret": 0,
                        "signal": False,
                        "position": 0,
                        "sentiment": sentiment,
                    }
                )
                continue

            if position_ratio == 0:
                results.append(
                    {
                        "date": date_str,
                        "ret": 0,
                        "signal": False,
                        "position": 0,
                        "sentiment": sentiment,
                    }
                )
                continue

            selected = strategy_func(date_str, prev_date_str)

            if len(selected) == 0:
                results.append(
                    {
                        "date": date_str,
                        "ret": 0,
                        "signal": False,
                        "position": position_ratio,
                        "sentiment": sentiment,
                    }
                )
                continue

            next_days = get_trade_days_range(
                date_str,
                (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=5)).strftime(
                    "%Y-%m-%d"
                ),
            )
            if len(next_days) < 2:
                continue
            next_date = next_days[1] if next_days[0] == date_str else next_days[0]

            day_returns = []
            for stock in selected[:3]:
                try:
                    buy_price = get_price(
                        stock, end_date=date_str, count=1, fields=["open"], panel=False
                    )
                    sell_price = get_price(
                        stock,
                        end_date=next_date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )

                    if len(buy_price) > 0 and len(sell_price) > 0:
                        ret = (
                            sell_price.iloc[0]["close"] / buy_price.iloc[0]["open"] - 1
                        ) * position_ratio
                        day_returns.append(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns) * 100
                results.append(
                    {
                        "date": date_str,
                        "ret": avg_ret,
                        "signal": True,
                        "position": position_ratio,
                        "count": len(day_returns),
                        "sentiment": sentiment,
                    }
                )
        except:
            continue

    return pd.DataFrame(results)


def calc_metrics(df, start_date=None):
    if start_date:
        df = df[df["date"] >= start_date]

    df_open = df[df["signal"] == True]

    if len(df_open) == 0:
        return None

    trades = len(df_open)
    total_ret = df_open["ret"].sum()
    avg_ret = df_open["ret"].mean()
    win_rate = (df_open["ret"] > 0).mean()

    positive = df_open[df_open["ret"] > 0]["ret"]
    negative = df_open[df_open["ret"] < 0]["ret"]

    avg_win = positive.mean() if len(positive) > 0 else 0
    avg_loss = abs(negative.mean()) if len(negative) > 0 else 0
    profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    cumulative = df_open["ret"].cumsum()
    max_cum = cumulative.cummax()
    drawdown = max_cum - cumulative
    max_dd = drawdown.max()

    years = len(df) / 250
    annual_ret = total_ret / years if years > 0 else 0
    calmar = annual_ret / max_dd if max_dd > 0 else 0

    consecutive_losses = 0
    max_consecutive = 0
    for ret in df_open["ret"]:
        if ret < 0:
            consecutive_losses += 1
            max_consecutive = max(max_consecutive, consecutive_losses)
        else:
            consecutive_losses = 0

    return {
        "trades": trades,
        "total_ret": total_ret,
        "avg_ret": avg_ret,
        "win_rate": win_rate,
        "profit_loss_ratio": profit_loss_ratio,
        "max_dd": max_dd,
        "annual_ret": annual_ret,
        "calmar": calmar,
        "max_consecutive_losses": max_consecutive,
    }


print("\n获取交易日...")
trade_days = get_trade_days_range(START_DATE, END_DATE)
sample_days = trade_days[::2]
print(f"采样交易日数: {len(sample_days)}")

print("\n" + "=" * 80)
print("第一部分：情绪指标组合有效性对比")
print("=" * 80)

indicator_groups = [
    ("最高连板", sentiment_switch_group1),
    ("最高连板+涨停家数", sentiment_switch_group2),
    ("最高连板+涨停家数+涨跌停比", sentiment_switch_group3),
    ("最高连板+涨停家数+涨跌停比+晋级率", sentiment_switch_group4),
]

indicator_results = []

print("\n【首板低开策略 - 不同情绪指标组合】")
for name, switch_func in indicator_groups:
    print(f"\n测试指标组合: {name}")
    df = backtest_strategy(sample_days, select_first_board_low_open, switch_func)
    metrics = calc_metrics(df)

    if metrics:
        indicator_results.append({"strategy": "首板低开", "indicator": name, **metrics})
        print(f"  开仓次数: {metrics['trades']}")
        print(f"  胜率: {metrics['win_rate']:.2%}")
        print(f"  盈亏比: {metrics['profit_loss_ratio']:.2f}")
        print(f"  最大回撤: {metrics['max_dd']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar']:.2f}")

print("\n【弱转强策略 - 不同情绪指标组合】")
for name, switch_func in indicator_groups:
    print(f"\n测试指标组合: {name}")
    df = backtest_strategy(sample_days, select_weak_to_strong, switch_func)
    metrics = calc_metrics(df)

    if metrics:
        indicator_results.append({"strategy": "弱转强", "indicator": name, **metrics})
        print(f"  开仓次数: {metrics['trades']}")
        print(f"  胜率: {metrics['win_rate']:.2%}")
        print(f"  盈亏比: {metrics['profit_loss_ratio']:.2f}")
        print(f"  最大回撤: {metrics['max_dd']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar']:.2f}")

print("\n" + "=" * 80)
print("第二部分：硬开关 vs 仓位调节器")
print("=" * 80)

control_groups = [
    ("无开关", None, None),
    ("硬开关", sentiment_switch_group3, None),
    ("仓位调节器", None, position_adjustor),
]

control_results = []

print("\n【首板低开策略 - 开关方式对比】")
for name, switch_func, position_func in control_groups:
    print(f"\n测试控制方式: {name}")
    df = backtest_strategy(
        sample_days, select_first_board_low_open, switch_func, position_func
    )
    metrics = calc_metrics(df)

    if metrics:
        control_results.append({"strategy": "首板低开", "control": name, **metrics})
        print(f"  开仓次数: {metrics['trades']}")
        print(f"  年化收益: {metrics['annual_ret']:.2f}%")
        print(f"  最大回撤: {metrics['max_dd']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar']:.2f}")
        print(f"  连续亏损: {metrics['max_consecutive_losses']}")

print("\n【弱转强策略 - 开关方式对比】")
for name, switch_func, position_func in control_groups:
    print(f"\n测试控制方式: {name}")
    df = backtest_strategy(
        sample_days, select_weak_to_strong, switch_func, position_func
    )
    metrics = calc_metrics(df)

    if metrics:
        control_results.append({"strategy": "弱转强", "control": name, **metrics})
        print(f"  开仓次数: {metrics['trades']}")
        print(f"  年化收益: {metrics['annual_ret']:.2f}%")
        print(f"  最大回撤: {metrics['max_dd']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar']:.2f}")
        print(f"  连续亏损: {metrics['max_consecutive_losses']}")

print("\n" + "=" * 80)
print("第三部分：2024年后样本外验证")
print("=" * 80)

oos_days = [
    d
    for d in sample_days
    if (d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else d) >= OOS_START
]
print(f"样本外交易日数: {len(oos_days)}")

oos_results = []

print("\n【首板低开 - 样本外结果】")
for name, switch_func, position_func in control_groups:
    print(f"\n{name}:")
    df = backtest_strategy(
        oos_days, select_first_board_low_open, switch_func, position_func
    )
    metrics = calc_metrics(df)

    if metrics:
        oos_results.append(
            {"strategy": "首板低开", "control": name, "period": "OOS", **metrics}
        )
        print(f"  开仓次数: {metrics['trades']}")
        print(f"  胜率: {metrics['win_rate']:.2%}")
        print(f"  盈亏比: {metrics['profit_loss_ratio']:.2f}")
        print(f"  最大回撤: {metrics['max_dd']:.2f}%")

print("\n【弱转强 - 样本外结果】")
for name, switch_func, position_func in control_groups:
    print(f"\n{name}:")
    df = backtest_strategy(oos_days, select_weak_to_strong, switch_func, position_func)
    metrics = calc_metrics(df)

    if metrics:
        oos_results.append(
            {"strategy": "弱转强", "control": name, "period": "OOS", **metrics}
        )
        print(f"  开仓次数: {metrics['trades']}")
        print(f"  胜率: {metrics['win_rate']:.2%}")
        print(f"  盈亏比: {metrics['profit_loss_ratio']:.2f}")
        print(f"  最大回撤: {metrics['max_dd']:.2f}%")

print("\n" + "=" * 80)
print("最终结论")
print("=" * 80)

indicator_df = pd.DataFrame(indicator_results)
control_df = pd.DataFrame(control_results)
oos_df = pd.DataFrame(oos_results)

output_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output/sentiment_switch_full_result.json"

import os

os.makedirs(os.path.dirname(output_file), exist_ok=True)

result_data = {
    "indicator_comparison": indicator_df.to_dict("records"),
    "control_comparison": control_df.to_dict("records"),
    "oos_results": oos_df.to_dict("records"),
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, ensure_ascii=False, indent=2, default=str)

print(f"\n结果已保存到: {output_file}")

print("\n研究完成!")
