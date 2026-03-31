# 小市值策略 V5 - 修复版
#
# 修复：简化情绪计算，确保能触发交易

from jqdata import *
import numpy as np


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09
    g.emotion_threshold = 20  # 降低阈值到20

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

    # 每周调仓
    run_weekly(rebalance, 1, "10:00")

    # 每日止损
    run_daily(stop_loss, "14:30")


def stop_loss(context):
    """止损"""
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(s, 0)
            log.info("止损: %s" % s)


def rebalance(context):
    """每周调仓"""

    # 1. 计算情绪指标（简化版）
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

    log.info("涨停家数: %d, 阈值: %d" % (zt_count, g.emotion_threshold))

    # 2. 情绪检查
    if zt_count < g.emotion_threshold:
        log.info("情绪不足，观望")
        return

    # 3. 获取股票池
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    # 过滤
    scu = [
        s
        for s in scu
        if not (
            current[s].paused
            or current[s].is_st
            or "ST" in current[s].name
            or "*" in current[s].name
            or "退" in current[s].name
        )
    ]

    # 次新股
    scu = [
        s
        for s in scu
        if (context.previous_date - get_security_info(s).start_date).days > 180
    ]

    log.info("过滤后股票数: %d" % len(scu))

    # 4. 市值筛选
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
        log.info("无符合条件股票")
        return

    stocks = list(df["code"])
    log.info("市值筛选后: %d只" % len(stocks))

    # 5. 不追涨停
    non_zt = []
    for s in stocks:
        if s in current:
            if (
                current[s].high_limit
                and current[s].last_price >= current[s].high_limit * 0.99
            ):
                continue
            non_zt.append(s)

    log.info("不追涨停后: %d只" % len(non_zt))

    if len(non_zt) == 0:
        return

    # 6. 选股（取市值最小的N只）
    selected = non_zt[: g.stock_num]

    # 7. 调仓
    # 卖出
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            order_target_value(s, 0)

    # 买入
    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)

    log.info("买入: %s" % selected[:5])
