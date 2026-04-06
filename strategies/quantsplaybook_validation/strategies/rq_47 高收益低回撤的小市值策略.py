# 原文链接：https://www.joinquant.com/post/高收益低回撤的小市值策略
# 策略：高收益低回撤的小市值策略
# 核心逻辑：小市值+低PE+MACD趋势过滤，月度调仓，持仓15只。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def init(context):
    context.n_stocks = 15
    context.bond_etf = '511010.XSHG'
    context.index_etf = '510300.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # MACD趋势过滤
    prices = history_bars(context.index_etf, 40, '1d', 'close')
    if len(prices) < 30:
        return
    dif, dea, macd = calc_macd(prices)

    if macd[-1] < 0 and dif[-1] < dea[-1]:
        # MACD死叉，持债
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info("MACD死叉，持债")
        return

    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 40.0]
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 6000000000]
    df = df[df['roe'] > 0.08]
    df = df.head(context.n_stocks + 10)
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
    logger.info(f"MACD过滤小市值调仓完成，持仓: {target}")
