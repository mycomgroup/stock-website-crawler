# 20行代码高胜率策略 - RiceQuant版本
# 逻辑：简单双均线择时（MA20 vs MA60），沪深300ETF，日度判断

import numpy as np


def init(context):
    context.security = '510300.XSHG'
    context.ma_short = 20
    context.ma_long = 60
    context.pos = False


def handle_bar(context, bar_dict):
    closes = history_bars(context.security, context.ma_long + 5, '1d', 'close')
    if closes is None or len(closes) < context.ma_long:
        return

    closes = np.array(closes, dtype=float)
    ma_short = np.mean(closes[-context.ma_short:])
    ma_long = np.mean(closes[-context.ma_long:])

    bar = (bar_dict[context.security] if context.security in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    if ma_short > ma_long and not context.pos:
        order_target_value(context.security, context.portfolio.total_value * 0.95)
        context.pos = True
    elif ma_short < ma_long and context.pos:
        order_target_value(context.security, 0)
        context.pos = False
