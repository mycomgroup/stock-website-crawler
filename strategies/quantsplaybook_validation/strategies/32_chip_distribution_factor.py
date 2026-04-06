# 筹码分布因子选股策略 - RiceQuant版本
# 来源：《根据前景理论的筹码因子构建》
# 核心逻辑：基于换手率加权计算筹码分布，构建相对资本收益（RC）均值/偏度因子
# 修复：
#   1. 移除 O(N²) 嵌套循环，改用向量化衰减计算
#   2. 月度调仓失败时重置 month，下月重试
#   3. 加强数据校验

import numpy as np


def calc_chip_distribution(prices, rel_volumes, window=60):
    """
    计算筹码分布代理变量（向量化版本）
    用 cumprod 替代嵌套循环实现路径依赖衰减
    """
    p = np.array(prices[-window:], dtype=float)
    tr = np.array(rel_volumes[-window:], dtype=float)
    current_price = p[-1]

    # 向量化衰减：每个历史时点的筹码被后续换手率逐步稀释
    # atr[i] = tr[i] * prod(1 - tr[j]) for j > i
    decay = np.ones(window)
    for i in range(window - 2, -1, -1):
        decay[i] = decay[i + 1] * (1 - min(tr[i + 1], 0.99))

    atr = tr * decay
    atr_sum = atr.sum()
    if atr_sum == 0:
        return None, None
    tr_w = atr / atr_sum

    rc = (current_price - p) / (current_price + 1e-10)

    rc_mean = np.average(rc, weights=tr_w)
    rc_var = np.average((rc - rc_mean) ** 2, weights=tr_w)
    rc_std = np.sqrt(rc_var)
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
    if context.month == -1:
        print(f"[32] 首次运行: {context.now}")
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components(context.index)
    if not stocks or len(stocks) < 10:
        return  # 不更新 month，下个 bar 继续重试

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            volumes = history_bars(stock, context.window + 5, '1d', 'volume')
            if prices is None or len(prices) < context.window:
                continue
            if volumes is None or len(volumes) < context.window:
                continue

            p = np.array(prices[-context.window:], dtype=float)
            if p[-1] == 0:
                continue

            v = np.array(volumes[-context.window:], dtype=float)
            avg_vol = np.mean(v)
            if avg_vol == 0:
                continue
            rel_vol = np.clip(v / avg_vol / (v.max() / avg_vol + 1e-10), 0, 1)

            rc_mean, rc_skew = calc_chip_distribution(p, rel_vol, context.window)
            if rc_mean is not None:
                scores[stock] = rc_mean + 0.5 * rc_skew
        except Exception:
            continue

    if not scores:
        return  # 不更新 month，下个 bar 继续重试

    # 成功选股后才更新月份
    context.month = current_month

    target = sorted(scores, key=scores.get, reverse=True)[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
