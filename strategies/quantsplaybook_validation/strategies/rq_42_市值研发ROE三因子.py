# 市值+研发支出+ROE三因子策略 - RiceQuant版本
# 原文：市值，研发支出，roe，三因子，跑赢大盘
# 作者：zyljq
# 原文：https://www.joinquant.com/post/28499
# 逻辑：市值小、ROE高的股票，每15天调仓，持仓9只

import numpy as np


def init(context):
    context.top_n = 9
    context.rebal_days = 15
    context.day_count = 0


def handle_bar(context, bar_dict):
    context.day_count += 1
    if context.day_count % context.rebal_days != 0:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 0]
        df = df[df['market_cap'] < 1e+10]
        df = df[df['roe'] > 0.05]
        df = df.head(context.top_n * 3)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        candidates = df.index.tolist()
    except Exception:
        return

    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.top_n:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
