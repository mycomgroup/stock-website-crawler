# 原文链接：https://www.joinquant.com/post/北向资金A股择时策略5年16倍
# 策略：北向资金A股择时策略（5年16倍）
# 核心逻辑：用沪深港通标的的整体涨跌作为北向资金代理信号，信号向上时持有小市值股票。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.bond_etf = '511010.XSHG'
    context.proxy_etf = '510300.XSHG'  # 用沪深300ETF代理北向资金信号
    context.signal_n = 5  # 5日动量信号
    scheduler.run_daily(check_signal, time_rule=market_open(minute=5))
    scheduler.run_monthly(rebalance_stocks, tradingday=1, time_rule=market_open(minute=30))
    context.target_stocks = []

def handle_bar(context, bar_dict):
    pass

def check_signal(context, bar_dict):
    # 用沪深300近5日涨跌作为北向资金代理信号
    prices = history_bars(context.proxy_etf, context.signal_n + 1, '1d', 'close')
    if len(prices) < context.signal_n + 1:
        return
    signal = (prices[-1] - prices[-context.signal_n - 1]) / prices[-context.signal_n - 1]

    if signal < -0.02:
        # 信号弱，切换债券
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        if context.portfolio.cash > 1000:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)

def rebalance_stocks(context, bar_dict):
    # 北向信号强时，持有小市值股票
    prices = history_bars(context.proxy_etf, 6, '1d', 'close')
    signal = (prices[-1] - prices[0]) / prices[0]
    if signal < -0.02:
        return

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
    df = df[df['market_cap'] < 3000000000]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 50.0]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]
    context.target_stocks = target

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
    logger.info(f"北向信号={signal:.2%}，持仓小市值: {target}")
