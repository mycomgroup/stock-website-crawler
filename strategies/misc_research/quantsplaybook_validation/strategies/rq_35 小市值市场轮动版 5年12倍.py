# 原文链接：https://www.joinquant.com/post/小市值市场轮动版5年12倍
# 策略：小市值市场轮动版 5年12倍
# 核心逻辑：小市值+市场动量轮动，大盘上涨时持有小市值，下跌时切换到债券ETF。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.bond_etf = '511010.XSHG'
    context.index_etf = '510300.XSHG'
    context.momentum_n = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 市场动量判断
    prices = history_bars(context.index_etf, context.momentum_n + 1, '1d', 'close')
    if len(prices) < context.momentum_n + 1:
        return
    market_momentum = (prices[-1] - prices[0]) / prices[0]

    if market_momentum < -0.03:
        # 大盘下跌，切换债券ETF
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info(f"大盘动量={market_momentum:.2%}，切换债券ETF")
        return

    # 大盘上涨，持有小市值股票
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 5000000000]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 60.0]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]

    if context.bond_etf in context.portfolio.positions:
        order_target_value(context.bond_etf, 0)

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
    logger.info(f"大盘动量={market_momentum:.2%}，持有小市值: {target}")
