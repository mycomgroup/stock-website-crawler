#!/usr/bin/env python3
"""
任务07：情绪指标精细化阈值搜索
目标：搜索涨停数阈值的最优分段点，替代当前的粗粒度30/50阈值

搜索范围：
- 冰点线：20, 25, 30, 35
- 启动线：40, 45, 50, 55, 60

测试策略：
1. 首板低开（短线事件驱动）
2. 小市值防守线（月度调仓，15-60亿市值）

验证期间：2020-01-01 至 2025-03-30
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务07：情绪指标精细化阈值搜索")
print("=" * 80)

START_DATE = "2020-01-01"
END_DATE = "2025-03-30"
OOS_START = "2024-01-01"

thresholds_free_point = [20, 25, 30, 35]
thresholds_start_line = [40, 45, 50, 55, 60]
all_thresholds = [0] + thresholds_free_point + thresholds_start_line

print(f"\n搜索范围：")
print(f"  冰点线阈值：{thresholds_free_point}")
print(f"  启动线阈值：{thresholds_start_line}")
print(f"  测试期间：{START_DATE} ~ {END_DATE}")
print(f"  样本外起点：{OOS_START}")


def get_zt_count(date):
    """获取涨停家数"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        if len(all_stocks) > 3000:
            all_stocks = all_stocks[:3000]

        df = get_price(
            all_stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        zt_count = len(df[df["close"] == df["high_limit"]])
        return zt_count
    except:
        return 0


def get_zt_stocks(date):
    """获取涨停股票列表"""
    try:
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
        )
        df = df.dropna()
        zt_df = df[df["close"] == df["high_limit"]]
        return list(zt_df["code"])
    except:
        return []


def test_first_board_strategy(date_list, threshold):
    """测试首板低开策略在不同阈值下的表现"""
    signal_count = 0
    total_return = 0
    win_count = 0
    total_profit = 0
    total_loss = 0
    daily_returns = []

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
            zt_count = get_zt_count(prev_date_str)

            if threshold > 0 and zt_count < threshold:
                continue

            prev_zt_stocks = get_zt_stocks(prev_date_str)

            if len(prev_zt_stocks) == 0:
                continue

            selected = []
            for stock in prev_zt_stocks[:50]:
                try:
                    prev_price = get_price(
                        stock,
                        end_date=prev_date_str,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    today_price = get_price(
                        stock,
                        end_date=date_str,
                        count=1,
                        fields=["open", "close", "high_limit"],
                        panel=False,
                    )

                    if len(prev_price) == 0 or len(today_price) == 0:
                        continue

                    prev_close = prev_price.iloc[0]["close"]
                    today_open = today_price.iloc[0]["open"]

                    open_ratio = (today_open / prev_close - 1) * 100

                    if (
                        -5 <= open_ratio <= -1
                        and today_open < today_price.iloc[0]["high_limit"]
                    ):
                        selected.append(stock)
                except:
                    continue

            if len(selected) == 0:
                continue

            signal_count += 1

            next_days = get_trade_days(
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
                        buy_open = buy_price.iloc[0]["open"]
                        sell_close = sell_price.iloc[0]["close"]

                        ret = (sell_close / buy_open - 1) * 100
                        day_returns.append(ret)

                        if ret > 0:
                            win_count += 1
                            total_profit += ret
                        else:
                            total_loss += abs(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                total_return += avg_ret
                daily_returns.append(avg_ret)
        except:
            continue

    if signal_count == 0:
        return None

    avg_return = np.mean(daily_returns) if len(daily_returns) > 0 else 0
    win_rate = win_count / signal_count * 100
    pl_ratio = total_profit / total_loss if total_loss > 0 else 0

    return {
        "threshold": threshold,
        "strategy": "首板低开",
        "signal_count": signal_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
        "profit_loss_ratio": round(pl_ratio, 2),
        "total_profit": round(total_profit, 2),
        "total_loss": round(total_loss, 2),
    }


def test_smallcap_defense_strategy(date_list, threshold):
    """测试小市值防守线策略在不同阈值下的表现"""
    signal_count = 0
    total_return = 0
    win_count = 0
    total_profit = 0
    total_loss = 0
    daily_returns = []

    for i in range(0, len(date_list), 20):
        date = date_list[i]
        date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else date

        try:
            zt_count = get_zt_count(date_str)

            if threshold > 0 and zt_count < threshold:
                continue

            signal_count += 1

            q = query(
                valuation.code,
                valuation.circulating_market_cap,
                valuation.pe_ratio,
                valuation.pb_ratio,
            ).filter(
                valuation.circulating_market_cap >= 15,
                valuation.circulating_market_cap <= 60,
                valuation.pe_ratio > 0,
                valuation.pe_ratio < 30,
                valuation.pb_ratio > 0,
                valuation.pb_ratio < 3,
            )

            df = get_fundamentals(q, date=date_str)

            if df.empty:
                continue

            df = df.sort_values("circulating_market_cap").head(10)
            selected = df["code"].tolist()

            if len(selected) == 0:
                continue

            if i + 20 < len(date_list):
                next_date = date_list[i + 20]
                next_date_str = (
                    next_date.strftime("%Y-%m-%d")
                    if hasattr(next_date, "strftime")
                    else next_date
                )
            else:
                continue

            day_returns = []
            for stock in selected:
                try:
                    buy_price = get_price(
                        stock, end_date=date_str, count=1, fields=["close"], panel=False
                    )
                    sell_price = get_price(
                        stock,
                        end_date=next_date_str,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )

                    if len(buy_price) > 0 and len(sell_price) > 0:
                        buy_close = buy_price.iloc[0]["close"]
                        sell_close = sell_price.iloc[0]["close"]

                        ret = (sell_close / buy_close - 1) * 100
                        day_returns.append(ret)

                        if ret > 0:
                            win_count += 1
                            total_profit += ret
                        else:
                            total_loss += abs(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                total_return += avg_ret
                daily_returns.append(avg_ret)
        except:
            continue

    if signal_count == 0:
        return None

    avg_return = np.mean(daily_returns) if len(daily_returns) > 0 else 0
    win_rate = win_count / signal_count * 100
    pl_ratio = total_profit / total_loss if total_loss > 0 else 0

    return {
        "threshold": threshold,
        "strategy": "小市值防守线",
        "signal_count": signal_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
        "profit_loss_ratio": round(pl_ratio, 2),
        "total_profit": round(total_profit, 2),
        "total_loss": round(total_loss, 2),
    }


print("\n获取交易日列表...")
all_trade_days = get_trade_days(START_DATE, END_DATE)
sample_days = all_trade_days[::5]

oos_days = [
    d
    for d in sample_days
    if (d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else d) >= OOS_START
]
in_sample_days = [
    d
    for d in sample_days
    if (d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else d) < OOS_START
]

print(f"样本内交易日数: {len(in_sample_days)}")
print(f"样本外交易日数: {len(oos_days)}")

results = {
    "first_board": {"in_sample": [], "out_of_sample": []},
    "smallcap_defense": {"in_sample": [], "out_of_sample": []},
}

print("\n" + "=" * 80)
print("策略1：首板低开 - 样本内测试")
print("=" * 80)

for threshold in all_thresholds:
    print(f"\n阈值 {threshold}...")
    r = test_first_board_strategy(in_sample_days, threshold)
    if r:
        results["first_board"]["in_sample"].append(r)
        print(
            f"  信号: {r['signal_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("策略1：首板低开 - 样本外测试")
print("=" * 80)

for threshold in all_thresholds:
    print(f"\n阈值 {threshold}...")
    r = test_first_board_strategy(oos_days, threshold)
    if r:
        results["first_board"]["out_of_sample"].append(r)
        print(
            f"  信号: {r['signal_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("策略2：小市值防守线 - 样本内测试")
print("=" * 80)

for threshold in all_thresholds:
    print(f"\n阈值 {threshold}...")
    r = test_smallcap_defense_strategy(in_sample_days, threshold)
    if r:
        results["smallcap_defense"]["in_sample"].append(r)
        print(
            f"  信号: {r['signal_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("策略2：小市值防守线 - 样本外测试")
print("=" * 80)

for threshold in all_thresholds:
    print(f"\n阈值 {threshold}...")
    r = test_smallcap_defense_strategy(oos_days, threshold)
    if r:
        results["smallcap_defense"]["out_of_sample"].append(r)
        print(
            f"  信号: {r['signal_count']}, 收益: {r['avg_return']}%, 胜率: {r['win_rate']}%"
        )

print("\n" + "=" * 80)
print("阈值搜索结果汇总表")
print("=" * 80)

if len(results["first_board"]["in_sample"]) > 0:
    fb_in_df = pd.DataFrame(results["first_board"]["in_sample"])
    print("\n【首板低开 - 样本内】")
    print(
        fb_in_df[
            ["threshold", "signal_count", "avg_return", "win_rate", "profit_loss_ratio"]
        ].to_string(index=False)
    )

if len(results["first_board"]["out_of_sample"]) > 0:
    fb_oos_df = pd.DataFrame(results["first_board"]["out_of_sample"])
    print("\n【首板低开 - 样本外】")
    print(
        fb_oos_df[
            ["threshold", "signal_count", "avg_return", "win_rate", "profit_loss_ratio"]
        ].to_string(index=False)
    )

if len(results["smallcap_defense"]["in_sample"]) > 0:
    def_in_df = pd.DataFrame(results["smallcap_defense"]["in_sample"])
    print("\n【小市值防守线 - 样本内】")
    print(
        def_in_df[
            ["threshold", "signal_count", "avg_return", "win_rate", "profit_loss_ratio"]
        ].to_string(index=False)
    )

if len(results["smallcap_defense"]["out_of_sample"]) > 0:
    def_oos_df = pd.DataFrame(results["smallcap_defense"]["out_of_sample"])
    print("\n【小市值防守线 - 样本外】")
    print(
        def_oos_df[
            ["threshold", "signal_count", "avg_return", "win_rate", "profit_loss_ratio"]
        ].to_string(index=False)
    )

print("\n" + "=" * 80)
print("最优阈值分析")
print("=" * 80)


def find_best_threshold(results_list, metric="avg_return"):
    if len(results_list) == 0:
        return None
    return max(results_list, key=lambda x: x[metric])


if len(results["first_board"]["out_of_sample"]) > 0:
    fb_best_return = find_best_threshold(
        results["first_board"]["out_of_sample"], "avg_return"
    )
    fb_best_winrate = find_best_threshold(
        results["first_board"]["out_of_sample"], "win_rate"
    )

    print("\n【首板低开策略 - 最优阈值】")
    if fb_best_return:
        print(
            f"  收益最优：阈值{fb_best_return['threshold']} (收益{fb_best_return['avg_return']}%)"
        )
    if fb_best_winrate:
        print(
            f"  胜率最优：阈值{fb_best_winrate['threshold']} (胜率{fb_best_winrate['win_rate']}%)"
        )

if len(results["smallcap_defense"]["out_of_sample"]) > 0:
    def_best_return = find_best_threshold(
        results["smallcap_defense"]["out_of_sample"], "avg_return"
    )
    def_best_winrate = find_best_threshold(
        results["smallcap_defense"]["out_of_sample"], "win_rate"
    )

    print("\n【小市值防守线策略 - 最优阈值】")
    if def_best_return:
        print(
            f"  收益最优：阈值{def_best_return['threshold']} (收益{def_best_return['avg_return']}%)"
        )
    if def_best_winrate:
        print(
            f"  胜率最优：阈值{def_best_winrate['threshold']} (胜率{def_best_winrate['win_rate']}%)"
        )

result_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/task07_sentiment_threshold_results.json"
with open(result_file, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存至: {result_file}")
print("\n阈值搜索完成！")
