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


# 最简强者恒强策略 - RiceQuant版本
# 原文：最简强者恒强策略
# 逻辑：选近期涨幅最大的股票（动量），月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.momentum_days = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]

    # 用市值过滤，选中小市值
    try:
        factor_df = get_factor(
            stocks,
            ['market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = _normalize_factor_frame(factor_df)
        if not hasattr(df, 'columns'):
            df = df.to_frame(name='market_cap')
        df = df[df['market_cap'] > 500000000]
        df = df[df['market_cap'] < 50000000000]
        if df is None or len(df) == 0:
            return
        df = df.sort_values('market_cap').head(200)
        candidates = list(df.index)
    except Exception:
        return
    # 计算动量（近N日涨幅）
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, context.momentum_days + 1, '1d', 'close')
            if closes is None or len(closes) < context.momentum_days + 1:
                continue
            momentum = closes[-1] / closes[0] - 1
            scores[stock] = momentum
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = []
    for stock in sorted_stocks:
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
