# 假弱高开策略 - THSQuant SuperMind 格式
from mindgo_api import *


def init(context):
    set_benchmark("000300.SH")
    g.stock = "000001.SZ"


def handle_bar(context, bar_dict):
    log.info("HANDLE_BAR CALLED")
    stock = g.stock
    log.info("Stock: " + stock)
    log.info("bar_dict keys: " + str(list(bar_dict.keys())[:5]))
    if stock in bar_dict:
        log.info("Stock found in bar_dict")
        cd = bar_dict[stock]
        log.info("open=" + str(cd.open) + " close=" + str(cd.close))
        order_target_percent(stock, 0.1)
        log.info("ORDER SENT")
