#!/usr/bin/env python3
"""
任务06v2：情绪开关阈值优化 - Notebook格式
测试阈值：0, 30, 50（三个关键阈值）
"""

from jqdata import *
import numpy as np
import json

print("=" * 80)
print("任务06v2：情绪开关阈值优化")
print("测试阈值：0(基准), 30(当前), 50(高情绪)")
print("=" * 80)

thresholds = [0, 30, 50]
test_dates = [
    "2021-01-15",
    "2021-04-15",
    "2021-07-15",
    "2021-10-15",
    "2022-01-15",
    "2022-04-15",
    "2022-07-15",
    "2022-10-15",
    "2023-01-15",
    "2023-04-15",
    "2023-07-15",
    "2023-10-15",
    "2024-01-15",
    "2024-04-15",
    "2024-07-15",
    "2024-10-15",
    "2025-01-15",
]

OOS_START = "2024-01-01"

print(f"\n测试日期数: {len(test_dates)}")


def get_zt_count(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ][:800]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    return len(df[df["close"] == df["high_limit"]])


results = {}

for threshold in thresholds:
    print(f"\n测试阈值 {threshold}...")

    signal_count = 0
    oos_signal_count = 0
    returns = []
    oos_returns = []
    wins = 0
    oos_wins = 0

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        date = test_dates[i]

        try:
            zt_count = get_zt_count(prev_date)

            if threshold > 0 and zt_count < threshold:
                continue

            signal_count += 1
            if date >= OOS_START:
                oos_signal_count += 1

            prev_zt_stocks = []
            prev_all = get_all_securities("stock", prev_date).index.tolist()
            prev_all = [
                s
                for s in prev_all
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ][:500]

            prev_df = get_price(
                prev_all,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                fill_paused=False,
            )
            prev_df = prev_df.dropna()
            prev_zt_stocks = list(
                prev_df[prev_df["close"] == prev_df["high_limit"]]["code"]
            )[:5]

            if len(prev_zt_stocks) == 0:
                continue

            day_returns = []
            for stock in prev_zt_stocks[:3]:
                try:
                    buy_df = get_price(
                        stock,
                        end_date=date,
                        count=1,
                        fields=["open", "high_limit"],
                        panel=False,
                    )
                    sell_df = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )

                    if len(buy_df) > 0 and len(sell_df) > 0:
                        buy_open = buy_df.iloc[0]["open"]
                        sell_close = sell_df.iloc[0]["close"]

                        if buy_open < buy_df.iloc[0]["high_limit"]:
                            ret = (sell_close / buy_open - 1) * 100
                            day_returns.append(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                returns.append(avg_ret)
                if date >= OOS_START:
                    oos_returns.append(avg_ret)

                if avg_ret > 0:
                    wins += 1
                    if date >= OOS_START:
                        oos_wins += 1

        except Exception as e:
            print(f"  {date} 错误: {e}")
            continue

    avg_return = np.mean(returns) if len(returns) > 0 else 0
    win_rate = wins / len(returns) * 100 if len(returns) > 0 else 0

    oos_avg_return = np.mean(oos_returns) if len(oos_returns) > 0 else 0
    oos_win_rate = oos_wins / len(oos_returns) * 100 if len(oos_returns) > 0 else 0

    results[threshold] = {
        "signal_count": signal_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
        "oos_signal_count": oos_signal_count,
        "oos_avg_return": round(oos_avg_return, 3),
        "oos_win_rate": round(oos_win_rate, 2),
    }

    print(f"  样本内: 信号{signal_count}, 收益{avg_return:.3f}%, 胜率{win_rate:.2f}%")
    print(
        f"  样本外: 信号{oos_signal_count}, 收益{oos_avg_return:.3f}%, 胜率{oos_win_rate:.2f}%"
    )

print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

for t, r in results.items():
    print(f"\n阈值{t}:")
    print(
        f"  样本内: {r['signal_count']}次, 收益{r['avg_return']}%, 胜率{r['win_rate']}%"
    )
    print(
        f"  样本外: {r['oos_signal_count']}次, 收益{r['oos_avg_return']}%, 胜率{r['oos_win_rate']}%"
    )

output_path = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_threshold_results.json"
)
with open(output_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存: {output_path}")
print("\n=== 测试完成 ===")
