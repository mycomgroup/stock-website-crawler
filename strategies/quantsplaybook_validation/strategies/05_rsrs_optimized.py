# RSRS择时策略（优化版）- RiceQuant版本
# 来源：《光大证券-基于阻力支撑相对强度（RSRS）的市场择时》
# 已验证策略，作为基准对比

import numpy as np


def ols_beta_r2(x, y):
    """纯 numpy OLS，返回 slope(beta) 和 R²"""
    x_mean, y_mean = np.mean(x), np.mean(y)
    ss_xx = np.sum((x - x_mean) ** 2)
    if ss_xx == 0:
        return None, None
    beta = np.sum((x - x_mean) * (y - y_mean)) / ss_xx
    alpha = y_mean - beta * x_mean
    y_hat = alpha + beta * x
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2

def init(context):
    context.security = '000300.XSHG'
    context.N = 18
    context.M = 300
    context.buy_threshold = 0.8
    context.sell_threshold = -0.8
    context.beta_history = []
    context.r2_history = []
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    N = context.N
    M = context.M

    # 分开获取高低价（RiceQuant history_bars 不支持多字段列表，需单独调用）
    lookback = N + 1
    all_highs = history_bars(security, lookback, '1d', 'high')
    all_lows = history_bars(security, lookback, '1d', 'low')
    if all_highs is None or all_lows is None or len(all_highs) < N:
        return

    highs = np.array(all_highs[-N:], dtype=float)
    lows = np.array(all_lows[-N:], dtype=float)

    beta, r2 = ols_beta_r2(lows, highs)
    if beta is None:
        return
    context.beta_history.append(beta)
    context.r2_history.append(r2)

    # 保持长度
    if len(context.beta_history) > M:
        context.beta_history = context.beta_history[-M:]
        context.r2_history = context.r2_history[-M:]

    if len(context.beta_history) < M:
        return

    # 计算标准分
    beta_arr = np.array(context.beta_history)
    mu, sigma = np.mean(beta_arr), np.std(beta_arr)
    if sigma == 0:
        return

    zscore = (beta_arr[-1] - mu) / sigma
    beta = beta_arr[-1]
    r2 = context.r2_history[-1] if context.r2_history else 0.5

    # 右偏标准分
    rsrs = zscore * beta * r2

    # 交易逻辑
    if rsrs > context.buy_threshold and not context.pos:
        order_target_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: RSRS={rsrs:.3f}")
    elif rsrs < context.sell_threshold and context.pos:
        order_target_value(security, 0)
        context.pos = False
        print(f"卖出: RSRS={rsrs:.3f}")