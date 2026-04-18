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


# 科技与狠活策略 - RiceQuant版本
# 逻辑：选科技板块（电子、计算机、通信）小市值高成长股，月度调仓

import numpy as np


def init(context):
    context.stock_num = 15
    context.month = -1
    # 科技相关指数成分股
    context.tech_indices = ['399673.XSHE', '000688.XSHG']  # 创业板50、科创50


def handle_bar(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    current_month = context.now.month
    if current_month == context.month:
        return

    # 从科技指数获取股票池
    pool = []
    for idx in context.tech_indices:
        try:
            comps = index_components(idx)
            if comps:
                pool.extend(comps)
        except Exception:
            pass

    if not pool:
        instruments_df = all_instruments('CS')
        pool = [s for s in stock_ids
                if s.startswith(('300', '688'))]

    pool = list(set(pool))

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stock_ids,
            ['market_cap', 'pe_ratio', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['inc_net_profit_year_on_year'] > 0.05]
        df = df[df['roe'] > 0.08]
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
