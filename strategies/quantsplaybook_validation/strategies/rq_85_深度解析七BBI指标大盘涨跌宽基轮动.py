# 深度解析七_BBI指标大盘涨跌宽基轮动 - RiceQuant版本
# 逻辑：用BBI指标判断大盘涨跌，在宽基ETF中轮动

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG', '510050.XSHG',
    ]
    context.bond_etf = '511010.XSHG'
    context.ref = '000300.XSHG'
    context.month = -1


def handle_bar(context, bar_dict):
    # BBI择时
    closes = history_bars(context.ref, 30, '1d', 'close')
    if closes is None or len(closes) < 25:
        return
    closes = np.array(closes, dtype=float)
    bbi = (np.mean(closes[-3:]) + np.mean(closes[-6:]) +
           np.mean(closes[-12:]) + np.mean(closes[-24:])) / 4
    above_bbi = closes[-1] > bbi

    if not above_bbi:
        for etf in list(context.portfolio.positions.keys()):
            if etf != context.bond_etf:
                order_target_value(etf, 0)
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is not None and bar.is_trading and context.bond_etf not in context.portfolio.positions:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        return

    current_month = context.now.month
    if current_month == context.month:
        return

    if context.bond_etf in context.portfolio.positions:
        order_target_value(context.bond_etf, 0)

    scores = {}
    for etf in context.etf_pool:
        try:
            c = history_bars(etf, 21, '1d', 'close')
            if c is None or len(c) < 21:
                continue
            scores[etf] = np.array(c, dtype=float)[-1] / np.array(c, dtype=float)[0] - 1
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    best = max(scores, key=scores.get)
    for etf in list(context.portfolio.positions.keys()):
        if etf != best:
            order_target_value(etf, 0)
    bar = (bar_dict[best] if best in bar_dict else None)
    if bar is not None and bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
