# 原文链接：https://www.joinquant.com/post/35463
# 策略：缠论交易策略
# 作者：quancker
# 核心逻辑：基于缠论笔/段识别，用MACD辅助判断买卖点
# 注：原版缠论类结构复杂，此处实现核心的MACD+均线缠论简化版

import numpy as np

SECURITY = '000300.XSHG'   # 沪深300指数
ETF = '510300.XSHG'        # 对应ETF


def ema(prices, period):
    result = []
    k = 2.0 / (period + 1)
    e = prices[0]
    for p in prices:
        e = p * k + e * (1 - k)
        result.append(e)
    return np.array(result)


def calc_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    diff = ema_fast - ema_slow
    dea  = ema(diff, signal)
    macd = (diff - dea) * 2
    return diff, dea, macd


def init(context):
    context.security = SECURITY
    context.etf = ETF
    context.pos = False
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    prices = history_bars(context.security, 60, '1d', 'close')
    if prices is None or len(prices) < 40:
        return

    p = np.array(prices, dtype=float)
    diff, dea, macd = calc_macd(p)

    # 缠论简化：用MACD金叉/死叉 + 价格在MA20上下判断买卖
    ma20 = np.mean(p[-20:])
    current = p[-1]

    # 买入信号：MACD金叉（diff上穿dea）且价格在MA20上方
    macd_cross_up = diff[-1] > dea[-1] and diff[-2] <= dea[-2]
    # 卖出信号：MACD死叉（diff下穿dea）或价格跌破MA20
    macd_cross_down = diff[-1] < dea[-1] and diff[-2] >= dea[-2]

    if macd_cross_up and current > ma20 and not context.pos:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"[缠论] 买入 MACD金叉 price={current:.2f} MA20={ma20:.2f}")
    elif (macd_cross_down or current < ma20 * 0.98) and context.pos:
        order_target_value(context.etf, 0)
        context.pos = False
        print(f"[缠论] 卖出 price={current:.2f} MA20={ma20:.2f}")
