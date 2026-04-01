# 基准版本 - 无路由器，始终满仓沪深300
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.target_position = 100
    set_benchmark("000300.XSHG")


def handle_data(context, data):
    target_value = context.portfolio.total_value

    if "000300.XSHG" not in context.portfolio.positions:
        order_value("000300.XSHG", target_value)
