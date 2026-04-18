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


# 大市值价值投资超额稳定策略 - RiceQuant版本
# 逻辑：market_cap>500亿 + pb低 + roe高，季度调仓

import numpy as np


def init(context):
    context.stock_num = 15
    context.quarter = -1


def handle_bar(context, bar_dict):
    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        return

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 5e+10]
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 5.0]
        df = df[df['roe'] > 0.10]
        df = df[df['roa'] > 0.05]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = [s for s in candidates if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return
    context.quarter = current_quarter

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)