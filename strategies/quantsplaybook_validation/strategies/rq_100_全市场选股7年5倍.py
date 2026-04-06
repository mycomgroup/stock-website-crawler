# 全市场选股7年5倍不择时策略 - RiceQuant版本
# 原文：全市场选股？7年5倍不择时，回撤30%左右
# 作者：Jacobb75
# 原文：https://www.joinquant.com/post/35307
# 逻辑：全市场选资产负债率低、ROA改善、营收增长的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['market_cap', 'roa', 'inc_revenue_year_on_year'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['roa'] > 0.0]
    df = df[df['inc_revenue_year_on_year'] > 0.05]
    df = df[df['debt_to_asset_ratio'] < 60.0]
    df = df.head(context.stock_num * 3)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    candidates = list(df.index)
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
