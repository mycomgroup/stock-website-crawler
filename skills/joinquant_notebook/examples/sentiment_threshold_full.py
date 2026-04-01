#!/usr/bin/env python3
"""
任务06v2：情绪开关阈值优化 - Notebook格式
增加测试日期，查看涨停家数分布
"""

from jqdata import *
import numpy as np
import json

print("=" * 80)
print("任务06v2：情绪开关阈值优化")
print("=" * 80)

thresholds = [0, 20, 30, 40, 50, 60, 80, 100]

all_dates = get_trade_days("2021-01-01", "2025-03-28")
test_dates = all_dates[::20]

OOS_START = "2024-01-01"

print(f"\n总交易日数: {len(all_dates)}")
print(f"测试日期数: {len(test_dates)}")


def get_zt_count(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ][:1500]

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


zt_distribution = {}
print("\n获取涨停家数分布...")
for date in test_dates[:30]:
    try:
        zt_count = get_zt_count(date)
        zt_distribution[date] = zt_count
        print(f"  {date}: {zt_count}涨停")
    except Exception as e:
        print(f"  {date}: 错误 {e}")

zt_counts = list(zt_distribution.values())
print(f"\n涨停家数统计:")
print(f"  平均值: {np.mean(zt_counts):.1f}")
print(f"  最大值: {np.max(zt_counts)}")
print(f"  最小值: {np.min(zt_counts)}")
print(f"  中位数: {np.median(zt_counts):.1f}")

threshold_pass_count = {}
for t in thresholds:
    count = sum(1 for z in zt_counts if z >= t)
    threshold_pass_count[t] = count
    print(f"  阈值{t}: {count}天通过 ({count / len(zt_counts) * 100:.1f}%)")

print("\n" + "=" * 80)
print("各阈值测试")
print("=" * 80)

results = {}

for threshold in thresholds:
    print(f"\n阈值 {threshold}...")

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
            ][:800]

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
            )[:10]

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

    if signal_count > 0:
        print(f"  样本内: {signal_count}次, 收益{avg_return:.3f}%, 胜率{win_rate:.2f}%")
        print(
            f"  样本外: {oos_signal_count}次, 收益{oos_avg_return:.3f}%, 胜率{oos_win_rate:.2f}%"
        )
    else:
        print(f"  无信号")

print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

for t, r in results.items():
    if r["signal_count"] > 0:
        print(
            f"阈值{t}: 样本内{r['signal_count']}次(收益{r['avg_return']}%,胜率{r['win_rate']}%) | 样本外{r['oos_signal_count']}次(收益{r['oos_avg_return']}%,胜率{r['oos_win_rate']}%)"
        )

output_path = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_threshold_results.json"
)
output_data = {
    "zt_distribution": zt_distribution,
    "threshold_pass_count": threshold_pass_count,
    "results": results,
}

try:
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存: {output_path}")
except Exception as e:
    print(f"\n保存失败: {e}")

print("\n=== 测试完成 ===")
