# RSRS趋势交易与网格交易结合策略 - RiceQuant版本
# 原文：基于RSRS的趋势交易与网格交易相结合的尝试
# 原文：https://www.joinquant.com/post/24680
# 逻辑：RSRS信号判断趋势，趋势向上时网格加仓，趋势向下时减仓

import numpy as np


def ols_beta_r2(x, y):
    xm, ym = np.mean(x), np.mean(y)
    ss_xx = np.sum((x - xm) ** 2)
    if ss_xx == 0:
        return None, None
    beta = np.sum((x - xm) * (y - ym)) / ss_xx
    alpha = ym - beta * xm
    y_hat = alpha + beta * x
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - ym) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2


def get_rsrs_signal(security, N=18, M=600, buy_th=0.7, sell_th=-0.7):
    try:
        highs = history_bars(security, N + M, '1d', 'high')
        lows = history_bars(security, N + M, '1d', 'low')
        if highs is None or lows is None or len(highs) < N + M:
            return 'KEEP'
        h = np.array(highs, dtype=float)
        l = np.array(lows, dtype=float)
        betas = []
        for i in range(M):
            b, r2 = ols_beta_r2(l[i:i+N], h[i:i+N])
            if b is not None:
                betas.append(b * (r2 or 0))
        if len(betas) < 10:
            return 'KEEP'
        betas = np.array(betas)
        z = (betas[-1] - np.mean(betas)) / (np.std(betas) + 1e-10)
        if z > buy_th:
            return 'BUY'
        elif z < sell_th:
            return 'SELL'
        return 'KEEP'
    except Exception:
        return 'KEEP'


def init(context):
    context.security = '510300.XSHG'
    context.gear = 2
    context.position_per_gear = 1.0 / (context.gear + 1)
    context.current_gear = 0
    context.base_price = None


def handle_bar(context, bar_dict):
    bar = (bar_dict[context.security] if context.security in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    signal = get_rsrs_signal('000300.XSHG')
    current_price = bar.close

    if context.base_price is None:
        context.base_price = current_price

    price_change = (current_price - context.base_price) / context.base_price

    if signal == 'SELL':
        order_target_value(context.security, 0)
        context.current_gear = 0
        return

    if signal == 'BUY' and context.current_gear == 0:
        target_ratio = context.position_per_gear
        order_target_value(context.security, context.portfolio.total_value * target_ratio)
        context.current_gear = 1
        context.base_price = current_price
        return

    # 网格逻辑：每跌5%加一格，每涨5%减一格
    gear_change = int(price_change / -0.05)
    target_gear = max(0, min(context.gear, context.current_gear + gear_change))

    if target_gear != context.current_gear:
        target_ratio = target_gear * context.position_per_gear
        order_target_value(context.security, context.portfolio.total_value * target_ratio)
        context.current_gear = target_gear
