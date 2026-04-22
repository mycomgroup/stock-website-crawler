# 微盘400每日再平衡策略 - RiceQuant版本
# 原文：微盘400每日再平衡
# 逻辑：选全市场市值最小的400只股票，每日等权再平衡

import numpy as np


def init(context):
    context.n_choice = 120
    context.n_position = 100
    context.choice = []
    context.position_size = 0
    scheduler.run_daily(i_update, time_rule=market_open(minute=0))
    scheduler.run_daily(i_trader, time_rule=market_open(minute=35))


def i_update(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stock_ids,
            ['market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        if not hasattr(df, 'columns'):
            df = df.to_frame(name='market_cap')
        df = df[df['market_cap'] > 0]
        df = df.sort_values('market_cap').head(context.n_choice * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    context.choice = candidates[:context.n_choice]
    context.position_size = (1.0 / context.n_position) * context.portfolio.total_value


def i_trader(context, bar_dict):
    choice = context.choice
    if not choice:
        return

    position_size = context.position_size
    lm_value = 0.8 * position_size
    hm_value = 1.2 * position_size

    for s in list(context.portfolio.positions.keys()):
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if s not in choice:
            order_target_value(s, 0)

    for s in choice:
        if context.portfolio.cash < position_size:
            break
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        pos = context.portfolio.positions.get(s)
        if pos is None:
            order_target_value(s, position_size)
        elif pos.market_value < lm_value:
            order_target_value(s, position_size)
        elif pos.market_value > hm_value:
            order_target_value(s, position_size)


def handle_bar(context, bar_dict):
    pass
