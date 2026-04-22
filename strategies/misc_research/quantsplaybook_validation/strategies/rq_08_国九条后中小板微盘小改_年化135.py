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


# 国九条后中小板微盘小改策略 - RiceQuant版本
# 逻辑：国九条后微盘股策略，选市值极小、PB>0、ROE>0的股票，过滤ST，月度调仓

import numpy as np


def init(context):
    context.stock_num = 30
    context.month = -1


def handle_bar(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    # 国九条后：排除科创板、北交所，聚焦中小板微盘
    stocks = [s for s in stock_ids
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
        df = df[df['market_cap'] > 2e+08]
        df = df[df['market_cap'] < 3e+09]
        df = df[df['roe'] > 0.00]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and not bar.is_trading:
            continue
        inst = instruments(stock)
        if inst and ('ST' in inst.symbol or '*' in inst.symbol):
            continue
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
