# 国九小市值策略 - RiceQuant版本
# 原文：国九小市值策略【年化100.5%|回撤25.6%】
# 作者：zycash
# 原文：https://www.joinquant.com/post/47791
# 逻辑：中小板小市值，过滤净利润为负、营收<1亿的股票，周度调仓，持仓4只
# 注：国九条过滤逻辑用基本面指标近似

import numpy as np


def init(context):
    context.stock_num = 4
    context.etf_cash = '511880.XSHG'  # 空仓时持有货币基金
    context.pass_months = [1, 4]      # 空仓月份
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    # 空仓月份
    if context.now.month in context.pass_months:
        for stock in list(context.portfolio.positions.keys()):
            if stock != context.etf_cash:
                order_target_value(stock, 0)
        order_target_value(context.etf_cash, context.portfolio.total_value * 0.95)
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe', 'net_profit'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 500000000]
        df = df[df['market_cap'] < 500000000]
        df = df[df['net_profit'] > 0.0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        df = df.head(context.stock_num * 3)
        candidates = list(df.index)
    except Exception:
        return
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if bar.close <= 50:  # 股价上限
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.week = current_week

    # 清空货币基金
    if context.etf_cash in context.portfolio.positions:
        order_target_value(context.etf_cash, 0)

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
