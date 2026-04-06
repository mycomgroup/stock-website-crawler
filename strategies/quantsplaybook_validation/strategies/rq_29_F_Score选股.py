# F_Score选股策略 - RiceQuant版本
# 原文：F_Score 选股，年化80%+
# 原文：https://www.joinquant.com/post/31359
# 注：原版用 get_money_flow 获取资金流，RQ不支持，改用基本面财务评分
# 逻辑：Piotroski F-Score 9项财务指标评分，选高分股票

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.top_n = 10
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    stocks = index_components(context.index)
    if not stocks:
        return

    context.week = current_week

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['roa'] > 0.0]
        df = df[df['operating_cash_flow'] > 0.0]
        df = df[df['inc_revenue_year_on_year'] > 0.0]
        df = df[df['inc_net_profit_year_on_year'] > 0]
        df = df[df['debt_asset_ratio'] < 60.0]
        df = df.head(context.stock_num * 3)
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