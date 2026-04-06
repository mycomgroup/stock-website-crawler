# 不含未来宽基ETF轮动8年50倍 - RiceQuant版本
# 逻辑：宽基ETF动量轮动 + BBI择时，无未来函数

import numpy as np

DEFENSIVE_ASSET = '511010.XSHG'


def calc_bbi(closes):
    if len(closes) < 24:
        return None
    return (np.mean(closes[-3:]) + np.mean(closes[-6:]) +
            np.mean(closes[-12:]) + np.mean(closes[-24:])) / 4


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG',
        '510050.XSHG', '518880.XSHG', '511010.XSHG',
    ]
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 65, '1d', 'close')
            if closes is None or len(closes) < 30:
                continue
            closes = np.array(closes, dtype=float)
            bbi = calc_bbi(closes)
            if bbi is None:
                continue
            # BBI过滤：价格在BBI上方才考虑
            if closes[-1] < bbi:
                continue
            momentum = closes[-1] / closes[-20] - 1
            scores[etf] = momentum
        except Exception:
            continue

    target = DEFENSIVE_ASSET
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            target = best

    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    order_target_value(target, context.portfolio.total_value * 0.95)

    context.month = current_month
