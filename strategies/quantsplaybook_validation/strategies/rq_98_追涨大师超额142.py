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


# 追涨大师超额142策略 - RiceQuant版本
# 逻辑：选近20日涨幅最大（动量最强）的小市值股票，周度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.last_week_date = None


def handle_bar(context, bar_dict):
    week_key = f"{context.now.year}-{context.now.isocalendar()[1]}"
    if context.now.isoweekday() != 1 or week_key == context.last_week_date:
        return

    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']

    all_stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 5]
        df = df[df['market_cap'] < 100]
        df = df.sort_values('market_cap')
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            scores[stock] = closes[-1] / closes[0] - 1
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    # 只选近期正收益的
    target = [s for s in sorted_stocks
              if scores[s] > 0 and (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    context.last_week_date = week_key

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
