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


# 一创PEG+EBIT+换手率波动率策略 - RiceQuant版本
# 原文：一创PEG+EBIT+turnover_volatility
# 逻辑：综合PEG（成长性）、EBIT/EV（盈利质量）、换手率波动率（流动性）多因子选股

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

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['roe'] > 0.0]
        df = df[df['inc_net_profit_year_on_year'] > 0.0]
        df = df.head(context.stock_num * 5)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        candidates = list(df.index)
    except Exception:
        return
    # 换手率波动率因子（用成交量波动率代理）
    scores = {}
    for stock in candidates[:context.stock_num * 3]:
        try:
            volumes = history_bars(stock, 20, '1d', 'volume')
            if volumes is None or len(volumes) < 20:
                scores[stock] = 0
                continue
            vol_std = np.std(volumes) / (np.mean(volumes) + 1e-10)
            scores[stock] = -vol_std  # 换手率波动小的优先
        except Exception:
            scores[stock] = 0

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
