"""
小市值策略 - 可运行版（简化）
去掉情绪开关，确保能交易

运行方式：
1. 复制到JoinQuant策略编辑器
2. 回测参数：2022-01-01 至 2024-12-31，初始资金10万
"""

from jqdata import *
import numpy as np


def initialize(context):
    """初始化"""
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09

    # 停手机制
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

    run_daily(stop_loss_check, "14:30")
    run_weekly(rebalance, 1, "10:00")


def stop_loss_check(context):
    """止损"""
    if g.pause_days > 0:
        g.pause_days -= 1
        return

    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(stock, 0)
            g.loss_count += 1
            if g.loss_count >= 3 and g.pause_days == 0:
                g.pause_days = 3
                log.info("停手3天")


def rebalance(context):
    """调仓"""
    # 停手检查
    if g.pause_days > 0:
        log.info("停手中")
        return

    # 获取股票池
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

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

    # 选市值最小的N只
    selected = list(df["code"])[: g.stock_num]

    log.info("选中: %s" % selected[:5])

    # 调仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected:
            pos = context.portfolio.positions[stock]
            if pos.price > pos.avg_cost:
                g.loss_count = 0
            order_target_value(stock, 0)

    value = context.portfolio.total_value / len(selected)
    for stock in selected:
        order_target_value(stock, value)
