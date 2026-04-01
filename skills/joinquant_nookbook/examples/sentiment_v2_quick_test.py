#!/usr/bin/env python3
"""
情绪层v2完善测试 - 快速版本
只测试关键参数，快速得出结论
"""

from jqdata import *
import numpy as np
import json

print("=" * 80)
print("情绪层v2完善测试 - 快速版本")
print("=" * 80)

# 测试日期：每月取1个
TEST_DATES = [
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
]

OOS_START = "2024-01-01"
STOCK_LIMIT = 200

print(f"\n测试日期数: {len(TEST_DATES)}")


def get_zt_count(date):
    """获取涨停家数"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ][:STOCK_LIMIT]

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
    except:
        return 0


def test_strategy(threshold_low=30, threshold_high=999, position_levels=None):
    """测试策略"""
    signal_count = 0
    oos_signal_count = 0
    returns = []
    oos_returns = []
    wins = 0
    oos_wins = 0

    for i in range(1, len(TEST_DATES)):
        prev_date = TEST_DATES[i - 1]
        date = TEST_DATES[i]

        try:
            zt_count = get_zt_count(prev_date)

            # 阈值过滤
            if zt_count < threshold_low or zt_count > threshold_high:
                continue

            # 仓位计算
            if position_levels:
                position_ratio = 0
                for thresh, ratio in position_levels:
                    if zt_count >= thresh:
                        position_ratio = ratio
                        break
                if position_ratio <= 0:
                    continue
            else:
                position_ratio = 1.0

            signal_count += 1
            if date >= OOS_START:
                oos_signal_count += 1

            # 获取涨停股票并计算收益
            prev_all = get_all_securities("stock", prev_date).index.tolist()
            prev_all = [
                s
                for s in prev_all
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ][:150]

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
            )[:2]

            if len(prev_zt_stocks) == 0:
                continue

            day_returns = []
            for stock in prev_zt_stocks:
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
                avg_ret = np.mean(day_returns) * position_ratio
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

    return {
        "signal_count": signal_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
        "oos_signal_count": oos_signal_count,
        "oos_avg_return": round(oos_avg_return, 3),
        "oos_win_rate": round(oos_win_rate, 2),
    }


# ============================================================
# 测试1：阈值优化
# ============================================================
print("\n" + "=" * 60)
print("测试1：阈值优化")
print("=" * 60)

threshold_results = {}
for threshold in [20, 30, 40, 50, 60, 80, 100]:
    print(f"\n测试阈值 {threshold}...")
    result = test_strategy(threshold_low=threshold)
    threshold_results[threshold] = result
    print(
        f"  样本内: 信号{result['signal_count']}, 收益{result['avg_return']}%, 胜率{result['win_rate']}%"
    )
    print(
        f"  样本外: 信号{result['oos_signal_count']}, 收益{result['oos_avg_return']}%, 胜率{result['oos_win_rate']}%"
    )

# ============================================================
# 测试2：过热过滤
# ============================================================
print("\n" + "=" * 60)
print("测试2：过热过滤")
print("=" * 60)

overheat_results = {}
for overheat in [80, 100, 120]:
    print(f"\n测试过热阈值 {overheat}...")
    result = test_strategy(threshold_low=30, threshold_high=overheat)
    overheat_results[overheat] = result
    print(
        f"  样本内: 信号{result['signal_count']}, 收益{result['avg_return']}%, 胜率{result['win_rate']}%"
    )
    print(
        f"  样本外: 信号{result['oos_signal_count']}, 收益{result['oos_avg_return']}%, 胜率{result['oos_win_rate']}%"
    )

# ============================================================
# 测试3：仓位分层
# ============================================================
print("\n" + "=" * 60)
print("测试3：仓位分层")
print("=" * 60)

position_3_levels = [(100, 0.0), (50, 1.0), (30, 0.5), (0, 0.0)]
position_5_levels = [(100, 0.0), (80, 1.0), (50, 0.8), (30, 0.5), (15, 0.25), (0, 0.0)]

position_results = {}

print("\n测试3档仓位...")
result = test_strategy(threshold_low=15, position_levels=position_3_levels)
position_results["3档"] = result
print(
    f"  样本内: 信号{result['signal_count']}, 加权收益{result['avg_return']}%, 胜率{result['win_rate']}%"
)
print(
    f"  样本外: 信号{result['oos_signal_count']}, 加权收益{result['oos_avg_return']}%, 胜率{result['oos_win_rate']}%"
)

print("\n测试5档仓位...")
result = test_strategy(threshold_low=15, position_levels=position_5_levels)
position_results["5档"] = result
print(
    f"  样本内: 信号{result['signal_count']}, 加权收益{result['avg_return']}%, 胜率{result['win_rate']}%"
)
print(
    f"  样本外: 信号{result['oos_signal_count']}, 加权收益{result['oos_avg_return']}%, 胜率{result['oos_win_rate']}%"
)

# ============================================================
# 汇总结果
# ============================================================
print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)

print("\n【测试1：阈值优化】")
for t, r in sorted(threshold_results.items()):
    print(
        f"  阈值{t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
    )

print("\n【测试2：过热过滤】")
for t, r in sorted(overheat_results.items()):
    print(
        f"  过热{t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
    )

print("\n【测试3：仓位分层】")
for t, r in position_results.items():
    print(
        f"  {t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
    )

# 保存结果
all_results = {
    "threshold": threshold_results,
    "overheat": overheat_results,
    "position": position_results,
}

output_path = "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_v2_quick_test_results.json"
with open(output_path, "w") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存: {output_path}")
print("\n=== 测试完成 ===")
