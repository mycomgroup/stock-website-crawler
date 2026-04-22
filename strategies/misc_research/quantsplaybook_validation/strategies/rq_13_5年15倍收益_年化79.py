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


# 5年15倍收益年化79策略 - RiceQuant版本
# 逻辑：小市值 + 高ROE + 低PB + 动量，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

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
        df = df[df['pb_ratio'] > 0]
        df = df[df['pb_ratio'] < 4]
        df = df[df['market_cap'] > 500000000.0]
        df = df[df['market_cap'] < 10000000000]
        df = df[df['roe'] > 0.10]
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            momentum = closes[-1] / closes[0] - 1
            roe = df.loc[stock, 'roe'] if stock in df.index else 0
            pb = df.loc[stock, 'pb_ratio'] if stock in df.index else 5
            scores[stock] = momentum * 0.4 + (roe / 100) * 0.4 - (pb / 10) * 0.2
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
