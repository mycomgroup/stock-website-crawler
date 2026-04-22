"""
小市值策略示例 - 使用 StrategyRegimeAnalyzer 框架

使用方法:
    cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook
    node run-skill.js --notebook-url <url> --cell-source "$(cat example_small_cap.py)" --timeout-ms 600000
"""

# ============================================================
# 小市值三分支验证 - 使用通用框架
# ============================================================

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# 配置
# ============================================================

CONFIG = {
    "start": "2020-01-01",
    "end": "2026-03-28",
    "freq": "quarterly",
    "cost": 0.003,
    "benchmarks": ["399101.XSHE", "000300.XSHG"],  # 中证2000, 沪深300
    "benchmark_names": {
        "399101.XSHE": "中证2000",
        "000300.XSHG": "沪深300",
    },
    "recent_since": "2024-01-01",
    "risk_free_rate": 0.02,
    "parallel": True,
    "max_workers": 4,
}

# 市场状态阈值 (季度)
REGIME_THRESHOLDS = {
    "bull": 0.05,  # 牛市: 季涨>5%
    "mild_down": -0.05,  # 温和下跌: 0~-5%
}

# ============================================================
# 工具函数
# ============================================================


def get_period_dates(start, end, freq="quarterly"):
    """获取调仓日期"""
    days = get_trade_days(start, end)
    result, last_period = [], None

    for d in days:
        if freq == "monthly":
            period = d.month
        elif freq == "quarterly":
            period = (d.month - 1) // 3
        else:
            raise ValueError(f"Unsupported freq: {freq}")

        if period != last_period:
            result.append(d)
            last_period = period

    return result


def filter_basic(stocks, date):
    """基础过滤"""
    try:
        is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
    except:
        pass
    return stocks


# ============================================================
# 策略定义
# ============================================================


def select_guojiu(date, n=10):
    """国九条筛选型"""
    q = (
        query(
            valuation.code,
            valuation.market_cap,
            valuation.pe_ratio,
            indicator.inc_net_profit_year_on_year,
        )
        .filter(
            valuation.market_cap > 10,
            valuation.market_cap < 50,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 40,
            indicator.inc_net_profit_year_on_year > 0,
        )
        .order_by(valuation.pe_ratio.asc())
        .limit(n * 3)
    )

    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)

    # 流动性过滤
    try:
        money = get_price(stks, end_date=date, count=20, fields=["money"], panel=False)
        avg_money = money.groupby("code")["money"].mean()
        liquid = avg_money[avg_money > 3e7].index.tolist()
        stks = [s for s in stks if s in liquid]
    except:
        pass

    return stks[:n]


def select_micro_cap(date, n=10):
    """微盘再平衡型"""
    q = (
        query(valuation.code, valuation.market_cap, valuation.pb_ratio)
        .filter(
            valuation.market_cap > 5,
            valuation.market_cap < 30,
            valuation.pb_ratio > 0,
            valuation.pb_ratio < 3,
        )
        .order_by(valuation.market_cap.asc())
        .limit(n * 3)
    )

    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)

    # 流动性过滤
    try:
        money = get_price(stks, end_date=date, count=20, fields=["money"], panel=False)
        avg_money = money.groupby("code")["money"].mean()
        liquid = avg_money[avg_money > 1e7].index.tolist()
        stks = [s for s in stks if s in liquid]
    except:
        pass

    return stks[:n]


def select_growth_small(date, n=10):
    """成长小盘型"""
    q = (
        query(
            valuation.code,
            valuation.market_cap,
            valuation.pe_ratio,
            indicator.inc_net_profit_year_on_year,
            indicator.roe,
        )
        .filter(
            valuation.market_cap > 30,
            valuation.market_cap < 150,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 50,
            indicator.inc_net_profit_year_on_year > 20,
            indicator.roe > 10,
        )
        .order_by(indicator.inc_net_profit_year_on_year.desc())
        .limit(n * 3)
    )

    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)
    return stks[:n]


# ============================================================
# 回测引擎
# ============================================================


def run_strategy(select_fn, label, dates, cost=0.003):
    """执行单个策略回测"""
    results = []
    prev_stocks = []

    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i + 1])

        try:
            selected = select_fn(d_str, 10)

            if not selected or len(selected) == 0:
                results.append({"date": d, "ret": 0, "turnover": 0})
                continue

            p0 = get_price(
                selected, end_date=d_str, count=1, fields=["close"], panel=False
            )
            p1 = get_price(
                selected, end_date=next_d_str, count=1, fields=["close"], panel=False
            )

            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]

            gross = ((p1 / p0) - 1).dropna().mean()
            turnover = len(set(selected) - set(prev_stocks)) / max(len(selected), 1)
            net_ret = gross - turnover * cost * 2

            results.append({"date": d, "ret": net_ret, "turnover": turnover})
            prev_stocks = selected

        except Exception as e:
            results.append({"date": d, "ret": 0, "turnover": 0})

    df = pd.DataFrame(results)
    df["date"] = pd.to_datetime(df["date"])
    return df


def run_benchmark(index_code, dates):
    """获取基准收益"""
    results = []

    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i + 1])

        try:
            p0 = get_price(
                index_code, end_date=d_str, count=1, fields=["close"], panel=False
            )["close"].iloc[-1]
            p1 = get_price(
                index_code, end_date=next_d_str, count=1, fields=["close"], panel=False
            )["close"].iloc[-1]
            ret = (p1 / p0) - 1
            results.append({"date": d, "ret": ret})
        except:
            results.append({"date": d, "ret": 0})

    df = pd.DataFrame(results)
    df["date"] = pd.to_datetime(df["date"])
    return df


# ============================================================
# 分析模块
# ============================================================


def classify_market(ret, thresholds):
    """市场状态分类"""
    if pd.isna(ret):
        return "未知"
    if ret > thresholds["bull"]:
        return f"牛市(涨>{thresholds['bull']:.0%})"
    elif ret > 0:
        return f"温和上涨(0~{thresholds['bull']:.0%})"
    elif ret > thresholds["mild_down"]:
        return f"温和下跌({thresholds['mild_down']:.0%}~0)"
    else:
        return f"熊市(跌<{thresholds['mild_down']:.0%})"


def calc_risk_metrics(returns, risk_free_rate=0.02, periods_per_year=4):
    """计算风险指标"""
    if len(returns) < 2:
        return {}

    cum_ret = (1 + returns).prod() - 1
    years = len(returns) / periods_per_year
    ann_ret = (1 + cum_ret) ** (1 / years) - 1 if years > 0 else 0
    ann_vol = returns.std() * np.sqrt(periods_per_year)
    sharpe = (ann_ret - risk_free_rate) / ann_vol if ann_vol > 0 else 0

    # 最大回撤
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    max_dd = abs(drawdown.min())

    # Calmar
    calmar = ann_ret / max_dd if max_dd > 0 else 0

    # 胜率
    win_rate = (returns > 0).sum() / len(returns)

    return {
        "累计收益": cum_ret,
        "年化收益": ann_ret,
        "年化波动": ann_vol,
        "夏普比率": sharpe,
        "最大回撤": max_dd,
        "Calmar比率": calmar,
        "胜率": win_rate,
    }


# ============================================================
# 主程序
# ============================================================

print("=" * 70)
print("小市值三分支验证 - 通用框架版本")
print("=" * 70)

# 获取调仓日期
dates = get_period_dates(CONFIG["start"], CONFIG["end"], CONFIG["freq"])
print(f"\n调仓次数: {len(dates) - 1} ({CONFIG['freq']}调仓)")

# 执行策略回测
print("\n执行策略回测...")
strategies = {
    "国九条筛选型": select_guojiu,
    "微盘再平衡型": select_micro_cap,
    "成长小盘型": select_growth_small,
}

strategy_results = {}
for name, fn in strategies.items():
    print(f"  {name}...")
    strategy_results[name] = run_strategy(fn, name, dates, CONFIG["cost"])

# 获取基准数据
print("\n获取基准数据...")
benchmark_results = {}
for code in CONFIG["benchmarks"]:
    bench_name = CONFIG["benchmark_names"].get(code, code)
    print(f"  {bench_name}...")
    benchmark_results[bench_name] = run_benchmark(code, dates)

# 合并数据
print("\n合并数据...")
merged = strategy_results[list(strategy_results.keys())[0]][["date"]].copy()
for name, df in strategy_results.items():
    merged = merged.merge(df[["date", "ret"]].rename(columns={"ret": name}), on="date")
for name, df in benchmark_results.items():
    merged = merged.merge(df[["date", "ret"]].rename(columns={"ret": name}), on="date")

# ============================================================
# 分析1: 年度收益
# ============================================================

print("\n" + "=" * 70)
print("【分析1: 按年度收益统计】")
print("=" * 70)

merged["year"] = merged["date"].dt.year
yearly = (
    merged.groupby("year")
    .agg(
        {
            col: lambda x: (1 + x.dropna()).prod() - 1 if len(x.dropna()) > 0 else 0
            for col in list(strategies.keys()) + list(benchmark_results.keys())
        }
    )
    .round(4)
)

print(yearly.to_string())

# ============================================================
# 分析2: 风险指标
# ============================================================

print("\n" + "=" * 70)
print("【分析2: 风险指标】")
print("=" * 70)

for name in strategies.keys():
    risk = calc_risk_metrics(merged[name], CONFIG["risk_free_rate"], 4)
    print(f"\n{name}:")
    for k, v in risk.items():
        if "比率" in k or "胜率" in k:
            print(f"  {k}: {v:.2f}")
        else:
            print(f"  {k}: {v:.1%}")

# ============================================================
# 分析3: 市场状态
# ============================================================

print("\n" + "=" * 70)
print("【分析3: 按市场状态分类】")
print("=" * 70)

main_benchmark = list(benchmark_results.keys())[0]
merged["regime"] = merged[main_benchmark].apply(
    lambda x: classify_market(x, REGIME_THRESHOLDS)
)

regime_order = [
    f"牛市(涨>{REGIME_THRESHOLDS['bull']:.0%})",
    f"温和上涨(0~{REGIME_THRESHOLDS['bull']:.0%})",
    f"温和下跌({REGIME_THRESHOLDS['mild_down']:.0%}~0)",
    f"熊市(跌<{REGIME_THRESHOLDS['mild_down']:.0%})",
]

for regime in regime_order:
    subset = merged[merged["regime"] == regime]
    if len(subset) == 0:
        continue
    print(f"\n{regime} (共{len(subset)}个季度):")
    for name in strategies.keys():
        mean_ret = subset[name].mean()
        cum_ret = (1 + subset[name]).prod() - 1
        print(f"  {name}: 季均{mean_ret:.2%} | 累计{cum_ret:.1%}")

# ============================================================
# 分析4: 择时效果
# ============================================================

print("\n" + "=" * 70)
print("【分析4: 择时效果对比】")
print("=" * 70)

merged["benchmark_lag1"] = merged[main_benchmark].shift(1)
total_q = len(merged)

for name in strategies.keys():
    print(f"\n{name}:")

    # 不择时
    all_rets = merged[name]
    cum_ret = (1 + all_rets).prod() - 1
    ann_ret = calc_risk_metrics(all_rets, CONFIG["risk_free_rate"], 4).get(
        "年化收益", 0
    )
    print(f"  不择时: 累计{cum_ret:.1%} | 年化{ann_ret:.1%} | 100%时间")

    # 前季>0%做
    mask = merged["benchmark_lag1"] > 0
    if mask.sum() > 0:
        timing_rets = merged.loc[mask, name]
        cum_ret = (1 + timing_rets).prod() - 1
        ann_ret = calc_risk_metrics(timing_rets, CONFIG["risk_free_rate"], 4).get(
            "年化收益", 0
        )
        pct = mask.sum() / total_q
        print(f"  前季>0%做: 累计{cum_ret:.1%} | 年化{ann_ret:.1%} | {pct:.0%}时间")

# ============================================================
# 分析5: 近期表现
# ============================================================

print("\n" + "=" * 70)
print("【分析5: 近期表现】")
print("=" * 70)

recent = merged[merged["date"] >= CONFIG["recent_since"]]
print(f"\n{CONFIG['recent_since']} 至今 ({len(recent)}个季度):")

for name in list(strategies.keys()) + list(benchmark_results.keys()):
    cum_ret = (1 + recent[name]).prod() - 1
    mean_ret = recent[name].mean()
    print(f"  {name}: 累计{cum_ret:.1%} | 季均{mean_ret:.2%}")

# ============================================================
# 分析6: 适合条件
# ============================================================

print("\n" + "=" * 70)
print("【分析6: 适合条件总结】")
print("=" * 70)

for name in strategies.keys():
    positive = merged[merged[name] > 0]
    negative = merged[merged[name] < 0]

    print(f"\n{name}:")
    print(f"  正收益期 ({len(positive)}个, {len(positive) / len(merged):.0%}):")
    print(f"    {main_benchmark}当季均值: {positive[main_benchmark].mean():.2%}")
    print(f"    {main_benchmark}前季均值: {positive['benchmark_lag1'].mean():.2%}")
    print(f"  负收益期 ({len(negative)}个, {len(negative) / len(merged):.0%}):")
    print(f"    {main_benchmark}当季均值: {negative[main_benchmark].mean():.2%}")
    print(f"    {main_benchmark}前季均值: {negative['benchmark_lag1'].mean():.2%}")

# ============================================================
# 结论
# ============================================================

print("\n" + "=" * 70)
print("【结论】")
print("=" * 70)

# 找出最佳策略
strategy_ann_returns = {}
for name in strategies.keys():
    risk = calc_risk_metrics(merged[name], CONFIG["risk_free_rate"], 4)
    strategy_ann_returns[name] = risk.get("年化收益", 0)

best = max(strategy_ann_returns, key=strategy_ann_returns.get)
worst = min(strategy_ann_returns, key=strategy_ann_returns.get)

print(f"\n最佳策略: {best} (年化{strategy_ann_returns[best]:.1%})")
print(f"最差策略: {worst} (年化{strategy_ann_returns[worst]:.1%})")

print("\n" + "=" * 70)
print("验证完成!")
print("=" * 70)
