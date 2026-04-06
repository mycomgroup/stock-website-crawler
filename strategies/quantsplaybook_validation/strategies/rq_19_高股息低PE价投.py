# 高股息低市盈率稳健增长价投策略 - RiceQuant版本
# 原文：高股息低市盈率稳健增长的价投策略
# 作者：芹菜1303
# 原文：https://www.joinquant.com/post/45552
# 逻辑：筛选PE低、ROE高、营收增长稳健的股票，月度调仓

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
    stocks = [s for s in stocks if not s.startswith(('688', '4', '8'))]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'roe', 'inc_net_profit_year_on_year', 'inc_revenue_year_on_year']
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 25.0]
    df = df[df['roe'] > 0.1]
    df = df[df['inc_net_profit_year_on_year'] > 0.1]
    df = df[df['inc_revenue_year_on_year'] > 0.05]
    df = df.head(context.stock_num * 3)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    candidates = list(df.index)
    target = [s for s in candidates if s in bar_dict and bar_dict[s].is_trading][:context.stock_num]

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
