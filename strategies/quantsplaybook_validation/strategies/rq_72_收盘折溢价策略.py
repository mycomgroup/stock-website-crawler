# 收盘折溢价策略 - RiceQuant版本
# 逻辑：宽基ETF动量轮动（净值数据不可用，用动量代替折溢价逻辑）

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG',
        '518880.XSHG', '511010.XSHG',
    ]
    context.month = -1


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
            momentum = closes[-1] / closes[0] - 1
            vol = np.std(np.diff(closes) / closes[:-1])
            scores[etf] = momentum - vol * 2
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    best = max(scores, key=scores.get)
    if scores[best] < 0:
        return

    for etf in list(context.portfolio.positions.keys()):
        if etf != best:
            order_target_value(etf, 0)

    bar = (bar_dict[best] if best in bar_dict else None)
    if bar is None or bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
