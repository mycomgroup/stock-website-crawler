# Minimal test strategy with handle_data
from mindgo_api import *


def initialize(context):
    log.info("INITIALIZE CALLED")
    set_benchmark("000300.SH")


def handle_data(context, data):
    log.info("HANDLE_DATA CALLED at " + context.current_dt.strftime("%Y-%m-%d %H:%M"))
    for stock in ["000001.SZ"]:
        bar = data[stock]
        if bar:
            log.info("Stock: %s, close: %s" % (stock, bar.close))
