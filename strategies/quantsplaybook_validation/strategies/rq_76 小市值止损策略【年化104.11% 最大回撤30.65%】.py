# 小市值止损策略 - RiceQuant版本
# 逻辑：小市值每日再平衡，加入止损机制

import numpy as np

def init(context):
    context.n_position = 50
    context.stop_loss_pct = -0.1
    context.choice = []
    context.position_size = 0
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    scheduler.run_daily(i_update, time_rule=market_open(minute=0))
    scheduler.run_daily(i_trader, time_rule=market_open(minute=35))
    scheduler.run_daily(stop_loss_check, time_rule=market_open(minute=210))

def i_update(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    factor_df = get_factor(
        stock_ids,
        ['market_cap']
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    if not hasattr(df, 'columns'):
        df = df.to_frame(name='market_cap')
    df = df[df['market_cap'] > 0]
    df = df.sort_values('market_cap').head(context.n_position * 2)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    context.choice = [s for s in candidates if s in bar_dict and bar_dict[s].is_trading][:context.n_position]
    context.position_size = (1.0 / context.n_position) * context.portfolio.total_value

def i_trader(context, bar_dict):
    if not context.choice:
        return
    for s in list(context.portfolio.positions.keys()):
        if s not in context.choice:
            bar = (bar_dict[s] if s in bar_dict else None)
            if bar and bar.is_trading:
                order_target_value(s, 0)
    for s in context.choice:
        if context.portfolio.cash < context.position_size:
            break
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        pos = context.portfolio.positions.get(s)
        if pos is None:
            order_target_value(s, context.position_size)

def stop_loss_check(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        if pos.avg_price > 0 and bar.close / pos.avg_price - 1 < context.stop_loss_pct:
            order_target_value(stock, 0)

def handle_bar(context, bar_dict):
    pass
