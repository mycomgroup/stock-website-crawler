# 筹码分布因子选股策略 - RiceQuant版本
# 来源：《根据前景理论的筹码因子构建》
# 核心逻辑：基于换手率加权计算筹码分布，构建相对资本收益（RC）均值/偏度因子
#           RC均值低（大量筹码被套）时，处置效应导致抛压大，做空；RC均值高时做多

import numpy as np


def calc_chip_distribution(prices, turnovers, window=60):
    """
    计算筹码分布的代理变量
    - prices: 收盘价序列
    - turnovers: 换手率序列
    - 返回：RC均值、RC偏度
    """
    if len(prices) < window or len(turnovers) < window:
        return None, None

    p = np.array(prices[-window:], dtype=float)
    tr = np.array(turnovers[-window:], dtype=float)
    current_price = p[-1]

    # 计算调整换手率（路径依赖）
    atr = np.zeros(window)
    atr[0] = tr[0]
    for i in range(1, window):
        atr[i] = tr[i]
        for j in range(i):
            atr[j] *= (1 - tr[i])

    # 归一化换手率
    atr_sum = atr.sum()
    if atr_sum == 0:
        return None, None
    tr_w = atr / atr_sum

    # 相对资本收益 RC = (current_price - p_n) / current_price
    rc = (current_price - p) / current_price

    # 加权均值和偏度
    rc_mean = np.average(rc, weights=tr_w)
    rc_std = np.sqrt(np.average((rc - rc_mean) ** 2, weights=tr_w))
    if rc_std == 0:
        return rc_mean, 0
    rc_skew = np.average(((rc - rc_mean) / rc_std) ** 3, weights=tr_w)

    return rc_mean, rc_skew


def init(context):
    context.index = '000300.XSHG'
    context.window = 60
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
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            turnovers = history_bars(stock, context.window, '1d', 'turnover_rate')
            if prices is None or len(prices) < context.window + 1:
                continue
            if turnovers is None or len(turnovers) < context.window:
                continue
            prices_arr = np.array(prices, dtype=float)
            if prices_arr[-1] == 0:
                continue
            # turnover_rate 在 RiceQuant 中是百分比（如1.5表示1.5%），归一化到小数
            tr_arr = np.array(turnovers, dtype=float)
            tr_arr = np.where(tr_arr > 1, tr_arr / 100.0, tr_arr)  # 兼容两种格式
            tr_arr = np.clip(tr_arr, 0, 1)
            rc_mean, rc_skew = calc_chip_distribution(
                prices_arr,
                tr_arr,
                context.window
            )
            if rc_mean is not None:
                # 选RC均值高（浮盈多）且偏度为正的股票
                scores[stock] = rc_mean + 0.5 * rc_skew
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
