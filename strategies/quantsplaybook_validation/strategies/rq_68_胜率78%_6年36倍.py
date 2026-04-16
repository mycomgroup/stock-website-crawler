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


# 胜率78%，6年36倍策略 - RiceQuant版本
# 原文：胜率78%，6年36倍，今年行情依然50%年化
# 逻辑：综合成长（净利润增速）、价值（PE低）、动量（近期涨幅）多因子选股

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
        ['pe_ratio', 'roe', 'inc_net_profit_year_on_year']
    )
    if factor_df is None or factor_df.empty:
        return
    df = _normalize_factor_frame(factor_df)
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 50.0]
    df = df[df['roe'] > 0.05]
    df = df[df['inc_net_profit_year_on_year'] > 0.0]
    df = df.head(context.stock_num * 5)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    candidates = list(df.index)
    # 加入动量因子
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 61, '1d', 'close')
            if closes is None or len(closes) < 61:
                continue
            momentum = closes[-1] / closes[0] - 1
            pe = df.loc[stock, 'pe_ratio'] if stock in df.index else 30
            roe = df.loc[stock, 'roe'] if stock in df.index else 0
            growth = df.loc[stock, 'inc_net_profit_year_on_year'] if stock in df.index else 0
            # 综合评分
            scores[stock] = momentum * 0.3 + roe / 100 * 0.4 + growth / 100 * 0.3
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

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

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
