# 低开买入小市值策略 - RiceQuant版本
# 原文：低开买入小市值策略（剥头皮策略）3.0 总结
# 逻辑：选小市值股票，当日低开（开盘价低于昨收）时买入，日内反弹卖出

import numpy as np


def init(context):
    context.stock_num = 5
    context.month = -1
    context.candidates = []
    context.last_update_week = -1
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))


def update_pool(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.last_update_week:
        return
    context.last_update_week = current_week

    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
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
        # Sort by market_cap ascending (smallest first), take top candidates
        df = df.sort_values('market_cap', ascending=True)
        df = df.head(context.stock_num * 3)
        context.candidates = df.index.tolist()  # FIX: assign to context.candidates
    except Exception:
        return


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    if not context.candidates:
        return

    # 卖出持仓
    for stock in list(context.portfolio.positions.keys()):
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(stock, 0)

    # 选低开股票买入
    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        closes = history_bars(stock, 2, '1d', 'close')
        if closes is None or len(closes) < 2:
            continue
        # 低开：当前价低于昨收1%以上
        if bar.open < closes[-2] * 0.99:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
