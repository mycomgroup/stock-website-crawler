# 处置效应因子（CGO）选股策略 - RiceQuant版本
# 来源：《处置效应因子：资本利得突出量CGO与风险偏好》
# 核心逻辑：CGO = (当前价格 - VWAP参考价) / VWAP参考价
#           CGO低（浮亏多）时，处置效应导致持有不卖，未来反弹
# 修复：
#   1. 月度调仓失败时不更新 month，下个 bar 重试
#   2. 加强数据校验，避免静默失败

import numpy as np


def calc_cgo(prices, volumes, window=52):
    """CGO = (当前价 - VWAP) / VWAP"""
    p = np.array(prices[-window:], dtype=float)
    vol = np.array(volumes[-window:], dtype=float)

    vol_sum = vol.sum()
    if vol_sum == 0:
        return None

    ref_price = np.average(p, weights=vol)
    if ref_price == 0:
        return None

    return (p[-1] - ref_price) / ref_price


def init(context):
    context.index = '000905.XSHG'   # 中证500
    context.window = 52
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    if context.month == -1:
        print(f"[33] 首次运行: {context.now}")
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components(context.index)
    if not stocks or len(stocks) < 10:
        return  # 不更新 month，重试

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            volumes = history_bars(stock, context.window + 1, '1d', 'volume')
            if prices is None or len(prices) < context.window + 1:
                continue
            if volumes is None or len(volumes) < context.window + 1:
                continue

            p = np.array(prices, dtype=float)
            v = np.array(volumes, dtype=float)
            if p[-1] == 0:
                continue

            cgo = calc_cgo(p, v, context.window)
            if cgo is not None:
                scores[stock] = -cgo  # CGO 越低越好
        except Exception:
            continue

    if not scores:
        return  # 不更新 month，重试

    context.month = current_month

    target = sorted(scores, key=scores.get, reverse=True)[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
