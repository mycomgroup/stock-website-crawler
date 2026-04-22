# 趋势永存策略 - RiceQuant版本
# 原文：《趋势永存》持续16年跑赢大盘的真正靠谱策略
# 作者：Ahfu
# 原文：https://www.joinquant.com/post/36489
# 逻辑：选沪深300成分股中动量强的股票，用ATR控制仓位，周度调仓
# 注：ATR 计算已用纯 numpy 实现替代 talib.ATR

import numpy as np


def calc_atr(highs, lows, closes, period):
    """纯 numpy 实现 ATR"""
    h = np.array(highs, dtype=float)
    l = np.array(lows, dtype=float)
    c = np.array(closes, dtype=float)
    tr = np.maximum(h[1:] - l[1:],
         np.maximum(np.abs(h[1:] - c[:-1]),
                    np.abs(l[1:] - c[:-1])))
    if len(tr) < period:
        return None
    return np.mean(tr[-period:])


def init(context):
    context.index = '000300.XSHG'
    context.momentum_day = 90
    context.ma_day = 100
    context.index_ma_day = 200
    context.atr_day = 20
    context.risk_factor = 0.001
    context.rank_threshold = 60
    scheduler.run_weekly(trade, weekday=3, time_rule=market_open(minute=2))


def handle_bar(context, bar_dict):
    pass


def good_market(context):
    try:
        prices = history_bars(context.index, context.index_ma_day + 1, '1d', 'close')
        if prices is None or len(prices) < context.index_ma_day + 1:
            return True
        p = np.array(prices, dtype=float)
        ma = np.mean(p[-context.index_ma_day:])
        return p[-1] > ma
    except Exception:
        return True


def get_stock_pool(context):
    stocks = index_components(context.index)
    if not stocks:
        return []

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.momentum_day + 1, '1d', 'close')
            if prices is None or len(prices) < context.momentum_day + 1:
                continue
            p = np.array(prices, dtype=float)
            ma = np.mean(p[-context.ma_day:]) if len(p) >= context.ma_day else np.mean(p)
            if p[-1] > ma:
                momentum = (p[-1] / p[0]) - 1
                scores[stock] = momentum
        except Exception:
            continue

    if not scores:
        return []
    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    cutoff = int(len(sorted_stocks) * context.rank_threshold / 100)
    return sorted_stocks[:cutoff]


def get_position_size(context, stock):
    try:
        highs = history_bars(stock, context.atr_day + 1, '1d', 'high')
        lows = history_bars(stock, context.atr_day + 1, '1d', 'low')
        closes = history_bars(stock, context.atr_day + 1, '1d', 'close')
        if any(x is None for x in [highs, lows, closes]):
            return context.portfolio.total_value * 0.05
        atr = calc_atr(highs, lows, closes, context.atr_day)
        if atr is None or atr == 0:
            return context.portfolio.total_value * 0.05
        position_value = context.portfolio.total_value * context.risk_factor / (atr / closes[-1])
        return min(position_value, context.portfolio.total_value * 0.1)
    except Exception:
        return context.portfolio.total_value * 0.05


def trade(context, bar_dict):
    stock_pool = get_stock_pool(context)
    held = set(context.portfolio.positions.keys())

    for stock in held:
        if stock not in stock_pool:
            order_target_value(stock, 0)

    if not good_market(context):
        return

    for stock in stock_pool:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        expected = get_position_size(context, stock)
        if context.portfolio.cash > expected:
            order_target_value(stock, expected)
