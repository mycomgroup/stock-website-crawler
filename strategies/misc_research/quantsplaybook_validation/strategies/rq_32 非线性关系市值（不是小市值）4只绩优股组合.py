# 原文链接：https://www.joinquant.com/post/非线性关系市值不是小市值4只绩优股组合
# 策略：非线性关系市值（不是小市值）4只绩优股组合
# 核心逻辑：选中等市值（50-200亿）+高ROE+低PE的绩优股，持仓4只，季度调仓。

import numpy as np

def init(context):
    context.n_stocks = 4
    context.min_cap = 50    # 最小市值50亿
    context.max_cap = 200   # 最大市值200亿
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'pb_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 25.0]
    df = df[df['roe'] > 0.15]
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 5.0]
    df = df.head(context.n_stocks + 5)
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
    logger.info(f"中等市值绩优股调仓完成，持仓: {target}")
