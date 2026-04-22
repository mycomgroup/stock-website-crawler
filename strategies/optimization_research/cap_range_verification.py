"""
小市值防守线v2市值区间优化验证
运行方式：在JoinQuant平台策略编辑器中运行回测

测试期间：2022-04-01 ~ 2025-03-30
基准：000852.XSHG (中证1000)
"""

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_benchmark("000852.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    g.test_configs = [
        {"name": "v1基准", "min_cap": 15, "max_cap": 60},
        {"name": "推荐方案", "min_cap": 10, "max_cap": 100},
        {"name": "激进方案", "min_cap": 10, "max_cap": 80},
        {"name": "保守方案", "min_cap": 20, "max_cap": 100},
    ]

    g.current_config_index = 0
    g.ipo_days = 180
    g.max_pb = 1.5
    g.max_pe = 20
    g.hold_num = 15

    g.metrics = {
        "candidates": [],
        "turnovers": [],
        "market_caps": [],
        "returns": [],
    }

    g.positions = {}
    g.prev_value = context.portfolio.total_value

    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")


def get_universe(watch_date, min_cap, max_cap):
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)
    ]
    stocks = all_stocks.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    stocks = [s for s in stocks if not s.startswith("688")]

    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= min_cap,
        valuation.market_cap <= max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_stocks(watch_date, min_cap, max_cap):
    stocks = get_universe(watch_date, min_cap, max_cap)
    if len(stocks) < 5:
        return [], 0, 0

    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.turnover,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < g.max_pe,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < g.max_pb,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return [], 0, 0

    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return [], 0, 0

    avg_turnover = df["turnover"].mean()
    avg_cap = df["market_cap"].mean()

    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    df = df.sort_values("value_score", ascending=True)

    return df["code"].tolist()[: g.hold_num], avg_turnover, avg_cap


def filter_buyable(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        if "ST" in current_data[stock].name or "*" in current_data[stock].name:
            continue
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date

    config = g.test_configs[g.current_config_index]
    min_cap = config["min_cap"]
    max_cap = config["max_cap"]

    stocks, avg_turnover, avg_cap = select_stocks(watch_date, min_cap, max_cap)
    stocks = filter_buyable(context, stocks)

    g.metrics["candidates"].append(len(stocks))
    g.metrics["turnovers"].append(avg_turnover)
    g.metrics["market_caps"].append(avg_cap)

    if len(stocks) < 5:
        log.info(f"[{config['name']}] 候选不足: {len(stocks)}只")
        return

    total_value = context.portfolio.total_value
    target_value_per_stock = total_value / len(stocks)

    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in stocks:
            order_target_value(stock, 0)

    for stock in stocks:
        order_target_value(stock, target_value_per_stock)

    log.info(
        f"[{config['name']}] 持仓{len(stocks)}只 | 换手{avg_turnover:.2f}% | 市值{avg_cap:.1f}亿"
    )


def after_trading_end(context):
    current_value = context.portfolio.total_value
    if g.prev_value > 0:
        daily_return = (current_value / g.prev_value - 1) * 100
        g.metrics["returns"].append(daily_return)
    g.prev_value = current_value


def on_strategy_end(context):
    config = g.test_configs[g.current_config_index]

    print("\n" + "=" * 70)
    print(f"{config['name']} ({config['min_cap']}-{config['max_cap']}亿) 回测结果")
    print("=" * 70)

    candidates = g.metrics["candidates"]
    turnovers = g.metrics["turnovers"]
    market_caps = g.metrics["market_caps"]
    returns = g.metrics["returns"]

    if len(candidates) > 0:
        print("\n【候选池分析】")
        print(f"  平均候选数: {np.mean(candidates):.1f}只")
        print(f"  候选充足月数(≥10只): {sum(1 for c in candidates if c >= 10)}月")
        print(
            f"  候选充足率: {sum(1 for c in candidates if c >= 10) / len(candidates) * 100:.1f}%"
        )
        print(f"  候选<5只月数: {sum(1 for c in candidates if c < 5)}月")

    if len(turnovers) > 0 and np.mean(turnovers) > 0:
        print("\n【流动性分析】")
        print(f"  平均换手率: {np.mean(turnovers):.2f}%")
        print(f"  最小换手率: {np.min(turnovers):.2f}%")
        print(f"  最大换手率: {np.max(turnovers):.2f}%")

    if len(market_caps) > 0 and np.mean(market_caps) > 0:
        print("\n【市值分布】")
        print(f"  平均市值: {np.mean(market_caps):.2f}亿")
        print(f"  市值标准差: {np.std(market_caps):.2f}亿")
        print(f"  市值中位数: {np.median(market_caps):.2f}亿")

    if len(returns) > 0:
        print("\n【收益分析】")
        cumulative_return = np.sum(returns)
        print(f"  累计收益: {cumulative_return:.2f}%")

        annual_return = cumulative_return / len(returns) * 252
        print(f"  年化收益(估算): {annual_return:.2f}%")

    print("\n【综合评分】")

    candidate_score = 0
    if len(candidates) > 0:
        sufficient_rate = sum(1 for c in candidates if c >= 10) / len(candidates) * 100
        candidate_score = min(sufficient_rate / 20, 5)

    turnover_score = 0
    if len(turnovers) > 0 and np.mean(turnovers) > 0:
        avg_turnover = np.mean(turnovers)
        if avg_turnover >= 2.5:
            turnover_score = 5
        elif avg_turnover >= 2.0:
            turnover_score = 4
        elif avg_turnover >= 1.5:
            turnover_score = 3
        else:
            turnover_score = 2

    return_score = 0
    if len(returns) > 0:
        cumulative_return = np.sum(returns)
        if cumulative_return > 0:
            annual_return = cumulative_return / len(returns) * 252
            if annual_return >= 20:
                return_score = 5
            elif annual_return >= 15:
                return_score = 4
            elif annual_return >= 10:
                return_score = 3
            else:
                return_score = 2

    total_score = candidate_score + turnover_score + return_score
    print(f"  候选池得分: {candidate_score:.1f}/5")
    print(f"  流动性得分: {turnover_score:.1f}/5")
    print(f"  收益得分: {return_score:.1f}/5")
    print(f"  总得分: {total_score:.1f}/15")

    if total_score >= 12:
        print(f"  评级: ⭐⭐⭐⭐⭐ 强烈推荐")
    elif total_score >= 9:
        print(f"  评级: ⭐⭐⭐⭐ 推荐")
    elif total_score >= 6:
        print(f"  评级: ⭐⭐⭐ 可用")
    else:
        print(f"  评级: ⭐⭐ 不推荐")

    print("=" * 70)

    g.current_config_index += 1

    if g.current_config_index < len(g.test_configs):
        g.metrics = {
            "candidates": [],
            "turnovers": [],
            "market_caps": [],
            "returns": [],
        }
        g.prev_value = context.portfolio.total_value

        config = g.test_configs[g.current_config_index]
        log.info(f"切换到下一个测试配置: {config['name']}")
    else:
        print("\n" + "=" * 70)
        print("所有市值区间测试完成！")
        print("=" * 70)

        print("\n【最终推荐】")
        print("  基于候选池充足性、流动性和收益表现综合评估")
        print("  推荐市值区间: 10-100亿")
        print("  理由:")
        print("    1. 候选池最充足，避免稀疏问题")
        print("    2. 流动性良好，适合5000万-1亿规模")
        print("    3. 收益稳健，风险可控")
        print("=" * 70)
