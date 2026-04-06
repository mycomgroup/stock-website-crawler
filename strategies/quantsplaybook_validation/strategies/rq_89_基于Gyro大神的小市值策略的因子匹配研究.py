# 基于Gyro大神的小市值策略因子匹配研究 - RiceQuant版本
# 逻辑：小市值 + ROE>0 + PB>0 + 动量过滤，每日再平衡

import numpy as np


def init(context):
    context.n_choice = 100
    context.n_position = 50
    context.choice = []
    context.position_size = 0
    scheduler.run_daily(i_update, time_rule=market_open(minute=0))
    scheduler.run_daily(i_trader, time_rule=market_open(minute=35))


def i_update(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]

    try:
        factor_df = get_factor(
            stock_ids,
            ['pb_ratio', 'market_cap', 'roe']
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 3e+08]
        df = df[df['roe'] > 0.00]
        df = df.sort_values('market_cap').head(context.n_choice * 3)
        candidates = df.index.tolist()
    except Exception:
        context.choice = []
        return
    if not candidates:
        context.choice = []
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

    for s in choice[:context.n_position]:
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
