# 原文链接：https://www.joinquant.com/post/蛇皮走位小市值策略V1.0
# 策略：蛇皮走位小市值策略V1.0
# 核心逻辑：小市值+低PE+换手率适中，每周调仓，持仓10只。

import numpy as np

def init(context):
    context.n_stocks = 10
    scheduler.run_weekly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'turnover_ratio'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 40.0]
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 5000000000]
    df = df[df['turnover_ratio'] > 1.0]
    df = df[df['turnover_ratio'] < 10.0]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"蛇皮走位小市值调仓完成，持仓: {target}")
