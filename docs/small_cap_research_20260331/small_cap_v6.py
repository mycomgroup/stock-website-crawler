# 小市值策略 V6 - 完整版
# 加入情绪开关 + 停手机制

from jqdata import *


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09

    # 情绪开关参数
    g.emotion_threshold = 25  # 涨停>=25开仓

    # 停手机制参数
    g.loss_count = 0  # 连续亏损计数
    g.pause_days = 0  # 剩余停手天数

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
    """盘前：更新停手状态 + 计算情绪"""
    # 更新停手
    if g.pause_days > 0:
        g.pause_days -= 1
        log.info("停手中，剩余%d天" % g.pause_days)

    # 计算情绪
    all_stocks = list(get_all_securities("stock").index)
    all_stocks = [
        s
        for s in all_stocks
        if not s.startswith("688") and not s.startswith("8") and not s.startswith("4")
    ]

    current = get_current_data()
    zt_count = 0

    for s in all_stocks[:300]:
        if s in current and current[s].high_limit:
            if current[s].last_price >= current[s].high_limit * 0.99:
                zt_count += 1

    g.emotion = zt_count
    log.info("涨停家数: %d, 阈值: %d" % (zt_count, g.emotion_threshold))


def stop_loss(context):
    """止损"""
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(s, 0)
            log.info("止损: %s" % s)

            # 记录亏损
            g.loss_count += 1
            if g.loss_count >= 3 and g.pause_days == 0:
                g.pause_days = 3
                log.info("触发停手：连亏3笔，停手3天")


def rebalance(context):
    """每周调仓"""

    # 停手检查
    if g.pause_days > 0:
        log.info("停手中，跳过")
        return

    # 情绪检查
    if g.emotion < g.emotion_threshold:
        log.info("情绪不足(%d<%d)，观望" % (g.emotion, g.emotion_threshold))
        return

    # 获取股票池
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    current = get_current_data()
    scu = [
        s
        for s in scu
        if not (
            current[s].paused
            or current[s].is_st
            or "ST" in current[s].name
            or "*" in current[s].name
        )
    ]

    # 市值筛选
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

    # 卖出
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            pos = context.portfolio.positions[s]
            pnl = pos.price / pos.avg_cost - 1

            if pnl > 0:
                g.loss_count = 0  # 盈利清零连亏
            else:
                g.loss_count += 1

            order_target_value(s, 0)

    # 买入
    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)

    log.info("买入: %s" % selected[:5])
