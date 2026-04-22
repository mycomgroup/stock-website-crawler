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


# 价值投资改进版 - RiceQuant版本
# 原文：价值投资改进版-6年9.5倍
# 逻辑：选大市值、高ROE、高ROA、低PB的价值股，季度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.quarter = -1


def handle_bar(context, bar_dict):
    # 季度调仓（每3个月）
    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'roe', 'roa'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['roe'] > 0.0]
        df = df[df['roa'] > 0.0]
        df = df[df['pb_ratio'] > 0.0]
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
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
    context.quarter = current_quarter

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
