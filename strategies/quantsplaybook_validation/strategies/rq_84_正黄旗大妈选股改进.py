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


# 正黄旗大妈选股改进版 - RiceQuant版本
# 原文：多大规模的基金收益最好？偏股基金规模研究（改进版）
# 逻辑：选低PB、高ROE、小市值的股票，加入动量过滤，月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
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
            ['pe_ratio', 'pb_ratio', 'market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 4.0]
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 40.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 2e+10]
        df = df[df['roe'] > 0.10]
        df = df[df['inc_net_profit_year_on_year'] > 0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 动量过滤：近20日正收益
    target = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            if closes[-1] > closes[0]:
                bar = (bar_dict[stock] if stock in bar_dict else None)
                if bar is None or bar.is_trading:
                    target.append(stock)
        except Exception:
            continue
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
