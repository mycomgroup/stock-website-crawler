# 宽基BBI动量追涨策略 - RiceQuant版本
# 逻辑：计算宽基ETF的BBI指标（3/6/12/24日均线均值），价格突破BBI时买入

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG', '510050.XSHG',
    ]
    context.bond_etf = '511010.XSHG'


def handle_bar(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 30, '1d', 'close')
            if closes is None or len(closes) < 25:
                continue
            closes = np.array(closes, dtype=float)
            bbi = (np.mean(closes[-3:]) + np.mean(closes[-6:]) +
                   np.mean(closes[-12:]) + np.mean(closes[-24:])) / 4
            if closes[-1] > bbi:
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
    if bar is None or bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
