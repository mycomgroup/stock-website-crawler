# 场内基金定投价值平均增强策略 - RiceQuant版本
# 逻辑：选宽基ETF，用价值平均法（目标价值线性增长）定投，月度执行

import numpy as np


def init(context):
    context.etf = '510300.XSHG'
    context.monthly_target_growth = 5000
    context.target_value = 0
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    context.target_value += context.monthly_target_growth

    bar = (bar_dict[context.etf] if context.etf in bar_dict else None)
    if bar is not None and not bar.is_trading:
        return

    pos = context.portfolio.positions.get(context.etf)
    current_value = pos.market_value if pos else 0
    diff = context.target_value - current_value

    if abs(diff) > 1000:
        order_target_value(context.etf, min(context.target_value, context.portfolio.total_value * 0.95))
