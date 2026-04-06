# 高股息低市盈率高增长价投策略 - RiceQuant版本
# 原文：高股息低市盈率高增长的价投策略
# 作者：芹菜1303
# 原文：https://www.joinquant.com/post/45552
# 逻辑：PE低、ROE高、营收增长稳健，月度调仓

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

    try:
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'roe', 'inc_net_profit_year_on_year', 'inc_revenue_year_on_year', 'dividend_ratio', 'market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if not hasattr(df, 'columns'):
            return
        df = df[df['market_cap'] > 20]
        df = df[df['pe_ratio'] > 0]
        df = df[df['pe_ratio'] < 25]
        df = df[df['roe'] > 0.08]
        df = df[df['inc_net_profit_year_on_year'] > 0.08]
        df = df[df['inc_revenue_year_on_year'] > 0.05]
        df = df[df['dividend_ratio'] > 0.005]
        df = df.sort_values(
            ['dividend_ratio', 'inc_net_profit_year_on_year', 'roe', 'pe_ratio'],
            ascending=[False, False, False, True]
        )
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

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
