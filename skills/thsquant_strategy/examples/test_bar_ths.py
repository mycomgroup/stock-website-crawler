# Test with handle_bar
from mindgo_api import *


def init(context):
    set_benchmark("000300.SH")
    context.stock = "000001.SZ"


def handle_bar(context, bar_dict):
    log.info("HANDLE_BAR CALLED")
    stock = context.stock
    if stock in bar_dict:
        log.info("Stock in bar_dict: " + stock)
        log.info("Close: " + str(bar_dict[stock].close))
    position = context.portfolio.positions.get(stock)
    if not position:
        order_target_percent(stock, 0.1)
        log.info("ORDER SENT: " + stock)
