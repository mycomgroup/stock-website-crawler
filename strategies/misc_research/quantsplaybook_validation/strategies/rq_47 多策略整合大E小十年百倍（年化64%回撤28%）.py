# 原文链接：https://www.joinquant.com/post/多策略整合大E小十年百倍年化64回撤28
# 策略：多策略整合大E小十年百倍（年化64%回撤28%）
# 核心逻辑：大盘ETF+小市值股票双策略整合，根据市场状态切换，用沪深300动量判断。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.etf = '510300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.etf_ratio = 0.4    # ETF仓位40%
    context.stock_ratio = 0.55  # 小市值仓位55%
    context.momentum_n = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 判断市场状态
    prices = history_bars(context.etf, context.momentum_n + 1, '1d', 'close')
    if len(prices) < context.momentum_n + 1:
        return
    ema20 = ema(prices, 20)
    market_up = prices[-1] > ema20[-1]
    momentum = (prices[-1] - prices[0]) / prices[0]

    if momentum < -0.05:
        # 市场大跌，全部切换债券
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info(f"市场动量={momentum:.2%}，全仓债券")
        return

    total_value = context.portfolio.total_value

    # 大盘ETF部分
    if market_up:
        order_target_value(context.etf, total_value * context.etf_ratio)
    else:
        order_target_value(context.etf, 0)

    # 小市值股票部分
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
    target_stocks = list(df.index)[:context.n_stocks]

    # 清仓不在目标中的股票
    for s in list(context.portfolio.positions.keys()):
        if s not in target_stocks and s != context.etf and s != context.bond_etf:
            order_target_value(s, 0)

    n = len(target_stocks)
    if n > 0:
        stock_value = total_value * context.stock_ratio / n
        for s in target_stocks:
            if s in bar_dict and bar_dict[s].is_trading:
                order_target_value(s, stock_value)

    logger.info(f"双策略整合：ETF={market_up}，小市值={target_stocks[:5]}")
