# 筹码分布因子选股策略 - RiceQuant版本
# 来源：《根据前景理论的筹码因子构建》
# 核心逻辑：基于换手率加权计算筹码分布，构建相对资本收益（RC）均值/偏度因子
#           RC均值低（大量筹码被套）时，处置效应导致抛压大，做空；RC均值高时做多
# 修复：用 volume 代替 turnover_rate（RiceQuant history_bars 不支持 turnover_rate 字段）
#       换手率代理 = 当日成交量 / 过去N日平均成交量（相对成交量）

import numpy as np


def calc_chip_distribution(prices, rel_volumes, window=60):
    """
    计算筹码分布的代理变量
    - prices: 收盘价序列 (window个)
    - rel_volumes: 相对成交量序列 (window个，已归一化)
    - 返回：RC均值、RC偏度
    """
    if len(prices) < window or len(rel_volumes) < window:
        return None, None

    p = np.array(prices[-window:], dtype=float)
    tr = np.array(rel_volumes[-window:], dtype=float)
    current_price = p[-1]

    # 计算调整换手率（路径依赖衰减）
    atr = np.zeros(window)
    atr[0] = tr[0]
    for i in range(1, window):
        atr[i] = tr[i]
        for j in range(i):
            atr[j] *= (1 - min(tr[i], 0.99))  # 防止乘以1导致全0

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
            volumes = history_bars(stock, context.window + 10, '1d', 'volume')
            if prices is None or len(prices) < context.window + 1:
                continue
            if volumes is None or len(volumes) < context.window:
                continue

            prices_arr = np.array(prices, dtype=float)
            if prices_arr[-1] == 0:
                continue

            vol_arr = np.array(volumes, dtype=float)
            # 用相对成交量作为换手率代理（归一化到0-1范围）
            avg_vol = np.mean(vol_arr)
            if avg_vol == 0:
                continue
            rel_vol = vol_arr[-context.window:] / avg_vol
            # 归一化到合理范围（0~1），避免极端值
            rel_vol = np.clip(rel_vol / (rel_vol.max() + 1e-10), 0, 1)

            rc_mean, rc_skew = calc_chip_distribution(
                prices_arr[-context.window:],
                rel_vol,
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
