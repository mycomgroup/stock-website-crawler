# ETF T0动量策略 - RiceQuant版本
# 逻辑：宽基ETF日内动量（用日线近似），选近5日涨幅最强的ETF持有

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG',
        '510050.XSHG', '518880.XSHG',
    ]
    context.bond_etf = '511010.XSHG'
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 6, '1d', 'close')
            if closes is None or len(closes) < 6:
                continue
            closes = np.array(closes, dtype=float)
            momentum_5d = closes[-1] / closes[0] - 1
            scores[etf] = momentum_5d
        except Exception:
            continue

    if not scores:
        return

    best = max(scores, key=scores.get)

    if scores[best] <= 0:
        for etf in list(context.portfolio.positions.keys()):
            if etf != context.bond_etf:
                order_target_value(etf, 0)
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        return

    for etf in list(context.portfolio.positions.keys()):
        if etf != best:
            order_target_value(etf, 0)

    bar = (bar_dict[best] if best in bar_dict else None)
    if bar is not None and bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
