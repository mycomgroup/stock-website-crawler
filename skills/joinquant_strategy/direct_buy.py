from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")
    g.day = 0


def handle_data(context, data):
    g.day += 1

    if g.day == 1:
        # 直接买入两只股票测试
        order_value("000001.XSHE", 500000)
        order_value("600000.XSHG", 500000)
        log.info("买入测试股票")

    if g.day == 10:
        # 10天后卖出
        for s in list(context.portfolio.positions):
            order_target(s, 0)
        log.info("卖出")
