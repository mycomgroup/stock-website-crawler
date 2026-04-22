# 原文链接：https://www.joinquant.com/post/35416
# 策略：动量ETF轮动-RSRS择时-卡尔曼滤波
# 作者：莫急莫急
# 核心逻辑：ETF动量轮动 + RSRS择时 + 卡尔曼滤波平滑动量
# 注：原版用 pykalman，RQ 不支持，此处用简单卡尔曼滤波替代

import numpy as np

ETF_POOL = ['510050.XSHG', '159928.XSHE', '510300.XSHG', '159949.XSHE']
REF_STOCK = '000300.XSHG'
N, M = 18, 600
THRESHOLD = 0.7
MOMENTUM_DAY = 20


def ols_beta_r2(x, y):
    xm, ym = np.mean(x), np.mean(y)
    ss_xx = np.sum((x - xm) ** 2)
    if ss_xx == 0:
        return None, None
    beta = np.sum((x - xm) * (y - ym)) / ss_xx
    yhat = ym + beta * (x - xm)
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - ym) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2


def kalman_smooth(obs, q=0.15, r=1.0):
    """简单卡尔曼滤波平滑序列"""
    x, p, res = float(obs[0]), r, []
    for o in obs:
        p += q
        k = p / (p + r)
        x += k * (float(o) - x)
        p = (1 - k) * p
        res.append(x)
    return np.array(res)


def init(context):
    context.etf_pool = ETF_POOL
    context.beta_history = []
    context.r2_history = []
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def get_rsrs(context):
    highs = history_bars(REF_STOCK, N + 1, '1d', 'high')
    lows  = history_bars(REF_STOCK, N + 1, '1d', 'low')
    if highs is None or lows is None or len(highs) < N:
        return None
    beta, r2 = ols_beta_r2(
        np.array(lows[-N:], dtype=float),
        np.array(highs[-N:], dtype=float)
    )
    if beta is None:
        return None
    context.beta_history.append(beta)
    context.r2_history.append(r2)
    if len(context.beta_history) > M:
        context.beta_history = context.beta_history[-M:]
        context.r2_history   = context.r2_history[-M:]
    if len(context.beta_history) < M:
        return None
    arr = np.array(context.beta_history)
    sigma = np.std(arr)
    if sigma == 0:
        return None
    z = (beta - np.mean(arr)) / sigma
    return z * beta * r2


def get_momentum(etf):
    prices = history_bars(etf, MOMENTUM_DAY + 5, '1d', 'close')
    if prices is None or len(prices) < MOMENTUM_DAY:
        return None
    p = np.array(prices[-MOMENTUM_DAY:], dtype=float)
    smoothed = kalman_smooth(p / p[0])
    slope = np.polyfit(np.arange(MOMENTUM_DAY), smoothed, 1)[0]
    return slope


def trade(context, bar_dict):
    rsrs = get_rsrs(context)
    if rsrs is None:
        return

    if rsrs < -THRESHOLD:
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        print(f"[卡尔曼RSRS] 空仓 rsrs={rsrs:.3f}")
        return

    if rsrs > THRESHOLD:
        scores = {etf: get_momentum(etf) for etf in context.etf_pool}
        scores = {k: v for k, v in scores.items() if v is not None}
        if not scores:
            return
        best = max(scores, key=scores.get)
        for s in list(context.portfolio.positions.keys()):
            if s != best:
                order_target_value(s, 0)
        order_target_value(best, context.portfolio.total_value * 0.95)
        print(f"[卡尔曼RSRS] 买入 {best} rsrs={rsrs:.3f} mom={scores[best]:.4f}")
