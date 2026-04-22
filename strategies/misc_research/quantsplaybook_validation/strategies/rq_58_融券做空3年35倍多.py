# 原文链接：https://www.joinquant.com/post/58001
# 策略：融券做空3年35倍多
# 核心逻辑：用沪深300ETF做多/空仓切换（无融券），MACD择时，趋势向上持多，向下空仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def init(context):
    context.etf = '510300.XSHG'  # 沪深300ETF
    context.in_market = False
    scheduler.run_daily(trade, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def trade(context, bar_dict):
    closes = history_bars(context.etf, 60, '1d', 'close')
    if closes is None or len(closes) < 40:
        return

    dif, dea, macd = calc_macd(closes)
    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else np.mean(closes)
    price = closes[-1]

    # 趋势向上：DIF>DEA且DIF>0且价格>MA20
    trend_up = dif[-1] > dea[-1] and dif[-1] > 0 and price > ma20

    # 趋势向下：DIF<DEA且DIF<0
    trend_down = dif[-1] < dea[-1] and dif[-1] < 0

    if not context.in_market and trend_up:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.in_market = True
        logger.info(f"MACD趋势向上，买入 {context.etf}，价格={price:.3f}")
    elif context.in_market and trend_down:
        order_target_value(context.etf, 0)
        context.in_market = False
        logger.info(f"MACD趋势向下，清仓 {context.etf}，价格={price:.3f}")
