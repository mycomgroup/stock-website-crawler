def _normalize_factor_frame(factor_df):
    if factor_df is None:
        return None
    try:
        if hasattr(factor_df, 'empty') and factor_df.empty:
            return factor_df
        if not hasattr(factor_df, 'columns'):
            factor_df = factor_df.to_frame()
        index = getattr(factor_df, 'index', None)
        if index is not None and getattr(index, 'nlevels', 1) > 1:
            factor_df = factor_df.groupby(level=-1).last()
        return factor_df.dropna()
    except Exception:
        return None


# 精选价值策略 - RiceQuant版本
# 原文：精选价值策略
# 作者：BAFE
# 原文：https://www.joinquant.com/post/29574
# 逻辑：多维财务筛选（市值、ROE、现金流、营收增长），月度调仓

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

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe', 'inc_net_profit_year_on_year', 'inc_revenue_year_on_year', 'operating_cash_flow'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['market_cap'] > 5e9]   # NOTE: RQ market_cap is yuan (元), JQ was 亿
        df = df[df['roe'] > 0.10]          # NOTE: RQ roe is decimal, JQ was percent
        df = df[df['inc_revenue_year_on_year'] > 0]
        df = df[df['inc_revenue_year_on_year'] < 0.50]
        df = df[df['inc_net_profit_year_on_year'] > 0.06]
        df = df[df['inc_net_profit_year_on_year'] < 0.50]
        df = df[df['operating_cash_flow'] > 0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or bar.is_trading:
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
