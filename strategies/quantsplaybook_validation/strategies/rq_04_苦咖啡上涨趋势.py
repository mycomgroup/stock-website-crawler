# 苦咖啡-默默赚钱系列（上涨趋势策略）- RiceQuant版本
# 原文：苦咖啡-默默赚钱系列-改
# 原文：https://www.joinquant.com/post/31267
# 逻辑：沪深300成分股中，选近120日线性回归斜率/截距>0.005且R²>0.9的股票，周度调仓

import numpy as np
from scipy.stats import linregress


def init(context):
    context.index = '000300.XSHG'
    context.max_hold = 2
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    stocks = index_components(context.index)
    if not stocks:
        return

    target_dict = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, 120, '1d', 'close')
            if prices is None or len(prices) < 120:
                continue
            y = np.array(prices, dtype=float)
            x = np.arange(120)
            slope, intercept, r_value, _, _ = linregress(x, y)
            if intercept > 0 and slope / intercept > 0.005 and r_value > 0.9:
                target_dict[stock] = r_value ** 2
        except Exception:
            continue

    if not target_dict:
        return

    target = sorted(target_dict, key=target_dict.get, reverse=True)[:context.max_hold]
    context.week = current_week

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
