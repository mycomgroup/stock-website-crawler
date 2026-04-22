# 7年40倍绩优低价超跌缩量小盘策略（扩容50只）- RiceQuant版本
# 原文：7年40倍绩优低价超跌缩量小盘 扩容到50只
# 作者：wywy1995
# 原文：https://www.joinquant.com/post/39960
# 逻辑：全市场选小市值、低价、ROE高的股票，周度调仓，持仓50只

import numpy as np


def init(context):
    context.stock_num = 50
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
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 500000000]
        df = df[df['market_cap'] < 100000000]
        df = df[df['pb_ratio'] > 0.01]
        df = df[df['pb_ratio'] < 20.0]
        df = df[df['roe'] > 0.05]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        candidates = list(df.index)
    except Exception:
        return
    # 过滤低价股（<2元）和高价股（>50元）
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if 2 <= bar.close <= 50:
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
