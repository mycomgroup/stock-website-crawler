# 低PB小市值低换手策略 - RiceQuant版本
# 原文：https://www.joinquant.com/post/35317
# 作者：QuantYY

import pandas as pd

def init(context):

    context.stock_num = 35
    context.last_month = -1

    scheduler.run_daily(trade, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def get_stock_pool(context, bar_dict):
    # Get all A-shares, filter out STAR/BSE
    all_stocks = [s for s in all_instruments('CS')['order_book_id'].tolist()
                  if not s.startswith(('688', '4', '8'))]

    # Filter ST, suspended, limit-up
    valid = []
    for stock in all_stocks:
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        if not bar.is_trading:
            continue
        inst = instruments(stock)
        if inst and inst.special_type in ('ST', '*ST'):
            continue
        valid.append(stock)

    if not valid:
        return []

    # Get factors
    today = str(context.now)
    try:
        prev_date = context.now.date()
        prev_date = context.now.date()
        factor_df = get_factor(
            all_stocks,
            ['pb_ratio', 'market_cap', 'turnover_ratio'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 0]
        df = df.head(200)
        candidates = df.index.tolist()
    except Exception:
        return []
    if df is None or len(df) == 0:
        return []
    result = set()

    # Low PB + low turnover
    pb_sorted = df.sort_values('pb_ratio').head(70)
    pb_turn = pb_sorted.sort_values('turnover_ratio').head(35)
    result.update(pb_turn.index.tolist())

    # Small cap + low turnover
    cap_sorted = df.sort_values('market_cap').head(70)
    cap_turn = cap_sorted.sort_values('turnover_ratio').head(35)
    result.update(cap_turn.index.tolist())

    return list(result)[:context.stock_num]

def trade(context, bar_dict):
    # Monthly rebalance
    if context.now.month == context.last_month:
        return
    context.last_month = context.now.month

    target = get_stock_pool(context, bar_dict)
    if not target:
        return

    # Sell
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    # Buy equal weight
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
