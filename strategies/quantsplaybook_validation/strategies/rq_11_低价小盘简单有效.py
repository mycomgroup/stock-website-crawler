"""
RiceQuant Strategy: 低价小盘简单有效
Author: wywy1995
Clone from: https://www.joinquant.com/post/39788
Strategy: Select low-price small-cap stocks weekly.
"""

import numpy as np


def init(context):
    context.stock_num = 15
    context.candidates = []
    scheduler.run_weekly(weekly_trade, weekday=1, time_rule=market_open(minute=30))


def get_stock_list(context):
    _instr = all_instruments('CS')
    all_stocks = [s for s in _instr['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8')]

    valid = []
    now_date = context.now.date() if hasattr(context.now, 'date') else context.now
    for s in all_stocks:
        try:
            inst = instruments(s)
            listed_date = getattr(inst, 'listed_date', None)
            if inst and listed_date and (now_date - listed_date).days >= 365:
                valid.append(s)
        except Exception:
            continue

    prices = {}
    for s in valid:
        bars = history_bars(s, 1, '1d', 'close')
        if bars is not None and len(bars) > 0 and bars[-1] > 0:
            prices[s] = bars[-1]

    if not prices:
        return []

    sorted_by_price = sorted(prices, key=prices.get)
    low_price_list = sorted_by_price[:int(0.1 * len(sorted_by_price))]

    # Get market cap for low-price stocks and sort by smallest
    try:
        factor_df = get_factor(
            low_price_list,
            ['market_cap']
        )
        if factor_df is None or len(factor_df) == 0:
            return low_price_list[:context.stock_num]
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return low_price_list[:context.stock_num]
        if not hasattr(df, 'columns'):
            df = df.to_frame(name='market_cap')
        df = df[df['market_cap'] > 0]
        df = df.sort_values('market_cap', ascending=True).head(500)
        return df.index.tolist()[:context.stock_num]
    except Exception:
        return low_price_list[:context.stock_num]


def weekly_trade(context, bar_dict):
    target = get_stock_list(context)
    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        if stock in bar_dict and bar_dict[stock].is_trading:
            order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def handle_bar(context, bar_dict):
    pass
