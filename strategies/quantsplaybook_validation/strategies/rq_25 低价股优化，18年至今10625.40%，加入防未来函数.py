# Auto-generated alias for placeholder rq_25 低价股优化，18年至今10625.40%，加入防未来函数.txt
# Reuses migrated RiceQuant implementation from rq_25_低价股优化.py
# Shared original URL: https://www.joinquant.com/post/40992

# 低价股优化策略 - RiceQuant版本
# 原文：低价股优化，18年至今10625.40%，已加防未来函数
# 原文：https://www.joinquant.com/post/40992
# 逻辑：全市场低价股（<5元），小市值，周度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.max_price = 5.0
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 500000000]
        df = df[df['market_cap'] < 300000000]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        candidates = list(df.index)
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if bar.close <= context.max_price:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.week = current_week

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
