# 致敬市场(1)探讨指数化策略投资 - RiceQuant版本
# 原文：致敬市场(1)，探讨指数化策略投资
# 逻辑：在中证500成分股中，选低PB、高ROE的股票做指数增强，月度调仓

import numpy as np


def init(context):
    context.index = '000905.XSHG'
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    iHandle(context, bar_dict, current_month)


def iHandle(context, bar_dict, current_month):
    stocks = index_components(context.index)
    if not stocks or len(stocks) < 10:
        return

    context.month = current_month

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['roe'] > 0.00]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)