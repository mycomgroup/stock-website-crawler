# ETF核心资产动量+RSRS择时轮动策略 - RiceQuant版本
# 原文：ETF核心资产轮动动量因子加RSRS择时每日策略
# 原文：https://www.joinquant.com/post/
# 逻辑：核心资产ETF按动量评分轮动，叠加RSRS择时信号

import numpy as np


CORE_ETFS = [
    '510300.XSHG',  # 沪深300ETF
    '510500.XSHG',  # 中证500ETF
    '159915.XSHE',  # 创业板ETF
    '513100.XSHG',  # 纳指100
    '518880.XSHG',  # 黄金ETF
    '511010.XSHG',  # 国债ETF
]


def calc_rsrs(security, n=18, m=600):
    """计算RSRS标准分"""
    try:
        highs = history_bars(security, n + m, '1d', 'high')
        lows = history_bars(security, n + m, '1d', 'low')
        if highs is None or lows is None or len(highs) < n + m:
            return 0
        betas = []
        for i in range(m):
            h = np.array(highs[i:i+n], dtype=float)
            l = np.array(lows[i:i+n], dtype=float)
            if np.std(l) == 0:
                continue
            beta = np.cov(h, l)[0, 1] / np.var(l)
            betas.append(beta)
        if len(betas) < 10:
            return 0
        betas = np.array(betas)
        return (betas[-1] - np.mean(betas)) / np.std(betas)
    except Exception:
        return 0


def get_momentum_score(etf, period=20):
    try:
        prices = history_bars(etf, period + 1, '1d', 'close')
        if prices is None or len(prices) < period + 1:
            return None
        p = np.array(prices, dtype=float)
        y = np.log(p)
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        annualized = np.exp(slope * 250) - 1
        y_hat = slope * x + intercept
        ss_res = np.sum((y - y_hat) ** 2)
        ss_tot = (len(y) - 1) * np.var(y, ddof=1)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return annualized * r2
    except Exception:
        return None


def init(context):
    context.etfs = CORE_ETFS
    context.rsrs_threshold = 0.7
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    # RSRS择时：用沪深300判断市场状态
    rsrs = calc_rsrs('000300.XSHG')

    scores = {}
    for etf in context.etfs:
        score = get_momentum_score(etf)
        if score is not None:
            scores[etf] = score

    if not scores:
        return

    context.month = current_month

    # RSRS信号弱时持有国债ETF
    if rsrs < -context.rsrs_threshold:
        for etf in list(context.portfolio.positions.keys()):
            if etf != '511010.XSHG':
                order_target_value(etf, 0)
        order_target_value('511010.XSHG', context.portfolio.total_value * 0.95)
        return

    target = sorted(scores, key=scores.get, reverse=True)[0]

    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    order_target_value(target, context.portfolio.total_value * 0.95)
