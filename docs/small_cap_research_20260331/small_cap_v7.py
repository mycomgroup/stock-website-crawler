# 小市值策略 V7 - 优化情绪阈值
# 降低情绪阈值到15

from jqdata import *


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09
    g.emotion_threshold = 15  # 降低到15

    g.loss_count = 0
    g.pause_days = 0

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
    if g.pause_days > 0:
        g.pause_days -= 1

    # 简化情绪计算
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")
    current = get_current_data()
    zt = 0
    for s in scu[:100]:
        if s in current and current[s].high_limit:
            if current[s].last_price >= current[s].high_limit * 0.99:
                zt += 1
    g.emotion = zt * 3  # 放大系数


def stop_loss(context):
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(s, 0)
            g.loss_count += 1
            if g.loss_count >= 3 and g.pause_days == 0:
                g.pause_days = 3


def rebalance(context):
    if g.pause_days > 0:
        return

    if g.emotion < g.emotion_threshold:
        log.info("情绪不足: %d" % g.emotion)
        return

    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")
    current = get_current_data()
    scu = [
        s
        for s in scu
        if not (current[s].paused or current[s].is_st or "ST" in current[s].name)
    ]

    q = (
        query(valuation.code, valuation.market_cap)
        .filter(
            valuation.code.in_(scu),
            valuation.market_cap.between(g.min_cap, g.max_cap),
            income.net_profit > 0,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)
    if df is None or len(df) == 0:
        return

    selected = list(df["code"])[: g.stock_num]

    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            pos = context.portfolio.positions[s]
            if pos.price > pos.avg_cost:
                g.loss_count = 0
            order_target_value(s, 0)

    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)

    log.info("买入: %s, 情绪:%d" % (selected[:3], g.emotion))
