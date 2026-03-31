# 小市值策略 - 最简版
# 去掉情绪开关，确保能交易

from jqdata import *


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200

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


def rebalance(context):
    """每周调仓 - 最简单版本"""

    # 1. 获取股票池
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    # 2. 过滤ST和停牌
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

    log.info("过滤后: %d只" % len(scu))

    # 3. 市值筛选
    q = (
        query(valuation.code, valuation.market_cap)
        .filter(
            valuation.code.in_(scu), valuation.market_cap.between(g.min_cap, g.max_cap)
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)

    if df is None or len(df) == 0:
        log.info("无股票")
        return

    # 4. 选股
    selected = list(df["code"])[: g.stock_num]

    log.info("选中: %s" % selected)

    # 5. 调仓
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            order_target_value(s, 0)

    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)
