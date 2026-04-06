# 北向Boll带ETF策略 - RiceQuant版本
# 逻辑：用布林带择时宽基ETF，价格突破上轨买入，跌破下轨卖出

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG', '510050.XSHG',
    ]
    context.bond_etf = '511010.XSHG'
    context.period = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 25, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            closes = np.array(closes, dtype=float)
            ma = np.mean(closes[-20:])
            std = np.std(closes[-20:])
            upper = ma + 2 * std
            lower = ma - 2 * std
            if closes[-1] > upper:
                scores[etf] = closes[-1] / closes[-20] - 1
        except Exception:
            continue

    if not scores:
        for etf in list(context.portfolio.positions.keys()):
            if etf != context.bond_etf:
                order_target_value(etf, 0)
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is not None and bar.is_trading and context.bond_etf not in context.portfolio.positions:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        return

    best = max(scores, key=scores.get)
    for etf in list(context.portfolio.positions.keys()):
        if etf != best:
            order_target_value(etf, 0)
    bar = (bar_dict[best] if best in bar_dict else None)
    if bar is not None and bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
