# 股指期货收盘折溢价策略 - RiceQuant版本
# 逻辑：用沪深300ETF代替期货，价格低于20日均线时买入（折价），高于时卖出

import numpy as np


def init(context):
    context.security = '510300.XSHG'
    context.ma_period = 20
    context.pos = False


def handle_bar(context, bar_dict):
    closes = history_bars(context.security, context.ma_period + 5, '1d', 'close')
    if closes is None or len(closes) < context.ma_period:
        return

    closes = np.array(closes, dtype=float)
    ma = np.mean(closes[-context.ma_period:])
    cur = closes[-1]

    bar = (bar_dict[context.security] if context.security in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    # 折价（价格低于均线）→ 买入
    if cur < ma * 0.99 and not context.pos:
        order_target_value(context.security, context.portfolio.total_value * 0.95)
        context.pos = True
    # 溢价（价格高于均线）→ 卖出
    elif cur > ma * 1.01 and context.pos:
        order_target_value(context.security, 0)
        context.pos = False
