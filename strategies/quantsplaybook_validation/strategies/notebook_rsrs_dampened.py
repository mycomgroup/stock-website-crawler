# 钝化 RSRS 择时策略 - RiceQuant 标准回测版本
# 候选2: 钝化 RSRS (V10)
# 构造: RSRS_dampened = z_score(beta) * R^2 * quantile(std(return), M)
# 参数: N=18, M=300, 阈值=0.7
# 标的: 沪深300 (000300.XSHG)
# 修复：移除 statsmodels 依赖，改用纯 numpy 实现 OLS 回归

import numpy as np


def ols_beta_r2(x, y):
    """纯 numpy 实现 OLS，返回 slope(beta) 和 R²"""
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    ss_xy = np.sum((x - x_mean) * (y - y_mean))
    ss_xx = np.sum((x - x_mean) ** 2)
    if ss_xx == 0:
        return None, None
    beta = ss_xy / ss_xx
    alpha = y_mean - beta * x_mean
    y_hat = alpha + beta * x
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2


def init(context):
    context.security = '000300.XSHG'
    context.N = 18          # 回归窗口
    context.M = 300         # 标准分窗口
    context.BUY_THRESHOLD = 0.7
    context.SELL_THRESHOLD = -0.7

    context.beta_history = []
    context.r2_history = []
    context.return_history = []
    context.prev_close = None
    context.in_market = False
    print(f"策略初始化完成，需要积累 {context.M} 天数据后开始交易")


def handle_bar(context, bar_dict):
    bar = bar_dict[context.security]
    close = bar.close

    if context.prev_close is not None and context.prev_close > 0:
        ret = (close - context.prev_close) / context.prev_close
        context.return_history.append(ret)
    context.prev_close = close

    highs = history_bars(context.security, context.N + 1, '1d', 'high')
    lows = history_bars(context.security, context.N + 1, '1d', 'low')

    if highs is None or lows is None or len(highs) < context.N:
        return

    h = np.array(highs[-context.N:], dtype=float)
    l = np.array(lows[-context.N:], dtype=float)

    beta, r2 = ols_beta_r2(l, h)
    if beta is None:
        return

    context.beta_history.append(beta)
    context.r2_history.append(r2)

    if len(context.beta_history) < context.M:
        return

    beta_window = np.array(context.beta_history[-context.M:])
    sigma = np.std(beta_window)
    if sigma == 0:
        return
    z = (beta - np.mean(beta_window)) / sigma

    if len(context.return_history) < context.N:
        return

    ret_arr = np.array(context.return_history)
    ret_std_window = []
    start = max(0, len(ret_arr) - context.M)
    for i in range(start, len(ret_arr) - context.N + 1):
        ret_std_window.append(np.std(ret_arr[i:i + context.N]))

    if not ret_std_window:
        return

    current_std = np.std(ret_arr[-context.N:])
    quantile = np.sum(np.array(ret_std_window) <= current_std) / len(ret_std_window)

    rsrs_dampened = z * r2 * quantile

    if rsrs_dampened > context.BUY_THRESHOLD and not context.in_market:
        order_target_value(context.security, context.portfolio.total_value * 0.95)
        context.in_market = True
    elif rsrs_dampened < context.SELL_THRESHOLD and context.in_market:
        order_target_value(context.security, 0)
        context.in_market = False
