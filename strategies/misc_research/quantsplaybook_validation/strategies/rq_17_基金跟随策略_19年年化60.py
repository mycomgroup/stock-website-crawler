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


# 基金跟随策略 - RiceQuant版本
# 逻辑：跟随公募基金重仓股（用沪深300中动量最强的股票代替），月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components('000300.XSHG')
    if not stocks:
        return

    context.month = current_month

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['roe'] > 0.10]
        candidates = df.index.tolist()
    except Exception:
        return
    # 用动量代理基金重仓（基金倾向持有近期表现好的股票）
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 61, '1d', 'close')
            if closes is None or len(closes) < 61:
                continue
            momentum = closes[-1] / closes[0] - 1
            roe = df.loc[stock, 'roe'] if stock in df.index else 0
            scores[stock] = momentum * 0.5 + (roe / 100) * 0.5
        except Exception:
            continue

    if not scores:
        return

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
