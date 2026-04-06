# 红利搬砖策略 - RiceQuant版本
# 原文：红利搬砖，年化29%
# 逻辑：选沪深300中低PB、低PE、高股息的股票，月度调仓

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.top_n = 5
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    handle_trader(context, bar_dict)


def handle_trader(context, bar_dict):
    stocks = index_components(context.index)
    if not stocks:
        return

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pe_ratio', 'pb_ratio', 'dividend_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0]
        df = df[df['pb_ratio'] < 3]
        df = df[df['pe_ratio'] > 0]
        df = df[df['pe_ratio'] < 20]
        df = df[df['dividend_ratio'] > 0.0100]  # RQ dividend_ratio 是小数
        df = df[df['market_cap'] > 20]
        df = df.sort_values(['dividend_ratio', 'pb_ratio', 'pe_ratio'], ascending=[False, True, True])
        df = df.head(context.top_n * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.top_n:
            break

    if not target:
        return

    context.month = context.now.month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 0.95 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight)
