# Auto-generated alias for placeholder rq_25 冷饭热吃之三，14年至今年华99.99%.txt
# Reuses migrated RiceQuant implementation from rq_25_冷饭热吃小市值.py
# Shared original URL: https://www.joinquant.com/post/47527

# 冷饭热吃之三小市值策略 - RiceQuant版本
# 原文：冷饭热吃之三，14年至今年华99.99%
# 作者：韶华不负
# 原文：https://www.joinquant.com/post/47527
# 逻辑：中小板小市值，4月空仓，周二调仓，持仓7只，有止损

import numpy as np


def init(context):
    context.stock_num = 7
    context.pass_months = [4]
    context.etf_cash = '511880.XSHG'
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return
    context.week = current_week

    # 空仓月份
    if context.now.month in context.pass_months:
        for stock in list(context.portfolio.positions.keys()):
            if stock != context.etf_cash:
                order_target_value(stock, 0)
        order_target_value(context.etf_cash, context.portfolio.total_value * 0.95)
        return

    # 止损：中小指跌幅>6%或单票跌幅>12%
    index_prices = history_bars('399101.XSHE', 2, '1d', 'close')
    if index_prices is not None and len(index_prices) >= 2:
        index_change = index_prices[-1] / index_prices[-2] - 1
        if index_change < -0.06:
            for stock in list(context.portfolio.positions.keys()):
                order_target_value(stock, 0)
            return

    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if pos and bar and bar.close / pos.avg_cost - 1 < -0.12:
            order_target_value(stock, 0)

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
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
        df = df[df['market_cap'] > 3e8]
        df = df[df['market_cap'] < 5e+09]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading and bar.close <= 100:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    if context.etf_cash in context.portfolio.positions:
        order_target_value(context.etf_cash, 0)

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)