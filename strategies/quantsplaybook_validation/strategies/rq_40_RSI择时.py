# RSI择时策略 - RiceQuant版本
# 原文：RSI学习贴
# 原文：https://www.joinquant.com/post/35994
# 逻辑：用RSI指标对沪深300ETF进行择时，RSI低买高卖

import numpy as np


def calc_rsi(prices, period=6):
    """手动计算RSI"""
    if len(prices) < period + 1:
        return None
    p = np.array(prices, dtype=float)
    deltas = np.diff(p)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def init(context):
    context.security = '510300.XSHG'  # 沪深300ETF
    context.rsi_period = 6
    context.buy_threshold = 30
    context.sell_threshold = 70
    context.pos = False


def handle_bar(context, bar_dict):
    security = context.security
    prices = history_bars(security, context.rsi_period + 5, '1d', 'close')
    if prices is None or len(prices) < context.rsi_period + 1:
        return

    rsi = calc_rsi(prices, context.rsi_period)
    if rsi is None:
        return

    if rsi < context.buy_threshold and not context.pos:
        order_target_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
    elif rsi > context.sell_threshold and context.pos:
        order_target_value(security, 0)
        context.pos = False
