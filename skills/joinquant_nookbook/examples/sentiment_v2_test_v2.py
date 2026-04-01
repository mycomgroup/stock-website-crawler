#!/usr/bin/env python3
"""
情绪层v2完善测试 - v2版本
使用连续交易日，修复测试逻辑
"""

from jqdata import *
import numpy as np
import json

print("=" * 80)
print("情绪层v2完善测试 - v2版本")
print("=" * 80)

# 获取连续交易日
trade_days = get_trade_days("2024-01-01", "2024-03-31")
TEST_DATES = [str(d) for d in trade_days[:40]]  # 取40个交易日

OOS_START = "2024-01-01"
STOCK_LIMIT = 300

print(f"\n测试日期数: {len(TEST_DATES)}")
print(f"测试范围: {TEST_DATES[0]} ~ {TEST_DATES[-1]}")


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


def get_zt_stocks(date, limit=3):
    """获取涨停股票列表"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ][:200]

        df = get_price(
            all_stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        zt_stocks = list(df[df["close"] == df["high_limit"]]["code"])[:limit]
        return zt_stocks
    except:
        return []


def test_strategy(threshold_low=30, threshold_high=999, position_levels=None):
    """测试策略"""
    signal_count = 0
    returns = []
    wins = 0

    for i in range(len(TEST_DATES) - 1):
        prev_date = TEST_DATES[i]
        date = TEST_DATES[i + 1]

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

            # 获取涨停股票
            zt_stocks = get_zt_stocks(prev_date, limit=2)

            if len(zt_stocks) == 0:
                continue

            signal_count += 1

            # 计算收益
            day_returns = []
            for stock in zt_stocks:
                try:
                    # 获取次日开盘价和收盘价
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
                        high_limit = buy_df.iloc[0]["high_limit"]

                        # 检查是否可以买入（不是一字涨停）
                        if buy_open < high_limit and buy_open > 0:
                            ret = (sell_close / buy_open - 1) * 100
                            day_returns.append(ret)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns) * position_ratio
                returns.append(avg_ret)

                if avg_ret > 0:
                    wins += 1

        except Exception as e:
            continue

    avg_return = np.mean(returns) if len(returns) > 0 else 0
    win_rate = wins / len(returns) * 100 if len(returns) > 0 else 0

    return {
        "signal_count": signal_count,
        "avg_return": round(avg_return, 3),
        "win_rate": round(win_rate, 2),
        "total_trades": len(returns),
    }


# ============================================================
# 测试1：阈值优化
# ============================================================
print("\n" + "=" * 60)
print("测试1：阈值优化")
print("=" * 60)

threshold_results = {}
for threshold in [0, 20, 30, 40, 50, 60, 80, 100]:
    print(f"\n测试阈值 {threshold}...")
    result = test_strategy(threshold_low=threshold)
    threshold_results[threshold] = result
    print(
        f"  信号: {result['signal_count']}, 收益: {result['avg_return']}%, 胜率: {result['win_rate']}%, 交易: {result['total_trades']}"
    )

# ============================================================
# 测试2：过热过滤
# ============================================================
print("\n" + "=" * 60)
print("测试2：过热过滤")
print("=" * 60)

overheat_results = {}
for overheat in [80, 100, 120, 999]:  # 999表示无过热过滤
    print(f"\n测试过热阈值 {overheat}...")
    result = test_strategy(threshold_low=30, threshold_high=overheat)
    overheat_results[overheat] = result
    print(
        f"  信号: {result['signal_count']}, 收益: {result['avg_return']}%, 胜率: {result['win_rate']}%, 交易: {result['total_trades']}"
    )

# ============================================================
# 测试3：仓位分层
# ============================================================
print("\n" + "=" * 60)
print("测试3：仓位分层")
print("=" * 60)

# 3档仓位
position_3_levels = [(100, 0.0), (50, 1.0), (30, 0.5), (0, 0.0)]
# 5档仓位
position_5_levels = [(100, 0.0), (80, 1.0), (50, 0.8), (30, 0.5), (15, 0.25), (0, 0.0)]
# 硬开关（基准）
position_hard = [(30, 1.0), (0, 0.0)]

position_results = {}

print("\n测试硬开关（基准）...")
result = test_strategy(threshold_low=0, position_levels=position_hard)
position_results["硬开关"] = result
print(
    f"  信号: {result['signal_count']}, 加权收益: {result['avg_return']}%, 胜率: {result['win_rate']}%, 交易: {result['total_trades']}"
)

print("\n测试3档仓位...")
result = test_strategy(threshold_low=0, position_levels=position_3_levels)
position_results["3档"] = result
print(
    f"  信号: {result['signal_count']}, 加权收益: {result['avg_return']}%, 胜率: {result['win_rate']}%, 交易: {result['total_trades']}"
)

print("\n测试5档仓位...")
result = test_strategy(threshold_low=0, position_levels=position_5_levels)
position_results["5档"] = result
print(
    f"  信号: {result['signal_count']}, 加权收益: {result['avg_return']}%, 胜率: {result['win_rate']}%, 交易: {result['total_trades']}"
)

# ============================================================
# 汇总结果
# ============================================================
print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)

print("\n【测试1：阈值优化】")
print("阈值 | 信号数 | 收益% | 胜率% | 交易次数")
print("-" * 40)
for t in sorted(threshold_results.keys()):
    r = threshold_results[t]
    print(
        f"  {t:3d} | {r['signal_count']:6d} | {r['avg_return']:6.3f} | {r['win_rate']:5.1f} | {r['total_trades']:6d}"
    )

print("\n【测试2：过热过滤】")
print("过热线 | 信号数 | 收益% | 胜率% | 交易次数")
print("-" * 40)
for t in sorted(overheat_results.keys()):
    r = overheat_results[t]
    label = f"{t}" if t < 999 else "无限制"
    print(
        f"  {label:4s} | {r['signal_count']:6d} | {r['avg_return']:6.3f} | {r['win_rate']:5.1f} | {r['total_trades']:6d}"
    )

print("\n【测试3：仓位分层】")
print("方案 | 信号数 | 加权收益% | 胜率% | 交易次数")
print("-" * 40)
for t, r in position_results.items():
    print(
        f"  {t:4s} | {r['signal_count']:6d} | {r['avg_return']:9.3f} | {r['win_rate']:5.1f} | {r['total_trades']:6d}"
    )

# 保存结果
all_results = {
    "threshold": threshold_results,
    "overheat": overheat_results,
    "position": position_results,
    "test_config": {
        "dates": TEST_DATES,
        "stock_limit": STOCK_LIMIT,
    },
}

output_path = "/Users/fengzhi/Downloads/git/testlixingren/output/sentiment_v2_test_results_v2.json"
with open(output_path, "w") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存: {output_path}")
print("\n=== 测试完成 ===")
