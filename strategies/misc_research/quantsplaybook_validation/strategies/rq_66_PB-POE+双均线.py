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


# PB-POE+双均线策略 - RiceQuant版本
# 原文：PB-POE+双均线
# 逻辑：选低PB、高ROE（PB-ROE模型）的股票，结合双均线择时

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1
    context.index = '000300.XSHG'
    context.ma_short = 20
    context.ma_long = 60


def handle_bar(context, bar_dict):
    # 双均线择时
    closes = history_bars(context.index, context.ma_long + 5, '1d', 'close')
    if closes is None or len(closes) < context.ma_long:
        return
    ma_short = np.mean(closes[-context.ma_short:])
    ma_long = np.mean(closes[-context.ma_long:])
    bull_market = ma_short > ma_long

    # 月度选股
    current_month = context.now.month
    if current_month == context.month:
        if not bull_market and context.portfolio.positions:
            for stock in list(context.portfolio.positions.keys()):
                order_target_value(stock, 0)
        return

    if not bull_market:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pb_ratio', 'roe']
    )
    if factor_df is None or factor_df.empty:
        return
    df = _normalize_factor_frame(factor_df)
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 3.0]
    df = df[df['roe'] > 0.1]
    df = df.head(context.stock_num * 3)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    candidates = list(df.index)
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
