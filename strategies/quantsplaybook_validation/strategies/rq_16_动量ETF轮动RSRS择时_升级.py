# 动量ETF轮动RSRS择时升级版 - RiceQuant版本
# 逻辑：ETF动量轮动 + RSRS择时，升级参数（N=18, M=300, 阈值0.7）

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
        '510300.XSHG', '159915.XSHE', '510500.XSHG',
        '518880.XSHG', '511010.XSHG', '513100.XSHG',
    ]
    context.momentum_days = 20
    context.N = 18
    context.M = 300
    context.threshold = 0.7
    context.ref = '000300.XSHG'
    context.beta_history = []
    context.r2_history = []
    context.in_market = False
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    if not context.beta_history:
        context.beta_history, context.r2_history = _bootstrap_rsrs_history(context.ref, context.N, context.M)
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

    if rsrs < -context.threshold:
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        context.in_market = False
        return

    if rsrs > context.threshold:
        scores = {}
        for etf in context.etf_pool:
            try:
                closes = history_bars(etf, context.momentum_days + 1, '1d', 'close')
                if closes is None or len(closes) < context.momentum_days + 1:
                    continue
                closes = np.array(closes, dtype=float)
                y = np.log(closes)
                x = np.arange(len(y))
                slope, intercept = np.polyfit(x, y, 1)
                r2 = 1 - np.sum((y - (slope * x + intercept))**2) / (np.var(y) * len(y) + 1e-10)
                scores[etf] = (np.exp(slope * 250) - 1) * max(r2, 0)
            except Exception:
                continue

        if not scores:
            return

        best = max(scores, key=scores.get)

        for etf in list(context.portfolio.positions.keys()):
            if etf != best:
                order_target_value(etf, 0)

        bar = (bar_dict[best] if best in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(best, context.portfolio.total_value * 0.95)
            context.in_market = True
