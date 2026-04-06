# 原文链接：https://www.joinquant.com/post/51001
# 策略：缠论交易策略
# 核心逻辑：缠论简化版，用MACD金叉/死叉+MA20判断买卖点，持有沪深300ETF(510300)。

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
    price = closes[-1]

    # 缠论买点：MACD金叉（DIF上穿DEA）且价格在MA20上方
    macd_cross_up = dif[-2] < dea[-2] and dif[-1] > dea[-1]
    # 缠论卖点：MACD死叉（DIF下穿DEA）或价格跌破MA20
    macd_cross_down = dif[-2] > dea[-2] and dif[-1] < dea[-1]

    if not context.in_market and macd_cross_up and price > ma20:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.in_market = True
        logger.info(f"缠论买点，买入 {context.etf}，价格={price:.3f}")
    elif context.in_market and (macd_cross_down or price < ma20 * 0.98):
        order_target_value(context.etf, 0)
        context.in_market = False
        logger.info(f"缠论卖点，清仓 {context.etf}，价格={price:.3f}")
