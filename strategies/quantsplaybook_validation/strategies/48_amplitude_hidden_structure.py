# 振幅因子的隐藏结构选股策略 - RiceQuant版本
# 来源：《振幅因子的隐藏结构》
# 核心逻辑：振幅 = (high - low) / prev_close
#           分解振幅为"跳空振幅"（gap）和"日内振幅"（intraday）
#           跳空振幅高 → 信息不对称，未来收益低；日内振幅高 → 流动性好

import numpy as np


def calc_amplitude_factors(opens, highs, lows, closes, window=20):
    """
    分解振幅因子
    - 总振幅 = (high - low) / prev_close
    - 跳空振幅 = |open - prev_close| / prev_close
    - 日内振幅 = (high - low) / open
    """
    if len(closes) < window + 1:
        return None, None, None

    o = np.array(opens[-window:], dtype=float)
    h = np.array(highs[-window:], dtype=float)
    l = np.array(lows[-window:], dtype=float)
    c_prev = np.array(closes[-window-1:-1], dtype=float)
    c_curr = np.array(closes[-window:], dtype=float)

    valid = c_prev > 0

    # 总振幅
    total_amp = np.where(valid, (h - l) / c_prev, 0)
    # 跳空振幅
    gap_amp = np.where(valid, np.abs(o - c_prev) / c_prev, 0)
    # 日内振幅
    intraday_amp = np.where(o > 0, (h - l) / o, 0)

    return np.mean(total_amp), np.mean(gap_amp), np.mean(intraday_amp)


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
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            opens = history_bars(stock, context.window, '1d', 'open')
            highs = history_bars(stock, context.window, '1d', 'high')
            lows = history_bars(stock, context.window, '1d', 'low')
            closes = history_bars(stock, context.window + 1, '1d', 'close')
            if any(x is None for x in [opens, highs, lows, closes]):
                continue

            total_amp, gap_amp, intraday_amp = calc_amplitude_factors(
                np.array(opens), np.array(highs),
                np.array(lows), np.array(closes),
                context.window
            )
            if total_amp is None:
                continue

            # 低跳空振幅（信息对称）+ 高日内振幅（流动性好）
            scores[stock] = -gap_amp + intraday_amp * 0.5
        except Exception:
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
