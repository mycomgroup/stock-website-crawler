# 处置效应因子（CGO）选股策略 - RiceQuant版本
# 来源：《处置效应因子：资本利得突出量CGO与风险偏好》
# 核心逻辑：CGO = (当前价格 - 参考价格) / 参考价格
#           参考价格为过去N日换手率加权平均成本
#           CGO高（浮盈大）时，投资者倾向卖出，股价承压；CGO低时反弹

import numpy as np


def calc_cgo(prices, turnovers, window=52):
    """
    计算资本利得突出量 CGO
    参考价格 = 换手率加权的历史均价
    """
    if len(prices) < window or len(turnovers) < window:
        return None

    p = np.array(prices[-window:], dtype=float)
    tr = np.array(turnovers[-window:], dtype=float)
    current_price = p[-1]

    # 换手率加权参考价格
    tr_sum = tr.sum()
    if tr_sum == 0:
        return None

    ref_price = np.average(p, weights=tr)
    cgo = (current_price - ref_price) / ref_price

    return cgo


def init(context):
    context.index = '000905.XSHG'   # 中证500
    context.window = 52              # 约一季度
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
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            turnovers = history_bars(stock, context.window, '1d', 'turnover_rate')
            if prices is None or turnovers is None:
                continue
            cgo = calc_cgo(
                np.array(prices, dtype=float),
                np.array(turnovers, dtype=float),
                context.window
            )
            if cgo is not None:
                # 选CGO低的股票（浮亏多，处置效应导致持有，未来反弹）
                scores[stock] = -cgo
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
