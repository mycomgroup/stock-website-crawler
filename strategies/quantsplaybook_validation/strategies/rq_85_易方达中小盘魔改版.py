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


# 易方达中小盘魔改版 - RiceQuant版本
# 逻辑：跟踪中小盘指数，选中小综指成分股中低PB高ROE的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components('399101.XSHE')
    if not stocks or len(stocks) < 10:
        all_stocks = all_instruments('CS')['order_book_id'].tolist()
        stocks = [s for s in all_stocks
                  if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 4.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['roe'] > 0.08]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = [s for s in candidates if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return
    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
