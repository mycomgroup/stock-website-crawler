from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")

    g.bought = False
    run_daily(trade, "09:35")
    run_daily(sell, "14:50")


def trade(context):
    if not g.bought:
        order_value("000001.XSHE", 500000)
        order_value("600000.XSHG", 500000)
        g.bought = True
        log.info("买入")


def sell(context):
    g.bought = False
    for s in list(context.portfolio.positions):
        order_target(s, 0)
