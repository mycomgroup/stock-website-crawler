"""
小市值策略 V9 - 修复版
修复了之前版本缺少ST过滤导致买入垃圾股的问题
加入了止损机制

运行方式：
1. 复制到JoinQuant策略编辑器
2. 回测参数：2022-01-01 至 2024-12-31，初始资金10万
"""

from jqdata import *


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09

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
    """每日止损检查"""
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(s, 0)
            log.info("止损: %s" % s)


def rebalance(context):
    """每周调仓"""
    # 1. 获取股票池
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    # 2. 过滤ST、停牌 (关键修复)
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

    # 3. 市值+财务筛选
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
    log.info("选中: %s" % selected[:5])

    # 4. 调仓
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            order_target_value(s, 0)

    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)
