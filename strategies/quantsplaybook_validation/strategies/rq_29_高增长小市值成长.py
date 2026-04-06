# 高增长业绩股池小市值成长型策略 - RiceQuant版本
# 原文：高增股池小市值轮动
# 作者：倚A听风雨
# 原文：https://www.joinquant.com/post/45110
# 逻辑：选高增长+小市值股票，4月空仓，周度调仓，持仓10只

import numpy as np


def init(context):
    context.total_stock_num = 10
    context.pass_months = [4]
    context.etf_cash = '511880.XSHG'
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    # 4月空仓
    if context.now.month in context.pass_months:
        for stock in list(context.portfolio.positions.keys()):
            if stock != context.etf_cash:
                order_target_value(stock, 0)
        order_target_value(context.etf_cash, context.portfolio.total_value * 0.95)
        return

    if context.etf_cash in context.portfolio.positions:
        order_target_value(context.etf_cash, 0)

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 3e8]   # NOTE: RQ market_cap is yuan (元), JQ was 亿
        df = df[df['market_cap'] < 1e10]
        df = df[df['inc_net_profit_year_on_year'] > 0.2]  # NOTE: RQ is decimal, JQ was percent
        df = df[df['inc_revenue_year_on_year'] > 0.10]
        df = df[df['roe'] > 0.08]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.total_stock_num:
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