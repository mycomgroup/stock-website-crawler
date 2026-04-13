from jqdata import *

SLIPPAGE_BPS = 0


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")

    if SLIPPAGE_BPS > 0:
        set_slippage(FixedSlippage(SLIPPAGE_BPS / 10000))

    run_daily(buy, "09:35")
    run_daily(sell, "14:50")


def buy(context):
    if len(context.portfolio.positions) == 0:
        cash = context.portfolio.available_cash
        order_value("000001.XSHE", cash * 0.4)
        order_value("600000.XSHG", cash * 0.4)


def sell(context):
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            order_target(s, 0)
