# 多因子策略（多元线性回归APT模型）- RiceQuant版本
# 原文：因子分析系列文章（八）：多因子策略（多元线性回归）
# 作者：量化狙击
# 原文：https://www.joinquant.com/post/25273
# 逻辑：市值+ROE多因子，每15天调仓，持仓9只

import numpy as np


def init(context):
    context.top_n = 9
    context.rebal_days = 15
    context.day_count = 0
    context.empty_etf = '511880.XSHG'


def handle_bar(context, bar_dict):
    context.day_count += 1
    if context.day_count % context.rebal_days != 0:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 500000000]
    df = df[df['roe'] > 0.05]
    df = df.head(context.top_n * 5)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    candidates = list(df.index)
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.top_n:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
