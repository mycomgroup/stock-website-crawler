# ETF动量轮动RSRS择时-魔改3优化版 - RiceQuant版本
# 原文：ETF动量轮动RSRS择时-魔改3小优化
# 作者：莫急莫急
# 原文：https://www.joinquant.com/post/35279
# 逻辑：4只宽基ETF按动量评分选最优，叠加RSRS+MA双重择时

import numpy as np
import math


ETF_POOL = [
    '510050.XSHG',  # 上证50ETF
    '159928.XSHE',  # 中证消费ETF
    '510300.XSHG',  # 沪深300ETF
    '159949.XSHE',  # 创业板50ETF
]
REF = '000300.XSHG'


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


def get_rank(etf_pool, m_days=20):
    scores = {}
    for etf in etf_pool:
        try:
            closes = history_bars(etf, m_days, '1d', 'close')
            if closes is None or len(closes) < m_days:
                continue
            p = np.array(closes, dtype=float)
            x = np.arange(len(p))
            slope, _ = np.polyfit(x, p / p[0], 1)
            scores[etf] = slope
        except Exception:
            continue
    return sorted(scores, key=scores.get, reverse=True)


def get_timing_signal(context, N=18, M=600, threshold=0.7, mean_day=30, mean_diff=5):
    try:
        highs = history_bars(REF, N + M, '1d', 'high')
        lows = history_bars(REF, N + M, '1d', 'low')
        closes = history_bars(REF, mean_day + mean_diff, '1d', 'close')
        if any(x is None for x in [highs, lows, closes]):
            return 'KEEP'

        h = np.array(highs, dtype=float)
        l = np.array(lows, dtype=float)
        c = np.array(closes, dtype=float)

        betas = []
        for i in range(M):
            b, _ = ols_beta_r2(l[i:i+N], h[i:i+N])
            if b is not None:
                betas.append(b)

        if len(betas) < 10:
            return 'KEEP'

        betas = np.array(betas)
        _, r2 = ols_beta_r2(l[-N:], h[-N:])
        z = (betas[-1] - np.mean(betas)) / (np.std(betas) + 1e-10)
        rsrs = z * (r2 or 0)

        today_ma = np.mean(c[mean_diff:])
        before_ma = np.mean(c[:mean_diff])

        if rsrs > threshold and today_ma > before_ma:
            return 'BUY'
        elif rsrs < -threshold and today_ma < before_ma:
            return 'SELL'
        return 'KEEP'
    except Exception:
        return 'KEEP'


def init(context):
    context.etf_pool = ETF_POOL
    context.pos = False
    scheduler.run_daily(my_trade, time_rule=market_open(minute=0))



def handle_bar(context, bar_dict):
    pass

def my_trade(context, bar_dict):
    ranked = get_rank(context.etf_pool)
    if not ranked:
        return

    signal = get_timing_signal(context)
    target = ranked[0]

    if signal == 'SELL':
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        return

    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    order_target_value(target, context.portfolio.total_value * 0.95)
