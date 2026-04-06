# 原文链接：https://www.joinquant.com/post/58002
# 策略：韶华研究之四_菲阿里四阶在T+1的短线策略应用
# 核心逻辑：菲阿里四阶，用价格区间（前日高低点）判断今日买卖点，T+1短线。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.etf = '510300.XSHG'  # 沪深300ETF
    context.in_market = False
    context.entry_price = 0
    # 菲阿里四阶关键价位
    context.pivot = 0
    context.r1 = 0
    context.s1 = 0
    scheduler.run_daily(calc_levels, time_rule=market_open(minute=1))
    scheduler.run_daily(trade_morning, time_rule=market_open(minute=30))
    scheduler.run_daily(trade_close, time_rule=market_open(minute=225))  # 14:45

def handle_bar(context, bar_dict):
    pass

def calc_levels(context, bar_dict):
    """计算菲阿里四阶关键价位"""
    highs = history_bars(context.etf, 2, '1d', 'high')
    lows = history_bars(context.etf, 2, '1d', 'low')
    closes = history_bars(context.etf, 2, '1d', 'close')
    if highs is None or lows is None or closes is None or len(highs) < 2:
        return
    prev_high = highs[-2]
    prev_low = lows[-2]
    prev_close = closes[-2]
    # 菲阿里轴心点
    context.pivot = (prev_high + prev_low + prev_close) / 3
    context.r1 = 2 * context.pivot - prev_low   # 阻力位1
    context.s1 = 2 * context.pivot - prev_high  # 支撑位1

def trade_morning(context, bar_dict):
    """早盘交易"""
    if context.etf not in bar_dict:
        return
    price = bar_dict[context.etf].close
    if price <= 0 or context.pivot <= 0:
        return

    # 价格突破轴心点上方买入
    if not context.in_market and price > context.pivot:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.in_market = True
        context.entry_price = price
        logger.info(f"菲阿里买入，价格={price:.3f}，轴心={context.pivot:.3f}")
    # 价格跌破支撑位止损
    elif context.in_market and price < context.s1:
        order_target_value(context.etf, 0)
        context.in_market = False
        logger.info(f"菲阿里止损，价格={price:.3f}，支撑={context.s1:.3f}")

def trade_close(context, bar_dict):
    """尾盘T+1平仓"""
    if context.in_market:
        order_target_value(context.etf, 0)
        context.in_market = False
        logger.info("菲阿里尾盘平仓")
