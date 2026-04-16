# 北向资金股票轮动策略 - RiceQuant版本
# 原文：北向资金股票轮动-优质策略可直接实盘
# 作者：Funine
# 原文：https://www.joinquant.com/post/30772
# 注：RiceQuant无北向资金API，用沪深300成分股动量替代
# 逻辑：选沪深300中近期动量最强的股票持仓

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.empty_keep = '511880.XSHG'  # 货币基金
    context.max_stock_count = 15
    context.momentum_period = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components(context.index)
    if not stocks:
        return

    context.month = current_month

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.momentum_period + 1, '1d', 'close')
            if prices is None or len(prices) < context.momentum_period + 1:
                continue
            p = np.array(prices, dtype=float)
            momentum = (p[-1] / p[0]) - 1
            if momentum > 0:
                scores[stock] = momentum
        except Exception:
            continue

    if not scores:
        for stock in list(context.portfolio.positions.keys()):
            if stock != context.empty_keep:
                order_target_value(stock, 0)
        order_target_value(context.empty_keep, context.portfolio.total_value * 0.95)
        return

    target = sorted(scores, key=scores.get, reverse=True)[:context.max_stock_count]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target and stock != context.empty_keep:
            order_target_value(stock, 0)

    if context.empty_keep in context.portfolio.positions:
        order_target_value(context.empty_keep, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for stock in target:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
