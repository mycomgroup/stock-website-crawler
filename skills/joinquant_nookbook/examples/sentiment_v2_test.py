#!/usr/bin/env python3
"""
情绪层v2完善测试 - 小规模版本
测试所有选项：阈值、过热过滤、仓位分层、趋势周期、动态阈值
"""

from jqdata import *
import numpy as np
import json
from datetime import datetime, timedelta

print("=" * 80)
print("情绪层v2完善测试 - 小规模版本")
print("=" * 80)

# ============================================================
# 配置参数
# ============================================================

# 测试日期：每月取1个，减少计算量
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
    "2025-01-15",
    "2025-02-15",
    "2025-03-15",
]

OOS_START = "2024-01-01"
STOCK_LIMIT = 300  # 只取300只股票，加速测试

# 测试参数
THRESHOLDS = [20, 30, 40, 50, 60, 80, 100]
OVERHEAT_THRESHOLDS = [80, 100, 120]
TREND_PERIODS = [5, 10]  # 趋势周期：5日 vs 10日

# 仓位档位
POSITION_3_LEVELS = [
    (100, 0.0),  # 过热
    (50, 1.0),  # 高情绪
    (30, 0.5),  # 中情绪
    (0, 0.0),  # 低情绪
]

POSITION_5_LEVELS = [
    (100, 0.0),  # 过热
    (80, 1.0),  # 极高
    (50, 0.8),  # 高
    (30, 0.5),  # 中
    (15, 0.25),  # 低
    (0, 0.0),  # 极低
]

print(f"\n测试日期数: {len(TEST_DATES)}")
print(f"股票数量限制: {STOCK_LIMIT}")
print(f"样本外起点: {OOS_START}")


# ============================================================
# 工具函数
# ============================================================


def get_zt_count(date, stock_limit=STOCK_LIMIT):
    """获取涨停家数"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ][:stock_limit]

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


def get_zt_counts_history(end_date, days=10):
    """获取历史涨停家数"""
    counts = []
    trade_days = get_trade_days(end_date=end_date, count=days)

    for d in trade_days:
        count = get_zt_count(d)
        counts.append(count)

    return counts


def calculate_trend(zt_counts, period):
    """计算趋势"""
    if len(zt_counts) < period:
        return "stable"

    recent = zt_counts[-period:]
    older = (
        zt_counts[-2 * period : -period]
        if len(zt_counts) >= 2 * period
        else zt_counts[:period]
    )

    recent_avg = sum(recent) / len(recent)
    older_avg = sum(older) / len(older)

    if recent_avg > older_avg * 1.1:
        return "up"
    elif recent_avg < older_avg * 0.9:
        return "down"
    else:
        return "stable"


def get_position_ratio(zt_count, position_levels):
    """根据仓位档位计算仓位比例"""
    for threshold, ratio in position_levels:
        if zt_count >= threshold:
            return ratio
    return 0.0


def dynamic_threshold(base_threshold, trend, method="fixed"):
    """动态阈值调整"""
    if method == "fixed":
        # 固定调整：±15%
        if trend == "up":
            return base_threshold * 0.85
        elif trend == "down":
            return base_threshold * 1.15
        else:
            return base_threshold
    elif method == "intensity":
        # 趋势强度调整：根据趋势强度调整
        if trend == "up":
            return base_threshold * 0.8
        elif trend == "down":
            return base_threshold * 1.2
        else:
            return base_threshold
    else:
        return base_threshold


# ============================================================
# 测试函数
# ============================================================


def test_threshold_only():
    """测试1：仅阈值优化"""
    print("\n" + "=" * 60)
    print("测试1：仅阈值优化")
    print("=" * 60)

    results = {}

    for threshold in THRESHOLDS:
        print(f"\n测试阈值 {threshold}...")

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
                if threshold > 0 and zt_count < threshold:
                    continue

                signal_count += 1
                if date >= OOS_START:
                    oos_signal_count += 1

                # 获取涨停股票并计算收益
                prev_all = get_all_securities("stock", prev_date).index.tolist()
                prev_all = [
                    s
                    for s in prev_all
                    if not (
                        s.startswith("68") or s.startswith("4") or s.startswith("8")
                    )
                ][:200]

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
                )[:3]

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

        print(
            f"  样本内: 信号{signal_count}, 收益{avg_return:.3f}%, 胜率{win_rate:.2f}%"
        )
        print(
            f"  样本外: 信号{oos_signal_count}, 收益{oos_avg_return:.3f}%, 胜率{oos_win_rate:.2f}%"
        )

    return results


def test_overheat_filter():
    """测试2：过热过滤"""
    print("\n" + "=" * 60)
    print("测试2：过热过滤")
    print("=" * 60)

    results = {}
    base_threshold = 30  # 使用当前阈值

    for overheat in OVERHEAT_THRESHOLDS:
        print(f"\n测试过热阈值 {overheat}...")

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

                # 阈值过滤 + 过热过滤
                if zt_count < base_threshold or zt_count > overheat:
                    continue

                signal_count += 1
                if date >= OOS_START:
                    oos_signal_count += 1

                # 获取涨停股票并计算收益
                prev_all = get_all_securities("stock", prev_date).index.tolist()
                prev_all = [
                    s
                    for s in prev_all
                    if not (
                        s.startswith("68") or s.startswith("4") or s.startswith("8")
                    )
                ][:200]

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
                )[:3]

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

        results[overheat] = {
            "signal_count": signal_count,
            "avg_return": round(avg_return, 3),
            "win_rate": round(win_rate, 2),
            "oos_signal_count": oos_signal_count,
            "oos_avg_return": round(oos_avg_return, 3),
            "oos_win_rate": round(oos_win_rate, 2),
        }

        print(
            f"  样本内: 信号{signal_count}, 收益{avg_return:.3f}%, 胜率{win_rate:.2f}%"
        )
        print(
            f"  样本外: 信号{oos_signal_count}, 收益{oos_avg_return:.3f}%, 胜率{oos_win_rate:.2f}%"
        )

    return results


def test_position_levels():
    """测试3：仓位分层"""
    print("\n" + "=" * 60)
    print("测试3：仓位分层")
    print("=" * 60)

    results = {}
    base_threshold = 30

    for name, levels in [("3档", POSITION_3_LEVELS), ("5档", POSITION_5_LEVELS)]:
        print(f"\n测试仓位分层 {name}...")

        signal_count = 0
        oos_signal_count = 0
        weighted_returns = []
        oos_weighted_returns = []
        wins = 0
        oos_wins = 0

        for i in range(1, len(TEST_DATES)):
            prev_date = TEST_DATES[i - 1]
            date = TEST_DATES[i]

            try:
                zt_count = get_zt_count(prev_date)

                # 获取仓位比例
                position_ratio = get_position_ratio(zt_count, levels)

                if position_ratio <= 0:
                    continue

                signal_count += 1
                if date >= OOS_START:
                    oos_signal_count += 1

                # 获取涨停股票并计算收益
                prev_all = get_all_securities("stock", prev_date).index.tolist()
                prev_all = [
                    s
                    for s in prev_all
                    if not (
                        s.startswith("68") or s.startswith("4") or s.startswith("8")
                    )
                ][:200]

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
                )[:3]

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
                    avg_ret = np.mean(day_returns)
                    weighted_ret = avg_ret * position_ratio  # 加权收益
                    weighted_returns.append(weighted_ret)
                    if date >= OOS_START:
                        oos_weighted_returns.append(weighted_ret)

                    if weighted_ret > 0:
                        wins += 1
                        if date >= OOS_START:
                            oos_wins += 1

            except Exception as e:
                print(f"  {date} 错误: {e}")
                continue

        avg_return = np.mean(weighted_returns) if len(weighted_returns) > 0 else 0
        win_rate = (
            wins / len(weighted_returns) * 100 if len(weighted_returns) > 0 else 0
        )

        oos_avg_return = (
            np.mean(oos_weighted_returns) if len(oos_weighted_returns) > 0 else 0
        )
        oos_win_rate = (
            oos_wins / len(oos_weighted_returns) * 100
            if len(oos_weighted_returns) > 0
            else 0
        )

        results[name] = {
            "signal_count": signal_count,
            "avg_return": round(avg_return, 3),
            "win_rate": round(win_rate, 2),
            "oos_signal_count": oos_signal_count,
            "oos_avg_return": round(oos_avg_return, 3),
            "oos_win_rate": round(oos_win_rate, 2),
        }

        print(
            f"  样本内: 信号{signal_count}, 加权收益{avg_return:.3f}%, 胜率{win_rate:.2f}%"
        )
        print(
            f"  样本外: 信号{oos_signal_count}, 加权收益{oos_avg_return:.3f}%, 胜率{oos_win_rate:.2f}%"
        )

    return results


def test_trend_dynamic():
    """测试4：趋势判断 + 动态阈值"""
    print("\n" + "=" * 60)
    print("测试4：趋势判断 + 动态阈值")
    print("=" * 60)

    results = {}
    base_threshold = 30

    for period in TREND_PERIODS:
        for method in ["fixed", "intensity"]:
            name = f"{period}日_{method}"
            print(f"\n测试趋势周期 {period}日, 动态方法 {method}...")

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
                    # 获取历史涨停家数
                    zt_counts = get_zt_counts_history(prev_date, days=period * 2)

                    if len(zt_counts) < period:
                        continue

                    current_zt = zt_counts[-1]
                    trend = calculate_trend(zt_counts, period)

                    # 动态阈值
                    threshold = dynamic_threshold(base_threshold, trend, method)

                    # 阈值过滤
                    if current_zt < threshold:
                        continue

                    signal_count += 1
                    if date >= OOS_START:
                        oos_signal_count += 1

                    # 获取涨停股票并计算收益
                    prev_all = get_all_securities("stock", prev_date).index.tolist()
                    prev_all = [
                        s
                        for s in prev_all
                        if not (
                            s.startswith("68") or s.startswith("4") or s.startswith("8")
                        )
                    ][:200]

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
                    )[:3]

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
                                stock,
                                end_date=date,
                                count=1,
                                fields=["close"],
                                panel=False,
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
            oos_win_rate = (
                oos_wins / len(oos_returns) * 100 if len(oos_returns) > 0 else 0
            )

            results[name] = {
                "signal_count": signal_count,
                "avg_return": round(avg_return, 3),
                "win_rate": round(win_rate, 2),
                "oos_signal_count": oos_signal_count,
                "oos_avg_return": round(oos_avg_return, 3),
                "oos_win_rate": round(oos_win_rate, 2),
            }

            print(
                f"  样本内: 信号{signal_count}, 收益{avg_return:.3f}%, 胜率{win_rate:.2f}%"
            )
            print(
                f"  样本外: 信号{oos_signal_count}, 收益{oos_avg_return:.3f}%, 胜率{oos_win_rate:.2f}%"
            )

    return results


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    all_results = {}

    # 测试1：仅阈值优化
    all_results["threshold_only"] = test_threshold_only()

    # 测试2：过热过滤
    all_results["overheat_filter"] = test_overheat_filter()

    # 测试3：仓位分层
    all_results["position_levels"] = test_position_levels()

    # 测试4：趋势判断 + 动态阈值
    all_results["trend_dynamic"] = test_trend_dynamic()

    # 保存结果
    output_path = "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_v2_test_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    print(f"结果已保存: {output_path}")

    # 打印汇总
    print("\n" + "=" * 80)
    print("汇总结果")
    print("=" * 80)

    print("\n【测试1：阈值优化】")
    for t, r in all_results["threshold_only"].items():
        print(
            f"  阈值{t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
        )

    print("\n【测试2：过热过滤】")
    for t, r in all_results["overheat_filter"].items():
        print(
            f"  过热{t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
        )

    print("\n【测试3：仓位分层】")
    for t, r in all_results["position_levels"].items():
        print(
            f"  {t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
        )

    print("\n【测试4：趋势动态】")
    for t, r in all_results["trend_dynamic"].items():
        print(
            f"  {t}: 样本内{r['avg_return']}%胜率{r['win_rate']}%, 样本外{r['oos_avg_return']}%胜率{r['oos_win_rate']}%"
        )

    print("\n=== 全部测试完成 ===")
