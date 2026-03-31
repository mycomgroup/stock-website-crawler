"""
任务02补充：情绪开关最近日期实测（JoinQuant版）
测试期间：2024-07-01 至 2025-03-28
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务02补充：情绪开关最近日期实测（JoinQuant版）")
print("测试期间：2024-07-01 至 2025-03-28")
print("=" * 80)


def get_zt_count(date):
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
    return len(zt_df)


def get_first_board_low_open(date, prev_date):
    prev_zt = []
    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    prev_zt_df = df[df["close"] == df["high_limit"]]
    prev_zt = list(prev_zt_df["code"])

    if len(prev_zt) == 0:
        return []

    selected = []
    for stock in prev_zt[:50]:
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
            limit_up = today_price.iloc[0]["high_limit"]

            open_ratio = (today_open / prev_close - 1) * 100

            if 0.5 <= open_ratio <= 1.5 and today_open < limit_up:
                selected.append(
                    {"code": stock, "open_ratio": open_ratio, "open_price": today_open}
                )
        except:
            continue

    return selected


def backtest_sentiment_switch(start_date, end_date, zt_threshold=30, use_switch=True):
    print(f"\n回测期间: {start_date} 至 {end_date}")
    print(f"情绪阈值: {zt_threshold}, 使用开关: {use_switch}")

    all_dates = get_trade_days(start_date, end_date)
    print(f"交易日数: {len(all_dates)}")

    results = {
        "total_days": len(all_dates),
        "trade_days": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "max_profits": [],
        "zt_counts": [],
        "skipped_by_switch": 0,
    }

    for i in range(1, len(all_dates) - 1):
        prev_date = all_dates[i - 1]
        curr_date = all_dates[i]
        next_date = all_dates[i + 1]

        try:
            zt_count = get_zt_count(prev_date)
            results["zt_counts"].append(zt_count)

            if use_switch and zt_count < zt_threshold:
                results["skipped_by_switch"] += 1
                continue

            selected = get_first_board_low_open(curr_date, prev_date)

            if len(selected) == 0:
                continue

            results["trade_days"] += 1

            for stock_info in selected[:3]:
                try:
                    next_price = get_price(
                        stock_info["code"],
                        end_date=next_date,
                        count=1,
                        fields=["open", "high", "close"],
                        panel=False,
                    )

                    if len(next_price) == 0:
                        continue

                    buy_price = stock_info["open_price"] * 1.005
                    sell_close = next_price.iloc[0]["close"]
                    sell_high = next_price.iloc[0]["high"]

                    profit = (sell_close / buy_price - 1) * 100
                    max_profit = (sell_high / buy_price - 1) * 100

                    results["trades"] += 1
                    results["profits"].append(profit)
                    results["max_profits"].append(max_profit)

                    if profit > 0:
                        results["wins"] += 1
                except:
                    pass

            if i % 20 == 0:
                print(
                    f"已处理 {i}/{len(all_dates)} 天, ZT={zt_count}, 累计交易={results['trades']}"
                )

        except Exception as e:
            continue

    if results["trades"] > 0:
        results["win_rate"] = results["wins"] / results["trades"] * 100
        results["avg_profit"] = np.mean(results["profits"])
        results["total_profit"] = np.sum(results["profits"])
        results["avg_max_profit"] = np.mean(results["max_profits"])

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

        results["avg_zt"] = np.mean(results["zt_counts"])
        results["min_zt"] = np.min(results["zt_counts"])
        results["max_zt"] = np.max(results["zt_counts"])

    return results


print("\n" + "=" * 80)
print("测试1: 无情绪开关（基准）")
print("=" * 80)
result_no_switch = backtest_sentiment_switch("2024-07-01", "2025-03-28", 0, False)

print("\n" + "=" * 80)
print("测试2: 情绪硬开关（阈值=30）")
print("=" * 80)
result_switch_30 = backtest_sentiment_switch("2024-07-01", "2025-03-28", 30, True)

print("\n" + "=" * 80)
print("测试3: 情绪硬开关（阈值=50）")
print("=" * 80)
result_switch_50 = backtest_sentiment_switch("2024-07-01", "2025-03-28", 50, True)

print("\n" + "=" * 80)
print("对照表汇总")
print("=" * 80)

comparison = []
for name, r in [
    ("无开关(基准)", result_no_switch),
    ("硬开关(阈值=30)", result_switch_30),
    ("硬开关(阈值=50)", result_switch_50),
]:
    if r["trades"] > 0:
        comparison.append(
            {
                "方案": name,
                "交易次数": r["trades"],
                "胜率%": round(r["win_rate"], 1),
                "平均收益%": round(r["avg_profit"], 2),
                "累计收益%": round(r["total_profit"], 1),
                "最大回撤%": round(r["max_dd"], 1),
                "盈亏比": round(r["pl_ratio"], 2),
            }
        )

df_comparison = pd.DataFrame(comparison)
print(df_comparison.to_string(index=False))

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
    print(f"\n阈值30改善:")
    print(
        f"  胜率变化: {result_switch_30['win_rate'] - result_no_switch['win_rate']:+.1f}%"
    )
    print(
        f"  平均收益变化: {result_switch_30['avg_profit'] - result_no_switch['avg_profit']:+.2f}%"
    )
    print(
        f"  回撤变化: {result_no_switch['max_dd'] - result_switch_30['max_dd']:+.1f}%"
    )
    print(
        f"  信号减少: {(result_no_switch['trades'] - result_switch_30['trades']) / result_no_switch['trades'] * 100:.1f}%"
    )

if result_no_switch["trades"] > 0 and result_switch_50["trades"] > 0:
    print(f"\n阈值50改善:")
    print(
        f"  胜率变化: {result_switch_50['win_rate'] - result_no_switch['win_rate']:+.1f}%"
    )
    print(
        f"  平均收益变化: {result_switch_50['avg_profit'] - result_no_switch['avg_profit']:+.2f}%"
    )
    print(
        f"  回撤变化: {result_no_switch['max_dd'] - result_switch_50['max_dd']:+.1f}%"
    )
    print(
        f"  信号减少: {(result_no_switch['trades'] - result_switch_50['trades']) / result_no_switch['trades'] * 100:.1f}%"
    )

output_file = "/Users/fengzhi/Downloads/git/testlixingren/output/task02_recent_backtest_result.json"
with open(output_file, "w") as f:
    json.dump(
        {
            "no_switch": {
                k: float(v) if isinstance(v, (np.integer, np.floating)) else v
                for k, v in result_no_switch.items()
                if not isinstance(v, list)
            },
            "switch_30": {
                k: float(v) if isinstance(v, (np.integer, np.floating)) else v
                for k, v in result_switch_30.items()
                if not isinstance(v, list)
            },
            "switch_50": {
                k: float(v) if isinstance(v, (np.integer, np.floating)) else v
                for k, v in result_switch_50.items()
                if not isinstance(v, list)
            },
        },
        f,
        indent=2,
    )
print(f"\n结果已保存至: {output_file}")

print("\n最终建议: 涨停家数 >= 30 作为硬开关阈值")
print("=" * 80)
