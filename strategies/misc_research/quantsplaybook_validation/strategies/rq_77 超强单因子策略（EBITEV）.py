# 超强单因子策略（EBIT/EV）- RiceQuant版本
# 原文：https://www.joinquant.com/post/24809
# 作者：许志强
# 注：RQ无直接EBIT/EV因子，用盈利收益率(1/pe_ratio)作为近似

import numpy as np
import pandas as pd


def init(context):
    context.hold_num = 20
    context.min_market_cap = 10e8
    context.last_month = -1
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def get_universe():
    all_stocks = [
        s
        for s in all_instruments('CS')['order_book_id'].tolist()
        if not s.startswith('688')
        and not s.startswith('4')
        and not s.startswith('8')
    ]
    return all_stocks


def get_stock_list(context):
    stocks = get_universe()
    if not stocks:
        return []

    try:
        prev_date = context.now.date()
        factor_df = get_factor(all_stocks, ['market_cap', 'pe_ratio', 'earnings_yield'])
        if factor_df is None or len(factor_df) == 0:
            return []
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return []

        df = df[
            (df['pe_ratio'] > 0) &
            (df['market_cap'] > context.min_market_cap)
        ]

        if len(df) == 0:
            return []

        df['earnings_yield'] = 1.0 / df['pe_ratio']
        df = df.sort_values('earnings_yield', ascending=False)

        return list(df.index[: context.hold_num])
    except Exception:
        return []


def trade(context, bar_dict):
    if context.now.month == context.last_month:
        return
    context.last_month = context.now.month

    target = get_stock_list(context)
    if not target:
        return

    target = [s for s in target if s in bar_dict and bar_dict[s].is_trading]
    if not target:
        return

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    w = 1.0 / len(target)
    for s in target:
        order_target_value(s, context.portfolio.total_value * w * 0.95)
