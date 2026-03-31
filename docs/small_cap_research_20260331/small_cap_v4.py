# 小市值策略 V4 - 简化版
#
# 核心改进：
# 1. 简化情绪开关（涨停家数>=20即可）
# 2. 放宽市值范围（5-200亿）
# 3. 简化选股逻辑

from jqdata import *
import numpy as np


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09
    g.emotion_threshold = 20  # 放宽到20

    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    set_slippage(FixedSlippage(0.02))

    run_daily(before_open, "09:00")
    run_daily(stop_loss, "14:30")
    run_weekly(rebalance, 1, "10:00")


def before_open(context):
    # 计算情绪指标
    g.emotion = get_emotion(context)
    log.info("涨停家数: %d" % g.emotion)


def get_emotion(context):
    """简单计算涨停家数"""
    stocks = list(get_all_securities("stock").index)
    stocks = [s for s in stocks if not s.startswith("688") and not s.startswith("8")]

    current = get_current_data()
    count = 0

    for s in stocks[:300]:
        if s in current and current[s].high_limit:
            if current[s].last_price >= current[s].high_limit * 0.99:
                count += 1

    return count


def stop_loss(context):
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(s, 0)
            log.info("止损: %s" % s)


def rebalance(context):
    # 情绪检查
    if g.emotion < g.emotion_threshold:
        log.info("情绪不足，持有ETF")
        return

    # 获取股票池
    stocks = get_pool(context)
    log.info("候选池: %d只" % len(stocks))

    if len(stocks) == 0:
        return

    # 选股
    selected = stocks[: g.stock_num]

    # 卖出
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            order_target_value(s, 0)

    # 买入
    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)

    log.info("买入: %s" % selected)


def get_pool(context):
    """获取小市值股票池"""
    # 全A
    all_stocks = list(get_all_securities("stock", context.previous_date).index)

    # 过滤
    current = get_current_data()
    all_stocks = [
        s
        for s in all_stocks
        if not (
            current[s].paused
            or current[s].is_st
            or "ST" in current[s].name
            or "*" in current[s].name
            or s.startswith("688")
            or s.startswith("8")
        )
    ]

    # 次新股
    all_stocks = [
        s
        for s in all_stocks
        if (context.previous_date - get_security_info(s).start_date).days > 180
    ]

    # 市值筛选
    q = (
        query(valuation.code, valuation.market_cap)
        .filter(
            valuation.code.in_(all_stocks),
            valuation.market_cap.between(g.min_cap, g.max_cap),
            income.net_profit > 0,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)
    return list(df["code"]) if df is not None and len(df) > 0 else []
