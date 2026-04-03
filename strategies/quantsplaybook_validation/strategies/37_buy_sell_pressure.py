# 基于量价关系度量买卖压力选股策略 - RiceQuant版本
# 来源：《基于量价关系度量股票的买卖压力》
# 核心逻辑：用日内价格位置（收盘价在高低价区间的位置）加权成交量
#           衡量买方压力（BP）和卖方压力（SP），BP-SP为净买压因子

import numpy as np


def calc_buy_sell_pressure(highs, lows, closes, volumes, window=20):
    """
    净买压因子 = 买方压力 - 卖方压力
    买方压力 BP = sum(volume * (close - low) / (high - low))
    卖方压力 SP = sum(volume * (high - close) / (high - low))
    """
    if len(closes) < window:
        return None

    h = np.array(highs[-window:], dtype=float)
    l = np.array(lows[-window:], dtype=float)
    c = np.array(closes[-window:], dtype=float)
    v = np.array(volumes[-window:], dtype=float)

    hl_range = h - l
    # 避免除零
    valid = hl_range > 0

    bp = np.where(valid, v * (c - l) / hl_range, 0).sum()
    sp = np.where(valid, v * (h - c) / hl_range, 0).sum()

    total = bp + sp
    if total == 0:
        return None

    # 归一化净买压
    net_pressure = (bp - sp) / total
    return net_pressure


def init(context):
    context.index = '000300.XSHG'
    context.window = 20
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    stocks = index_components(context.index)
    stocks = [s for s in stocks if s in bar_dict]

    scores = {}
    for stock in stocks:
        try:
            highs = history_bars(stock, context.window, '1d', 'high')
            lows = history_bars(stock, context.window, '1d', 'low')
            closes = history_bars(stock, context.window, '1d', 'close')
            volumes = history_bars(stock, context.window, '1d', 'volume')
            if any(x is None for x in [highs, lows, closes, volumes]):
                continue
            factor = calc_buy_sell_pressure(
                np.array(highs), np.array(lows),
                np.array(closes), np.array(volumes),
                context.window
            )
            if factor is not None:
                scores[stock] = factor
        except:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
