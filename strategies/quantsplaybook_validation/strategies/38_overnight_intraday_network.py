# 基于隔夜与日间网络关系因子选股策略 - RiceQuant版本
# 来源：《基于隔夜与日间的网络关系因子》
# 核心逻辑：隔夜收益（close-to-open）与日间收益（open-to-close）的比值
#           隔夜收益高代表机构/信息优势，日间收益高代表散户追涨
#           选择隔夜收益占比高的股票

import numpy as np


def calc_overnight_ratio(opens, closes, window=20):
    """
    计算隔夜收益占比
    隔夜收益 = open[t] / close[t-1] - 1
    日间收益 = close[t] / open[t] - 1
    """
    if len(opens) < window + 1 or len(closes) < window + 1:
        return None

    o = np.array(opens[-window:], dtype=float)
    c_prev = np.array(closes[-window-1:-1], dtype=float)
    c_curr = np.array(closes[-window:], dtype=float)

    # 隔夜收益
    overnight = o / c_prev - 1
    # 日间收益
    intraday = c_curr / o - 1

    # 避免除零
    total_abs = np.abs(overnight) + np.abs(intraday)
    valid = total_abs > 0.001

    if valid.sum() == 0:
        return None

    # 隔夜收益占比（绝对值）
    overnight_ratio = np.mean(
        np.abs(overnight[valid]) / total_abs[valid]
    )

    # 隔夜方向性（正隔夜收益占比）
    overnight_direction = np.mean(overnight > 0)

    return overnight_ratio * overnight_direction


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
            opens = history_bars(stock, context.window + 1, '1d', 'open')
            closes = history_bars(stock, context.window + 1, '1d', 'close')
            if opens is None or closes is None:
                continue
            factor = calc_overnight_ratio(
                np.array(opens), np.array(closes), context.window
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
