# BigQuant 简单回测示例

import numpy as np
import pandas as pd


def initialize(context):
    set_benchmark("000300.XSHG")
    context.stock = "000001.XSHE"


def handle_data(context, data):
    if context.stock not in context.portfolio.positions:
        order_target_percent(context.stock, 1.0)
        print(f"买入 {context.stock}")


def after_trading(context):
    pass
