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


# 预判ST并过滤避雷策略 - RiceQuant版本
# 原文：预判st并过滤避雷代码 740（50只）
# 逻辑：选中证500成分股中，高股息、低PE、低PB的价值股，过滤ST风险，周度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.last_week_date = None


def handle_bar(context, bar_dict):
    week_key = f"{context.now.year}-{context.now.isocalendar()[1]}"
    # 周一调仓
    if context.now.weekday() == 0 and week_key != context.last_week_date:
        adjust_position(context, bar_dict)
        context.last_week_date = week_key


def adjust_position(context, bar_dict):
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
            ['pe_ratio', 'pb_ratio', 'market_cap', 'dividend_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 30.0]
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 3.0]
        df = df[df['market_cap'] > 20]
        df = df[df['dividend_ratio'] > 0.0000]
        df = df.sort_values(['dividend_ratio', 'pe_ratio', 'pb_ratio'], ascending=[False, True, True])
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and not bar.is_trading:
            continue
        # 过滤ST（名称含ST的跳过）
        inst = instruments(stock)
        if inst and ('ST' in inst.symbol or '*' in inst.symbol):
            continue
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
