# ETF趋势跟随策略 - RiceQuant版本
# 逻辑：宽基ETF动量轮动，趋势确认后买入，跌破均线卖出

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300
        '159915.XSHE',  # 创业板
        '510500.XSHG',  # 中证500
        '510050.XSHG',  # 上证50
    ]
    context.bond_etf = '511010.XSHG'
    context.ma_period = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        # 日度止损：跌破均线卖出
        for etf in list(context.portfolio.positions.keys()):
            if etf == context.bond_etf:
                continue
            closes = history_bars(etf, context.ma_period + 1, '1d', 'close')
            if closes is None or len(closes) < context.ma_period:
                continue
            ma = np.mean(closes[-context.ma_period:])
            if closes[-1] < ma * 0.98:
                order_target_value(etf, 0)
                bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
                if bar is None or bar.is_trading:
                    order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        return
    context.month = current_month

    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 61, '1d', 'close')
            if closes is None or len(closes) < 61:
                continue
            closes = np.array(closes, dtype=float)
            ma20 = np.mean(closes[-20:])
            # 只选价格在均线上方的ETF
            if closes[-1] < ma20:
                continue
            momentum = closes[-1] / closes[0] - 1
            scores[etf] = momentum
        except Exception:
            continue

    if not scores:
        for etf in list(context.portfolio.positions.keys()):
            if etf != context.bond_etf:
                order_target_value(etf, 0)
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is None or bar.is_trading:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        return

    best = max(scores, key=scores.get)

    for etf in list(context.portfolio.positions.keys()):
        if etf != best:
            order_target_value(etf, 0)

    bar = (bar_dict[best] if best in bar_dict else None)
    if bar is None or bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
