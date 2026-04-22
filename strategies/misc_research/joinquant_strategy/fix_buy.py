from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")

    run_daily(buy, "09:35")
    run_daily(sell, "14:50")


def buy(context):
    if len(context.portfolio.positions) == 0:
        # 分散资金买入
        cash = context.portfolio.available_cash
        order_value("000001.XSHE", cash * 0.4)
        order_value("600000.XSHG", cash * 0.4)
        log.info(f"买入，可用资金:{cash}")


def sell(context):
    # 检查是否有可平仓
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            order_target(s, 0)
            log.info(f"卖出 {s}")
