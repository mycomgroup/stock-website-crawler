# Minimal test with handle_data and no f-strings
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    log.info("INIT OK")


def handle_data(context, data):
    stock = "000001.SZ"
    log.info("HANDLE_DATA at " + context.current_dt.strftime("%Y-%m-%d"))
    log.info("data type: " + str(type(data)))
    log.info("data keys: " + str(list(data.keys())[:5]))
