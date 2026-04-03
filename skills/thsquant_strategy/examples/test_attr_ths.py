# Minimal attribute_history test
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    run_daily(test_attr, time="before_open")


def test_attr(context):
    stock = "000001.SZ"
    prices = attribute_history(stock, 5, "1d", ["close", "high_limit"])
    log.info("Prices type: %s" % type(prices))
    log.info(
        "Prices columns: %s"
        % str(prices.columns.tolist() if hasattr(prices, "columns") else "N/A")
    )
    log.info(
        "Prices shape: %s" % str(prices.shape if hasattr(prices, "shape") else "N/A")
    )
    log.info(
        "Prices last row: %s"
        % str(prices.iloc[-1].to_dict() if len(prices) > 0 else "empty")
    )
