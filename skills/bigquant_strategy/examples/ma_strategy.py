# BigQuant 双均线策略示例

import numpy as np
import pandas as pd


def initialize(context):
    set_benchmark("000300.XSHG")
    context.stock = "000001.XSHE"
    context.short_window = 5
    context.long_window = 20


def handle_data(context, data):
    prices = history(context.stock, ["close"], context.long_window, "1d")
    if prices is None or len(prices) < context.long_window:
        return

    short_ma = prices["close"].iloc[-context.short_window :].mean()
    long_ma = prices["close"].mean()

    current_position = context.portfolio.positions.get(context.stock, None)

    if short_ma > long_ma and not current_position:
        order_target_percent(context.stock, 1.0)
        print(f"买入信号触发: 短均线={short_ma:.2f}, 长均线={long_ma:.2f}")
    elif short_ma < long_ma and current_position:
        order_target_percent(context.stock, 0)
        print(f"卖出信号触发: 短均线={short_ma:.2f}, 长均线={long_ma:.2f}")
