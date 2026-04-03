# Ultra simple test
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    log.info("INIT CALLED")


def handle_bar(context, bar_dict):
    log.info("HANDLE_BAR at " + context.current_dt.strftime("%H:%M"))
    stock = "000001.SZ"
    if stock in bar_dict:
        cd = bar_dict[stock]
        log.info("open=" + str(cd.open) + " close=" + str(cd.close))
        order_target_percent(stock, 0.1)
        log.info("ORDER SENT")
