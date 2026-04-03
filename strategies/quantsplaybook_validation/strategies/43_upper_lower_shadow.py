# 上下影线因子选股策略 - RiceQuant版本
# 来源：《上下影线因子》
# 核心逻辑：
#   上影线 = (high - max(open, close)) / (high - low)  → 上方抛压
#   下影线 = (min(open, close) - low) / (high - low)   → 下方支撑
#   净影线因子 = 下影线均值 - 上影线均值
#   净影线高（下影线强）→ 支撑强，未来上涨概率高

import numpy as np


def calc_shadow_factor(opens, highs, lows, closes, window=20):
    """计算净影线因子"""
    if len(closes) < window:
        return None

    o = np.array(opens[-window:], dtype=float)
    h = np.array(highs[-window:], dtype=float)
    l = np.array(lows[-window:], dtype=float)
    c = np.array(closes[-window:], dtype=float)

    hl_range = h - l
    valid = hl_range > 0

    if valid.sum() == 0:
        return None

    # 上影线
    upper_shadow = np.where(valid, (h - np.maximum(o, c)) / hl_range, 0)
    # 下影线
    lower_shadow = np.where(valid, (np.minimum(o, c) - l) / hl_range, 0)

    # 净影线因子
    net_shadow = np.mean(lower_shadow) - np.mean(upper_shadow)
    return net_shadow


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
            opens = history_bars(stock, context.window, '1d', 'open')
            highs = history_bars(stock, context.window, '1d', 'high')
            lows = history_bars(stock, context.window, '1d', 'low')
            closes = history_bars(stock, context.window, '1d', 'close')
            if any(x is None for x in [opens, highs, lows, closes]):
                continue
            factor = calc_shadow_factor(
                np.array(opens), np.array(highs),
                np.array(lows), np.array(closes),
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
