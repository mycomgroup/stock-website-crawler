# Simple order test
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    log.info("INIT CALLED")


def handle_data(context, data):
    log.info("HANDLE_DATA CALLED")
    stock = "000001.SZ"
    position = context.portfolio.positions.get(stock)
    if not position:
        order_target_percent(stock, 0.1)
        log.info("ORDER SENT: " + stock)
