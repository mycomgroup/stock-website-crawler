#!/usr/bin/env python3
"""
RFScore 六策略完整对比 - 5年回测
包含原版3个策略 + 优化版3个策略
回测时间：2021-01-01 至 2026-03-28
"""

from jqdata import *
import pandas as pd
import numpy as np
import json
from datetime import datetime

print("=" * 80)
print("RFScore 六策略完整对比 - 5年回测")
print("回测时间：2021-01-01 至 2026-03-28")
print("=" * 80)

# 季度调仓日期
test_dates = [
    "2021-01-04",
    "2021-04-01",
    "2021-07-01",
    "2021-10-08",
    "2022-01-04",
    "2022-04-01",
    "2022-07-01",
    "2022-10-10",
    "2023-01-03",
    "2023-04-03",
    "2023-07-03",
    "2023-10-09",
    "2024-01-02",
    "2024-04-01",
    "2024-07-01",
    "2024-10-08",
    "2025-01-02",
    "2025-04-01",
    "2025-07-01",
    "2025-10-08",
    "2026-01-05",
    "2026-03-02",
]

print(f"\n调仓时点: {len(test_dates)} 个")


def get_universe(date_str):
    """获取股票池"""
    try:
        hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
        zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
        stocks = list(hs300 | zz500)
        stocks = [s for s in stocks if not s.startswith("688")]

        sec = get_all_securities(types=["stock"], date=date_str)
        sec = sec.loc[sec.index.intersection(stocks)]
        threshold = pd.Timestamp(date_str) - pd.Timedelta(days=180)
        sec = sec[sec["start_date"].apply(lambda x: pd.Timestamp(x) <= threshold)]
        stocks = sec.index.tolist()

        is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()

        paused = get_price(
            stocks, end_date=date_str, count=1, fields="paused", panel=False
        )
        paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
        stocks = paused[paused == 0].index.tolist()

        return stocks
    except Exception as e:
        print(f"  获取股票池失败: {e}")
        return []


def calc_market_state(date_str):
    """计算市场状态（简化版）"""
    try:
        hs300 = get_index_stocks("000300.XSHG", date=date_str)
        prices = get_price(
            hs300, end_date=date_str, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        breadth = float((close.iloc[-1] > close.mean()).mean())

        idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
        trend = float(idx["close"].iloc[-1]) > float(idx["close"].mean())

        return breadth, trend
    except:
        return 0.5, True


def calc_sentiment(date_str):
    """计算情绪指标"""
    try:
        all_stocks = get_all_securities("stock", date=date_str).index.tolist()
        all_stocks = [
            s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
        ]
        sample = all_stocks[:500]

        df = get_price(
            sample,
            end_date=date_str,
            count=1,
            fields=["close", "high_limit", "low_limit"],
            panel=False,
        )
        df = df.dropna()

        hl_count = len(df[df["close"] == df["high_limit"]])
        ll_count = len(df[df["close"] == df["low_limit"]])

        score = 50
        if hl_count > 80:
            score += 20
        elif hl_count > 50:
            score += 10
        elif hl_count < 15:
            score -= 15

        if ll_count > 50:
            score -= 15

        return max(0, min(100, score))
    except:
        return 50


def calc_return(stocks, start_date, end_date):
    """计算收益"""
    if not stocks:
        return 0
    returns = []
    for s in stocks:
        try:
            p1 = get_price(
                s, end_date=start_date, count=1, fields=["close"], panel=False
            )
            p2 = get_price(s, end_date=end_date, count=1, fields=["close"], panel=False)
            if not p1.empty and not p2.empty:
                r = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                    p1["close"].iloc[-1]
                )
                returns.append(r)
        except:
            pass
    return np.mean(returns) if returns else 0


# ========== 策略定义 ==========


def strategy_v2(date_str, hold_num=20):
    """V2原版: PB10% + ROA排序"""
    stocks = get_universe(date_str)
    if not stocks:
        return []

    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["roa"] > 0)]
    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    picks = (
        df[df["pb_group"] <= 1]
        .sort_values(["roa", "pb_ratio"], ascending=[False, True])
        .head(hold_num)["code"]
        .tolist()
    )
    return picks


def strategy_release_v1(date_str, hold_num=15):
    """Release V1: PB10% + 行业上限30%"""
    stocks = get_universe(date_str)
    if not stocks:
        return []

    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["roa"] > 0.5)]
    if df.empty:
        return []

    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    primary = df[df["pb_group"] == 1].sort_values(
        ["roa", "pb_ratio"], ascending=[False, True]
    )

    try:
        industry_raw = get_industry(primary["code"].tolist(), date=date_str)
        industry_map = {
            c: industry_raw.get(c, {}).get("sw_l1", {}).get("industry_name", "Unknown")
            for c in primary["code"].tolist()
        }
    except:
        industry_map = {}

    picks = []
    industry_counts = {}
    limit_count = max(1, int(hold_num * 0.3))
    for code in primary["code"].tolist():
        if len(picks) >= hold_num:
            break
        ind = industry_map.get(code, "Unknown")
        if industry_counts.get(ind, 0) < limit_count:
            picks.append(code)
            industry_counts[ind] = industry_counts.get(ind, 0) + 1
    return picks


def strategy_defensive(date_str, hold_num=10):
    """Defensive: 进攻层 + 防守ETF"""
    stocks = strategy_v2(date_str, hold_num)
    return stocks


def strategy_enhanced(date_str, hold_num=15):
    """增强选股版: 综合评分 + 行业上限"""
    stocks = get_universe(date_str)
    if not stocks:
        return []

    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )
    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[(df["pb_ratio"] > 0) & (df["roa"] > 0)]
    df = df.sort_values("pb_ratio")
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    df["质量分"] = 100
    df["估值分"] = (1 - df["pb_group"] / 10) * 100
    df["成长分"] = np.clip(df["roa"] * 2, 0, 100)
    df["综合分"] = df["质量分"] * 0.5 + df["估值分"] * 0.3 + df["成长分"] * 0.2

    primary = df[df["pb_group"] <= 1].sort_values(
        ["综合分", "pb_ratio"], ascending=[False, True]
    )

    try:
        industry_raw = get_industry(primary["code"].tolist(), date=date_str)
        industry_map = {
            c: industry_raw.get(c, {}).get("sw_l1", {}).get("industry_name", "Unknown")
            for c in primary["code"].tolist()
        }
    except:
        industry_map = {}

    picks = []
    industry_counts = {}
    limit_count = max(1, int(hold_num * 0.3))
    for code in primary["code"].tolist():
        if len(picks) >= hold_num:
            break
        ind = industry_map.get(code, "Unknown")
        if industry_counts.get(ind, 0) < limit_count:
            picks.append(code)
            industry_counts[ind] = industry_counts.get(ind, 0) + 1
    return picks


def strategy_multi_signal(date_str, hold_num=15):
    """多信号风控版: 5信号 + 连续仓位"""
    breadth, trend = calc_market_state(date_str)
    sentiment = calc_sentiment(date_str)

    # 计算仓位
    score = 0
    if breadth > 0.5:
        score += 2
    elif breadth > 0.35:
        score += 1
    elif breadth < 0.2:
        score -= 1

    if trend:
        score += 1

    if sentiment > 60:
        score += 1
    elif sentiment < 30:
        score -= 1

    position_map = {5: 1.0, 4: 0.8, 3: 0.6, 2: 0.4, 1: 0.2, 0: 0.1, -1: 0.0}
    position = position_map.get(score, 0.5)

    actual_hold_num = int(hold_num * position)
    stocks = strategy_release_v1(date_str, actual_hold_num)

    return stocks, position


def strategy_dynamic_hedge(date_str, hold_num=10):
    """动态对冲版: 动态进攻仓位 + 防守ETF"""
    breadth, trend = calc_market_state(date_str)
    sentiment = calc_sentiment(date_str)

    # 计算进攻仓位
    score = 0
    if breadth > 0.5:
        score += 2
    elif breadth > 0.35:
        score += 1
    elif breadth < 0.2:
        score -= 1

    if trend:
        score += 1

    if sentiment > 60:
        score += 1
    elif sentiment < 30:
        score -= 1

    position_map = {5: 0.5, 4: 0.4, 3: 0.3, 2: 0.2, 1: 0.1, 0: 0.05, -1: 0.0}
    offensive_weight = position_map.get(score, 0.25)

    stocks = strategy_enhanced(date_str, hold_num)

    return stocks, offensive_weight


# ========== 运行回测 ==========
results = {
    "V2原版": {"returns": [], "desc": "PB10%+ROA排序"},
    "Release V1": {"returns": [], "desc": "PB10%+行业上限30%"},
    "Defensive原版": {"returns": [], "desc": "进攻+防守ETF"},
    "增强选股版": {"returns": [], "desc": "综合评分+行业上限"},
    "多信号风控版": {"returns": [], "desc": "5信号风控+连续仓位"},
    "动态对冲版": {"returns": [], "desc": "动态对冲+防守ETF"},
}

print("\n开始5年回测...")

for i in range(len(test_dates) - 1):
    date = test_dates[i]
    next_date = test_dates[i + 1]

    print(f"\n[{i + 1}/{len(test_dates) - 1}] {date} -> {next_date}")

    breadth, trend = calc_market_state(date)
    sentiment = calc_sentiment(date)
    print(f"  广度={breadth:.2f}, 趋势={'↑' if trend else '↓'}, 情绪={sentiment:.0f}")

    # 根据市场状态调整持仓数
    if breadth < 0.15 and not trend:
        base_hold = 0
    elif breadth < 0.25 and not trend:
        base_hold = 10
    else:
        base_hold = 20

    # 1. V2原版
    v2_picks = strategy_v2(date, base_hold) if base_hold > 0 else []
    v2_ret = calc_return(v2_picks, date, next_date)
    results["V2原版"]["returns"].append(v2_ret)
    print(f"  V2原版: {len(v2_picks)}只, {v2_ret * 100:.2f}%")

    # 2. Release V1
    r1_hold = int(base_hold * 0.75) if base_hold > 0 else 0
    r1_picks = strategy_release_v1(date, r1_hold) if r1_hold > 0 else []
    r1_ret = calc_return(r1_picks, date, next_date)
    results["Release V1"]["returns"].append(r1_ret)
    print(f"  Release V1: {len(r1_picks)}只, {r1_ret * 100:.2f}%")

    # 3. Defensive原版
    def_weight = 0.5 if base_hold > 0 else 0
    def_picks = strategy_defensive(date, 10)
    def_stock_ret = calc_return(def_picks, date, next_date)
    def_etf_ret = calc_return(
        ["511010.XSHG", "518880.XSHG", "510880.XSHG"], date, next_date
    )
    def_ret = def_stock_ret * def_weight + def_etf_ret * 0.3
    results["Defensive原版"]["returns"].append(def_ret)
    print(
        f"  Defensive: 仓位{def_weight:.0%}, 股票{def_stock_ret * 100:.2f}%, ETF{def_etf_ret * 100:.2f}%, 组合{def_ret * 100:.2f}%"
    )

    # 4. 增强选股版
    enh_hold = int(base_hold * 0.75) if base_hold > 0 else 0
    enh_picks = strategy_enhanced(date, enh_hold) if enh_hold > 0 else []
    enh_ret = calc_return(enh_picks, date, next_date)
    results["增强选股版"]["returns"].append(enh_ret)
    print(f"  增强选股版: {len(enh_picks)}只, {enh_ret * 100:.2f}%")

    # 5. 多信号风控版
    ms_picks, ms_position = strategy_multi_signal(date, 15)
    ms_ret = calc_return(ms_picks, date, next_date) * ms_position
    results["多信号风控版"]["returns"].append(ms_ret)
    print(
        f"  多信号风控: 仓位{ms_position:.0%}, {len(ms_picks)}只, 调整后{ms_ret * 100:.2f}%"
    )

    # 6. 动态对冲版
    dh_picks, dh_weight = strategy_dynamic_hedge(date, 10)
    dh_stock_ret = calc_return(dh_picks, date, next_date)
    dh_etf_ret = calc_return(
        ["511010.XSHG", "518880.XSHG", "510880.XSHG"], date, next_date
    )
    dh_ret = dh_stock_ret * dh_weight + dh_etf_ret * 0.3
    results["动态对冲版"]["returns"].append(dh_ret)
    print(
        f"  动态对冲: 进攻{dh_weight:.0%}, 股票{dh_stock_ret * 100:.2f}%, ETF{dh_etf_ret * 100:.2f}%, 组合{dh_ret * 100:.2f}%"
    )


# ========== 汇总结果 ==========
print("\n" + "=" * 80)
print("5年回测结果汇总")
print("=" * 80)

summary = []
for name, data in results.items():
    returns = data["returns"]
    if not returns:
        continue

    total = np.sum(returns) * 100
    avg = np.mean(returns) * 100
    std = np.std(returns) * 100
    sharpe = (
        (np.mean(returns) / np.std(returns) * np.sqrt(4)) if np.std(returns) > 0 else 0
    )
    win = len([r for r in returns if r > 0]) / len(returns) * 100 if returns else 0
    max_dd = min(returns) * 100 if returns else 0

    summary.append(
        {
            "strategy": name,
            "desc": data["desc"],
            "total_return": round(total, 2),
            "avg_quarterly": round(avg, 2),
            "std": round(std, 2),
            "sharpe": round(sharpe, 2),
            "win_rate": round(win, 1),
            "max_drawdown": round(max_dd, 2),
        }
    )

    print(f"\n{name} ({data['desc']})")
    print(f"  累计收益: {total:.2f}%")
    print(f"  季度平均: {avg:.2f}%")
    print(f"  收益波动: {std:.2f}%")
    print(f"  夏普比率: {sharpe:.2f}")
    print(f"  胜率: {win:.1f}%")
    print(f"  最差季度: {max_dd:.2f}%")

print("\n" + "-" * 80)
print(f"{'策略':<20} {'累计收益':>10} {'季度平均':>10} {'夏普':>8} {'胜率':>8}")
print("-" * 80)
for s in summary:
    print(
        f"{s['strategy']:<20} {s['total_return']:>9.2f}% {s['avg_quarterly']:>9.2f}% {s['sharpe']:>8.2f} {s['win_rate']:>7.1f}%"
    )

# 保存结果
result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_5year_comparison.json"
)
with open(result_file, "w") as f:
    json.dump(
        {
            "test_period": f"{test_dates[0]} to {test_dates[-1]}",
            "test_dates": test_dates,
            "summary": summary,
            "quarterly_returns": {
                k: [r * 100 for r in v["returns"]] for k, v in results.items()
            },
        },
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"\n✓ 结果已保存: {result_file}")

# 最终结论
print("\n" + "=" * 80)
print("最终结论")
print("=" * 80)

best_return = max(summary, key=lambda x: x["total_return"])
best_sharpe = max(summary, key=lambda x: x["sharpe"])
best_win = max(summary, key=lambda x: x["win_rate"])

print(f"\n收益最高: {best_return['strategy']} ({best_return['total_return']:.2f}%)")
print(f"夏普最优: {best_sharpe['strategy']} (夏普{best_sharpe['sharpe']:.2f})")
print(f"胜率最高: {best_win['strategy']} ({best_win['win_rate']:.1f}%)")

print("\n=== 完成! ===")
print("=" * 80)
