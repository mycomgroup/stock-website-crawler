# 多品种ETF动量轮动EPO优化 - RiceQuant版本
# 逻辑：宽基+商品+债券ETF动量轮动，用等权代替EPO优化

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300
        '159915.XSHE',  # 创业板
        '518880.XSHG',  # 黄金
        '511010.XSHG',  # 国债
        '513100.XSHG',  # 纳指100
    ]
    context.momentum_days = 20
    context.top_n = 2
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.momentum_days + 1, '1d', 'close')
            if closes is None or len(closes) < context.momentum_days + 1:
                continue
            closes = np.array(closes, dtype=float)
            y = np.log(closes)
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            r2 = 1 - np.sum((y - (slope * x + intercept))**2) / (np.var(y) * len(y) + 1e-10)
            scores[etf] = (np.exp(slope * 250) - 1) * max(r2, 0)
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    sorted_etfs = sorted(scores, key=scores.get, reverse=True)
    target = [e for e in sorted_etfs if scores[e] > 0][:context.top_n]

    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_target_value(etf, 0)

    if not target:
        return

    weight = 1.0 / len(target)
    for etf in target:
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is None or bar.is_trading:
            order_target_value(etf, context.portfolio.total_value * weight * 0.95)
