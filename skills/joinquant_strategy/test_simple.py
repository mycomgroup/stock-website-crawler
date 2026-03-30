# 最简单的测试策略
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")

    g.stock = "000001.XSHE"
    run_daily(trade, "9:30")


def trade(context):
    if context.portfolio.positions[g.stock].total_amount == 0:
        order_value(g.stock, 10000)
    else:
        order_target_value(g.stock, 0)
