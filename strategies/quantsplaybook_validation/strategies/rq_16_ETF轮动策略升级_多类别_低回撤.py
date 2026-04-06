# ETF多类别轮动升级版 - RiceQuant版本
# 逻辑：宽基+行业+债券ETF池，动量轮动，低波动率优先，低回撤

import numpy as np

def _ols_beta_r2(x, y):
    """Pure numpy OLS: returns (beta, r2)"""
    xm, ym = x.mean(), y.mean()
    ss_xx = ((x - xm) ** 2).sum()
    if ss_xx == 0:
        return None, None
    beta = ((x - xm) * (y - ym)).sum() / ss_xx
    y_hat = ym + beta * (x - xm)
    ss_res = ((y - y_hat) ** 2).sum()
    ss_tot = ((y - ym) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2



def _bootstrap_rsrs_history(ref, n, m):
    highs = history_bars(ref, n + m, '1d', 'high')
    lows = history_bars(ref, n + m, '1d', 'low')
    if highs is None or lows is None or len(highs) < n + m or len(lows) < n + m:
        return [], []
    beta_history = []
    r2_history = []
    for i in range(m):
        h = np.array(highs[i:i + n], dtype=float)
        l = np.array(lows[i:i + n], dtype=float)
        beta, r2 = _ols_beta_r2(l, h)
        if beta is None:
            continue
        beta_history.append(beta)
        r2_history.append(r2)
    return beta_history, r2_history


def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300
        '159915.XSHE',  # 创业板
        '510500.XSHG',  # 中证500
        '510050.XSHG',  # 上证50
        '518880.XSHG',  # 黄金
        '511010.XSHG',  # 国债
        '513100.XSHG',  # 纳指100
        '159928.XSHE',  # 消费
    ]
    context.N = 18
    context.M = 300
    context.ref = '000300.XSHG'
    context.beta_history = []
    context.r2_history = []
    context.in_market = False
    context.month = -1


def handle_bar(context, bar_dict):
    if not context.beta_history:
        context.beta_history, context.r2_history = _bootstrap_rsrs_history(context.ref, context.N, context.M)
    # RSRS择时
    highs = history_bars(context.ref, context.N + 1, '1d', 'high')
    lows = history_bars(context.ref, context.N + 1, '1d', 'low')
    if highs is None or lows is None or len(highs) < context.N:
        return

    h = np.array(highs[-context.N:], dtype=float)
    l = np.array(lows[-context.N:], dtype=float)
    beta, r2 = _ols_beta_r2(l, h)
    if beta is None:
        return
    context.beta_history.append(beta)
    context.r2_history.append(r2)

    if len(context.beta_history) > context.M:
        context.beta_history = context.beta_history[-context.M:]
        context.r2_history = context.r2_history[-context.M:]

    if len(context.beta_history) < context.M:
        return

    beta_arr = np.array(context.beta_history)
    mu, sigma = np.mean(beta_arr), np.std(beta_arr)
    if sigma == 0:
        return
    rsrs = (beta_arr[-1] - mu) / sigma * beta_arr[-1] * context.r2_history[-1]

    current_month = context.now.month
    if current_month == context.month:
        if rsrs < -0.7 and context.in_market:
            for etf in list(context.portfolio.positions.keys()):
                order_target_value(etf, 0)
            context.in_market = False
        return
    context.month = current_month

    if rsrs < -0.7:
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        context.in_market = False
        return

    # 动量+低波动率选ETF
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 60, '1d', 'close')
            if closes is None or len(closes) < 60:
                continue
            closes = np.array(closes, dtype=float)
            momentum = closes[-1] / closes[0] - 1
            returns = np.diff(closes) / closes[:-1]
            vol = np.std(returns)
            scores[etf] = momentum - vol * 2
        except Exception:
            continue

    if not scores:
        return

    best = max(scores, key=scores.get)
    if scores[best] < 0:
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        context.in_market = False
        return

    for etf in list(context.portfolio.positions.keys()):
        if etf != best:
            order_target_value(etf, 0)

    bar = (bar_dict[best] if best in bar_dict else None)
    if bar is not None and bar.is_trading:
        order_target_value(best, context.portfolio.total_value * 0.95)
        context.in_market = True
