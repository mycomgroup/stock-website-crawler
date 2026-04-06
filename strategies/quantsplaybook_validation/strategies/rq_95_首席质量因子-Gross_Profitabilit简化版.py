# 首席质量因子-Gross Profitability（简化版）- RiceQuant版本
# 原文：首席质量因子-Gross Profitabilit（简化版）
# 逻辑：Novy-Marx毛利率因子（GP/A），选毛利率高的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1
    scheduler.run_daily(trade_open, time_rule=market_open(minute=0))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=0))


def handle_bar(context, bar_dict):
    pass


def trade_open(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe', 'gross_profit_margin'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 2e+09]
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['gross_profit_margin'] > 0.2]
        df = df[df['roe'] > 0.05]
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


def after_market_close(context, bar_dict):
    pass
