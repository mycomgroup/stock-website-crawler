# 原文链接：https://www.joinquant.com/post/59000
# 策略：北向RSRS与布林带择时
# 核心逻辑：RSRS+布林带双重择时，RSRS>阈值且价格在布林带中轨上方时持股。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:])
    y = np.array(high[-n:])
    b = np.polyfit(x, y, 1)
    return b[0]

def calc_boll(p, n=20, k=2):
    ma = np.mean(p[-n:])
    std = np.std(p[-n:])
    return ma + k * std, ma, ma - k * std

def init(context):
    context.etf = '510300.XSHG'
    context.rsrs_threshold = 1.0
    context.in_market = False
    scheduler.run_daily(trade, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def trade(context, bar_dict):
    closes = history_bars(context.etf, 60, '1d', 'close')
    highs = history_bars(context.etf, 30, '1d', 'high')
    lows = history_bars(context.etf, 30, '1d', 'low')

    if closes is None or highs is None or lows is None:
        return
    if len(closes) < 30 or len(highs) < 18:
        return

    rsrs = calc_rsrs(highs, lows, n=18)
    upper, mid, lower = calc_boll(closes, n=20)
    price = closes[-1]

    # 买入条件：RSRS>阈值 且 价格>布林带中轨
    buy_signal = rsrs > context.rsrs_threshold and price > mid
    # 卖出条件：RSRS<阈值 或 价格<布林带中轨
    sell_signal = rsrs < context.rsrs_threshold or price < mid * 0.99

    if not context.in_market and buy_signal:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.in_market = True
        logger.info(f"RSRS+布林带买入，RSRS={rsrs:.2f}，价格={price:.3f}，中轨={mid:.3f}")
    elif context.in_market and sell_signal:
        order_target_value(context.etf, 0)
        context.in_market = False
        logger.info(f"RSRS+布林带卖出，RSRS={rsrs:.2f}，价格={price:.3f}")
