# 原文链接：https://www.joinquant.com/post/63003
# 策略：生猪期货CTA策略
# 核心逻辑：用农业ETF(159825)代替生猪期货，MACD趋势跟踪，趋势向上持有。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def init(context):
    context.agri_etf = '159825.XSHE'  # 农业ETF（代替生猪期货）
    context.in_market = False
    context.entry_price = 0
    context.stop_loss = 0.06  # 6%止损
    scheduler.run_daily(trade, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def trade(context, bar_dict):
    closes = history_bars(context.agri_etf, 60, '1d', 'close')
    if closes is None or len(closes) < 40:
        return

    dif, dea, macd = calc_macd(closes)
    ma20 = np.mean(closes[-20:])
    price = closes[-1]

    # 止损检查
    if context.in_market and context.entry_price > 0:
        if (context.entry_price - price) / context.entry_price > context.stop_loss:
            order_target_value(context.agri_etf, 0)
            context.in_market = False
            logger.info(f"农业ETF止损，价格={price:.3f}")
            return

    # MACD趋势跟踪
    trend_up = dif[-1] > dea[-1] and dif[-1] > 0 and price > ma20
    trend_down = dif[-1] < dea[-1] and dif[-1] < 0

    if not context.in_market and trend_up:
        order_target_value(context.agri_etf, context.portfolio.total_value * 0.95)
        context.in_market = True
        context.entry_price = price
        logger.info(f"农业ETF买入，价格={price:.3f}")
    elif context.in_market and trend_down:
        order_target_value(context.agri_etf, 0)
        context.in_market = False
        logger.info(f"农业ETF卖出，价格={price:.3f}")
