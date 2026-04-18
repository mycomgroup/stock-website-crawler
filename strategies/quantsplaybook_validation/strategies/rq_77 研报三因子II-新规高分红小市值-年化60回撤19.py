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


# 研报三因子II-新规高分红小市值 - RiceQuant版本
# 逻辑：高股息率 + 小市值 + 低PB，月度调仓

import numpy as np

def init(context):
    context.stock_num = 20
    context.month = -1
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
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
            ['pb_ratio', 'dividend_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0]
        df = df[df['pb_ratio'] < 3]
        df = df[df['dividend_ratio'] > 0.0200]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = [s for s in candidates if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return
    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
