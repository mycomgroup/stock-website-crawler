#!/usr/bin/env python3
"""
RFScore 六策略对比验证

对比版本：
原版：
1. rfscore7_pb10_final_v2.py (V2)
2. rfscore7_pb10_release_v1.py (Release V1)
3. rfscore_defensive_combined.py (Defensive)

优化版：
4. rfscore7_pb10_enhanced_selection.py (增强选股版)
5. rfscore7_pb10_multi_signal_risk_control.py (多信号风控版)
6. rfscore_defensive_dynamic_hedge.py (动态对冲版)

回测时间：2025-01-01 至 2026-03-28
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 70)
print("RFScore 六策略对比验证")
print("=" * 70)


def get_universe(date_str):
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
    paused = get_price(stocks, end_date=date_str, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()
    return stocks


def calc_breadth(date_str):
    hs300 = get_index_stocks("000300.XSHG", date=date_str)
    prices = get_price(
        hs300, end_date=date_str, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    return float((close.iloc[-1] > close.mean()).mean())


def calc_trend(date_str):
    idx = get_price("000300.XSHG", end_date=date_str, count=20, fields=["close"])
    return float(idx["close"].iloc[-1]) > float(idx["close"].mean())


def calc_sentiment(date_str):
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


def calc_north_flow(date_str):
    try:
        df = get_money_flow(
            ["北向资金"], end_date=date_str, count=5, fields=["net_amount"]
        )
        if df is not None and not df.empty:
            return float(df["net_amount"].sum())
    except:
        pass
    return 0


def calc_down_days(date_str):
    idx = get_price("000300.XSHG", end_date=date_str, count=10, fields=["close"])
    closes = idx["close"].values
    down_count = 0
    for i in range(len(closes) - 1, 0, -1):
        if closes[i] < closes[i - 1]:
            down_count += 1
        else:
            break
    return down_count


def calc_market_state(date_str):
    return {
        "breadth": calc_breadth(date_str),
        "trend": calc_trend(date_str),
        "sentiment": calc_sentiment(date_str),
        "north_flow": calc_north_flow(date_str),
        "down_days": calc_down_days(date_str),
    }


def select_stocks_v2(date_str, hold_num):
    """V2: RFScore7 + PB10% + Score>=6补位"""
    stocks = get_universe(date_str)
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
    primary = df[df["pb_group"] <= 1].sort_values(
        ["roa", "pb_ratio"], ascending=[False, True]
    )
    picks = primary["code"].head(hold_num).tolist()
    if len(picks) < hold_num:
        secondary = df[df["pb_group"] <= 2].sort_values(
            ["roa", "pb_ratio"], ascending=[False, True]
        )
        for code in secondary["code"].tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    return picks[:hold_num]


def select_stocks_release_v1(date_str, hold_num):
    """Release V1: RFScore7 + PB10% + 行业上限"""
    stocks = get_universe(date_str)
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
    industry_raw = get_industry(primary["code"].tolist(), date=date_str)
    industry_map = {
        c: industry_raw.get(c, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        for c in primary["code"].tolist()
    }
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


def select_stocks_enhanced(date_str, hold_num):
    """增强选股版: 综合评分 + 行业上限"""
    stocks = get_universe(date_str)
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
    industry_raw = get_industry(primary["code"].tolist(), date=date_str)
    industry_map = {
        c: industry_raw.get(c, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        for c in primary["code"].tolist()
    }
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


def calc_position_multi_signal(state):
    """多信号风控: 5信号计算仓位"""
    score = 0
    if state["breadth"] > 0.5:
        score += 2
    elif state["breadth"] > 0.35:
        score += 1
    elif state["breadth"] < 0.2:
        score -= 1
    if state["trend"]:
        score += 1
    if state["sentiment"] > 60:
        score += 1
    elif state["sentiment"] < 30:
        score -= 1
    if state["north_flow"] > 50e8:
        score += 1
    elif state["north_flow"] < -50e8:
        score -= 1
    if state["down_days"] >= 5:
        score -= 2
    position_map = {5: 1.0, 4: 0.8, 3: 0.6, 2: 0.4, 1: 0.2, 0: 0.1, -1: 0.0, -2: 0.0}
    return position_map.get(score, 0.5)


def calc_return(stocks, start, end):
    if not stocks:
        return 0
    returns = []
    for s in stocks:
        try:
            p1 = get_price(s, end_date=start, count=1, fields="close", panel=False)
            p2 = get_price(s, end_date=end, count=1, fields="close", panel=False)
            if not p1.empty and not p2.empty:
                r = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                    p1["close"].iloc[-1]
                )
                returns.append(r)
        except:
            pass
    return np.mean(returns) if returns else 0


dates = [
    "2025-01-02",
    "2025-02-05",
    "2025-03-03",
    "2025-04-01",
    "2025-05-06",
    "2026-01-05",
    "2026-02-05",
    "2026-03-02",
]
print(f"\n测试日期: {dates}")
print(f"测试月份数: {len(dates)}")

results = {
    "V2_原版": {"returns": [], "desc": "RFScore7+PB10%+Score6补位"},
    "Release_V1_原版": {"returns": [], "desc": "RFScore7+PB10%+行业上限+无补位"},
    "Defensive_原版": {"returns": [], "desc": "50%进攻+30%ETF+20%现金"},
    "Enhanced_Selection_优化": {"returns": [], "desc": "综合评分+行业上限+尾盘调仓"},
    "Multi_Signal_优化": {"returns": [], "desc": "5信号风控+连续仓位"},
    "Dynamic_Hedge_优化": {"returns": [], "desc": "动态防守层+风控增强"},
}

for i, date in enumerate(dates):
    print(f"\n{'=' * 70}")
    print(f"[{i + 1}/{len(dates)}] {date}")
    print("=" * 70)

    state = calc_market_state(date)
    print(
        f"市场状态: 广度={state['breadth']:.3f}, 趋势={'↑' if state['trend'] else '↓'}, 情绪={state['sentiment']:.0f}, 北向={state['north_flow'] / 1e8:.1f}亿, 连跌={state['down_days']}天"
    )

    next_dates = get_trade_days(date, "2026-03-28")
    next_date = str(next_dates[20]) if len(next_dates) > 20 else str(next_dates[-1])

    # 1. V2 原版
    v2_hold = (
        20
        if state["breadth"] >= 0.25 or state["trend"]
        else (10 if state["breadth"] >= 0.15 else 0)
    )
    v2_picks = select_stocks_v2(date, v2_hold) if v2_hold > 0 else []
    v2_ret = calc_return(v2_picks, date, next_date)
    results["V2_原版"]["returns"].append(v2_ret)
    print(f"V2原版: 持仓={len(v2_picks)}, 收益={v2_ret * 100:.2f}%")

    # 2. Release V1 原版
    if state["breadth"] < 0.15:
        r1_hold = 0
    elif state["breadth"] < 0.25:
        r1_hold = 10
    elif state["breadth"] < 0.35 and not state["trend"]:
        r1_hold = 12
    else:
        r1_hold = 15
    r1_picks = select_stocks_release_v1(date, r1_hold) if r1_hold > 0 else []
    r1_ret = calc_return(r1_picks, date, next_date)
    results["Release_V1_原版"]["returns"].append(r1_ret)
    print(f"Release V1原版: 持仓={len(r1_picks)}, 收益={r1_ret * 100:.2f}%")

    # 3. Defensive 原版
    def_weight = (
        0.5
        if state["breadth"] >= 0.25 or state["trend"]
        else (0.25 if state["breadth"] >= 0.15 else 0)
    )
    def_picks = select_stocks_v2(date, 10)
    def_stock_ret = calc_return(def_picks, date, next_date)
    def_etf_ret = calc_return(
        ["511010.XSHG", "518880.XSHG", "510880.XSHG"], date, next_date
    )
    def_ret = def_stock_ret * def_weight + def_etf_ret * 0.3
    results["Defensive_原版"]["returns"].append(def_ret)
    print(
        f"Defensive原版: 进攻仓位={def_weight:.0%}, 股票={def_stock_ret * 100:.2f}%, ETF={def_etf_ret * 100:.2f}%, 组合={def_ret * 100:.2f}%"
    )

    # 4. Enhanced Selection 优化版
    enh_hold = (
        20
        if state["breadth"] >= 0.25 or state["trend"]
        else (10 if state["breadth"] >= 0.15 else 0)
    )
    enh_picks = select_stocks_enhanced(date, enh_hold) if enh_hold > 0 else []
    enh_ret = calc_return(enh_picks, date, next_date)
    results["Enhanced_Selection_优化"]["returns"].append(enh_ret)
    print(f"增强选股版: 持仓={len(enh_picks)}, 收益={enh_ret * 100:.2f}%")

    # 5. Multi Signal 优化版
    ms_position = calc_position_multi_signal(state)
    ms_hold = int(15 * ms_position)
    ms_picks = select_stocks_release_v1(date, ms_hold) if ms_hold > 0 else []
    ms_ret = calc_return(ms_picks, date, next_date) * ms_position
    results["Multi_Signal_优化"]["returns"].append(ms_ret)
    print(
        f"多信号风控版: 仓位={ms_position:.0%}, 持仓={len(ms_picks)}, 收益={ms_ret * 100:.2f}%"
    )

    # 6. Dynamic Hedge 优化版
    dh_position = calc_position_multi_signal(state) * 0.5
    dh_hold = int(15 * dh_position / 0.5)
    dh_picks = select_stocks_enhanced(date, dh_hold) if dh_hold > 0 else []
    dh_stock_ret = calc_return(dh_picks, date, next_date)
    dh_etf_ret = calc_return(
        ["511010.XSHG", "518880.XSHG", "510880.XSHG"], date, next_date
    )
    dh_ret = dh_stock_ret * dh_position + dh_etf_ret * 0.3
    results["Dynamic_Hedge_优化"]["returns"].append(dh_ret)
    print(
        f"动态对冲版: 进攻仓位={dh_position:.0%}, 股票={dh_stock_ret * 100:.2f}%, ETF={dh_etf_ret * 100:.2f}%, 组合={dh_ret * 100:.2f}%"
    )


print("\n" + "=" * 70)
print("六策略对比结果")
print("=" * 70)

summary = []
for name, data in results.items():
    returns = data["returns"]
    total = np.sum(returns) * 100
    avg = np.mean(returns) * 100
    std = np.std(returns) * 100
    sharpe = (
        np.mean(returns) / np.std(returns) * np.sqrt(12) if np.std(returns) > 0 else 0
    )
    win = len([r for r in returns if r > 0]) / len(returns) * 100 if returns else 0
    summary.append(
        {
            "name": name,
            "desc": data["desc"],
            "total_return": round(total, 2),
            "avg_monthly": round(avg, 2),
            "std": round(std, 2),
            "sharpe": round(sharpe, 2),
            "win_rate": round(win, 1),
        }
    )
    print(f"\n{name} ({data['desc']})")
    print(f"  累计收益: {total:.2f}%")
    print(f"  月均收益: {avg:.2f}%")
    print(f"  收益标准差: {std:.2f}%")
    print(f"  夏普比率: {sharpe:.2f}")
    print(f"  胜率: {win:.1f}%")

print("\n" + "-" * 70)
print(f"{'策略':<30} {'累计':>8} {'月均':>8} {'夏普':>8} {'胜率':>8}")
print("-" * 70)
for s in summary:
    print(
        f"{s['name']:<30} {s['total_return']:>7.2f}% {s['avg_monthly']:>7.2f}% {s['sharpe']:>8.2f} {s['win_rate']:>7.1f}%"
    )

# 对比分析
print("\n" + "=" * 70)
print("优化效果对比")
print("=" * 70)

pairs = [
    ("V2_原版", "Enhanced_Selection_优化", "选股优化"),
    ("Release_V1_原版", "Multi_Signal_优化", "风控增强"),
    ("Defensive_原版", "Dynamic_Hedge_优化", "对冲优化"),
]

for orig, opt, label in pairs:
    orig_data = next(s for s in summary if s["name"] == orig)
    opt_data = next(s for s in summary if s["name"] == opt)
    print(f"\n{label}:")
    print(
        f"  原版: 收益={orig_data['total_return']:.2f}%, 夏普={orig_data['sharpe']:.2f}"
    )
    print(
        f"  优化: 收益={opt_data['total_return']:.2f}%, 夏普={opt_data['sharpe']:.2f}"
    )
    print(
        f"  提升: 收益+{opt_data['total_return'] - orig_data['total_return']:.2f}%, 夏普+{opt_data['sharpe'] - orig_data['sharpe']:.2f}"
    )

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_six_strategies_comparison.json"
with open(result_file, "w") as f:
    json.dump(
        {
            "test_period": "2025-01-01 to 2026-03-28",
            "test_dates": dates,
            "summary": summary,
            "monthly_returns": {
                k: [r * 100 for r in v["returns"]] for k, v in results.items()
            },
        },
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"\n结果已保存: {result_file}")
print("\n" + "=" * 70)
print("验证完成!")
print("=" * 70)
