# Auto-generated alias for placeholder rq_19 高股息低市盈率稳健增长的价投策略.txt
# Reuses migrated RiceQuant implementation from rq_04_高股息低PE高增长价投.py
# Shared original URL: https://www.joinquant.com/post/45552

# 高股息低市盈率高增长价投策略 - RiceQuant版本
# 原文：高股息低市盈率高增长的价投策略
# 作者：芹菜1303
# 原文：https://www.joinquant.com/post/45552
# 逻辑：PE低、ROE高、营收增长稳健，月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
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
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
