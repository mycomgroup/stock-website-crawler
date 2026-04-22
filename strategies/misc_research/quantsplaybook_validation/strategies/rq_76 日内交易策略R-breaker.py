# R-Breaker日内交易策略 - RiceQuant版本（日线近似）
# 逻辑：基于前日高低收盘价计算支撑阻力位，突破时交易

import numpy as np

def init(context):
    context.security = '510300.XSHG'
    context.f1 = 0.35
    context.f2 = 0.07
    context.f3 = 0.25
    context.pos = False
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
def handle_bar(context, bar_dict):
    closes = history_bars(context.security, 2, '1d', 'close')
    highs = history_bars(context.security, 2, '1d', 'high')
    lows = history_bars(context.security, 2, '1d', 'low')
    if closes is None or len(closes) < 2:
        return

    prev_close = closes[-2]
    prev_high = highs[-2]
    prev_low = lows[-2]

    pivot = (prev_high + prev_low + prev_close) / 3
    r1 = 2 * pivot - prev_low
    r2 = pivot + (prev_high - prev_low)
    s1 = 2 * pivot - prev_high
    s2 = pivot - (prev_high - prev_low)

    bar = (bar_dict[context.security] if context.security in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    cur = bar.close
    if cur > r2 and not context.pos:
        order_target_value(context.security, context.portfolio.total_value * 0.95)
        context.pos = True
    elif cur < s2 and context.pos:
        order_target_value(context.security, 0)
        context.pos = False
