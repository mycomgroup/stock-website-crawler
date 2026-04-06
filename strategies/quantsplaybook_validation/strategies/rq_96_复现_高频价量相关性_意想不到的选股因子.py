# 复现高频价量相关性选股因子 - RiceQuant版本
# 逻辑：计算日线价量相关性（收益率与成交量变化率的相关系数），选相关性高的股票

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components('000300.XSHG')
    if not stocks:
        return

    context.month = current_month

    scores = {}
    for stock in stocks:
        try:
            closes = history_bars(stock, 22, '1d', 'close')
            volumes = history_bars(stock, 22, '1d', 'volume')
            if closes is None or volumes is None or len(closes) < 22:
                continue
            closes = np.array(closes, dtype=float)
            volumes = np.array(volumes, dtype=float)
            price_ret = np.diff(closes) / closes[:-1]
            vol_ret = np.diff(volumes) / (volumes[:-1] + 1e-10)
            if np.std(price_ret) == 0 or np.std(vol_ret) == 0:
                continue
            corr = np.corrcoef(price_ret, vol_ret)[0, 1]
            scores[stock] = corr
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
