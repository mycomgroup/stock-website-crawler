# 原文链接：https://www.joinquant.com/post/37516
# 策略：ETF动量轮动RSRS择时-V2.1（乖离动量 + RSRS + 盘中止损）
# 作者：Deemoo
# 核心逻辑：用乖离率斜率作为动量，RSRS择时，日频简化止损

import numpy as np

ETF_POOL = ['510050.XSHG', '510300.XSHG', '159949.XSHE', '159928.XSHE']
REF_STOCK = '000300.XSHG'
N, M = 18, 600
THRESHOLD = 0.7
MOMENTUM_DAY = 20
BIAS_N = 90


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


def init(context):
    context.etf_pool = ETF_POOL
    context.beta_history = []
    context.r2_history = []
    scheduler.run_daily(trade, time_rule=market_open(minute=30))
    scheduler.run_daily(check_stop, time_rule=market_close(minute=30))


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


def get_bias_momentum(etf):
    need = BIAS_N + MOMENTUM_DAY + 5
    prices = history_bars(etf, need, '1d', 'close')
    if prices is None or len(prices) < BIAS_N + MOMENTUM_DAY:
        return None
    p = np.array(prices, dtype=float)
    # 计算乖离率序列
    ma90 = np.array([np.mean(p[i:i + BIAS_N]) for i in range(len(p) - BIAS_N + 1)])
    bias = p[BIAS_N - 1:] / ma90
    bias_recent = bias[-MOMENTUM_DAY:]
    if bias_recent[0] == 0:
        return None
    slope = np.polyfit(np.arange(MOMENTUM_DAY), bias_recent / bias_recent[0], 1)[0]
    return slope


def trade(context, bar_dict):
    rsrs = get_rsrs(context)
    if rsrs is None:
        return

    if rsrs < -THRESHOLD:
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        print(f"[RSRS V2.1] 空仓 rsrs={rsrs:.3f}")
        return

    if rsrs > THRESHOLD:
        scores = {etf: get_bias_momentum(etf) for etf in context.etf_pool}
        scores = {k: v for k, v in scores.items() if v is not None}
        if not scores:
            return
        best = max(scores, key=scores.get)
        for s in list(context.portfolio.positions.keys()):
            if s != best:
                order_target_value(s, 0)
        order_target_value(best, context.portfolio.total_value * 0.95)
        print(f"[RSRS V2.1] 买入 {best} rsrs={rsrs:.3f}")


def check_stop(context, bar_dict):
    """日频简化止损：当日跌幅超过3%则卖出"""
    for s in list(context.portfolio.positions.keys()):
        prices = history_bars(s, 2, '1d', 'close')
        if prices is None or len(prices) < 2:
            continue
        if prices[-1] / prices[-2] - 1 < -0.03:
            order_target_value(s, 0)
            print(f"[RSRS V2.1] 止损 {s}")
