# 八仙过海V2策略 - RiceQuant版本
# 逻辑：多ETF动量轮动，选动量最强的ETF持有

import numpy as np

CASH_ETF = '511010.XSHG'

def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG', '510050.XSHG',
        '518880.XSHG', '511010.XSHG', '513100.XSHG', '159928.XSHE',
    ]
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
            closes = history_bars(etf, 61, '1d', 'close')
            if closes is None or len(closes) < 61:
                continue
            closes = np.array(closes, dtype=float)
            y = np.log(closes)
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            r2 = 1 - np.sum((y - (slope * x + intercept))**2) / (np.var(y) * len(y) + 1e-10)
            scores[etf] = (np.exp(slope * 250) - 1) * max(r2, 0)
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
