# 追涨大师（超额142）策略 - RiceQuant版本
# 原文：追涨大师（超额142）
# 逻辑：选近期动量最强的股票，月度调仓

import numpy as np
import math


def get_momentum_score(stock, period=20):
    try:
        prices = history_bars(stock, period, '1d', 'close')
        if prices is None or len(prices) < period:
            return None
        y = np.log(np.array(prices, dtype=float))
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        annualized = math.exp(slope * 250) - 1
        y_hat = slope * x + intercept
        ss_res = np.sum((y - y_hat) ** 2)
        ss_tot = (len(y) - 1) * np.var(y, ddof=1)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return annualized * r2
    except Exception:
        return None


def init(context):
    context.index = '000300.XSHG'
    context.top_n = 10
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
        score = get_momentum_score(stock)
        if score is not None and score > 0:
            scores[stock] = score

    if not scores:
        return

    target = sorted(scores, key=scores.get, reverse=True)[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for stock in target:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
