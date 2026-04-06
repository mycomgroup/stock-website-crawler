# 中小综指数增强策略 - RiceQuant版本
# 来源：28 【回顾2】小市值成长股策略更新
# 逻辑：在中证500成分股中，选市值小、ROE高、净利润增速高的成长股，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    # 中证500成分股（RiceQuant中中小综指399101可能不可用，用中证500替代）
    stocks = index_components('000905.XSHG')
    if not stocks or len(stocks) < 10:
        instruments_df = all_instruments('CS')
        stocks = instruments_df['order_book_id'].tolist()
        stocks = [s for s in stocks if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 5e+08]
        df = df[df['market_cap'] < 2e+10]
        df = df[df['roe'] > 0.05]
        df = df[df['inc_net_profit_year_on_year'] > 0]
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

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
