# 趋势交易5.0无择时策略 - RiceQuant版本
# 原文：趋势交易5.0 无择时-2年5倍不是梦
# 作者：矢南
# 原文：https://www.joinquant.com/post/31286
# 逻辑：选沪深300成分股中趋势最强的股票，用线性回归斜率评分
# 注：RiceQuant 不支持 scipy，已用 numpy 手动实现线性回归替代 linregress

import numpy as np


def numpy_linregress(x, y):
    """纯 numpy 线性回归，返回 slope 和 r"""
    x_mean, y_mean = np.mean(x), np.mean(y)
    ss_xx = np.sum((x - x_mean) ** 2)
    if ss_xx == 0:
        return 0, 0
    slope = np.sum((x - x_mean) * (y - y_mean)) / ss_xx
    y_hat = y_mean + slope * (x - x_mean)
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    r = np.sqrt(max(r2, 0))
    return slope, r


def init(context):
    context.index = '000300.XSHG'
    context.buy_count = 10
    context.period = 60
    context.month = -1


def get_trend_score(stock, period=60):
    try:
        prices = history_bars(stock, period, '1d', 'close')
        if prices is None or len(prices) < period:
            return None
        p = np.array(prices, dtype=float)
        x = np.arange(period)
        slope, r = numpy_linregress(x, np.log(p))
        annualized = np.exp(slope * 250) - 1
        return annualized * (r ** 2)
    except Exception:
        return None


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
        score = get_trend_score(stock, context.period)
        if score is not None and score > 0:
            scores[stock] = score

    if not scores:
        return

    target = sorted(scores, key=scores.get, reverse=True)[:context.buy_count]

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
