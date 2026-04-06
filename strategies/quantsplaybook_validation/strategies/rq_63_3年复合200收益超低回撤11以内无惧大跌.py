# 原文链接：https://www.joinquant.com/post/63000
# 策略：3年复合200收益超低回撤11以内无惧大跌
# 核心逻辑：低回撤策略，用MACD+BOLL双重过滤，小市值+低PE选股，严格止损。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def calc_boll(p, n=20, k=2):
    ma = np.mean(p[-n:])
    std = np.std(p[-n:])
    return ma + k * std, ma, ma - k * std

def init(context):
    context.n_stocks = 10
    context.stop_loss = 0.08  # 8%止损
    context.entry_prices = {}
    context.index_etf = '510300.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(check_stop_loss, time_rule=market_open(minute=60))

def handle_bar(context, bar_dict):
    pass

def check_stop_loss(context, bar_dict):
    for s, entry in list(context.entry_prices.items()):
        if s in bar_dict and entry > 0:
            price = bar_dict[s].close
            if (entry - price) / entry > context.stop_loss:
                order_target_value(s, 0)
                context.entry_prices.pop(s, None)
                logger.info(f"止损触发: {s}，亏损={(entry-price)/entry:.2%}")

def rebalance(context, bar_dict):
    # 大盘MACD+BOLL择时
    index_closes = history_bars(context.index_etf, 60, '1d', 'close')
    if index_closes is None or len(index_closes) < 40:
        return

    dif, dea, macd = calc_macd(index_closes)
    upper, mid, lower = calc_boll(index_closes)
    market_ok = dif[-1] > dea[-1] and index_closes[-1] > mid

    if not market_ok:
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        context.entry_prices.clear()
        logger.info("大盘信号不佳，空仓")
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
    df = df[df['roe'] > 0.08]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    target = list(df.index)[:context.n_stocks]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)
            context.entry_prices.pop(s, None)

    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
            context.entry_prices[s] = bar_dict[s].close
    logger.info(f"低回撤策略调仓，持仓: {target}")
