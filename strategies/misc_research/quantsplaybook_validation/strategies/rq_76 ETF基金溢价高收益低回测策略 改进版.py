# ETF基金溢价策略改进版 - RiceQuant版本
# 逻辑：宽基ETF动量轮动，选近期动量最强的ETF

import numpy as np

CASH_ETF = '511010.XSHG'

def init(context):
    context.etf_pool = ['510300.XSHG','159915.XSHE','510500.XSHG','518880.XSHG','511010.XSHG']
    context.month = -1
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)

def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            closes = np.array(closes, dtype=float)
            scores[etf] = closes[-1] / closes[0] - 1
        except Exception:
            continue

    target = CASH_ETF
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            target = best
    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)
    order_target_value(target, context.portfolio.total_value * 0.95)

    context.month = current_month
