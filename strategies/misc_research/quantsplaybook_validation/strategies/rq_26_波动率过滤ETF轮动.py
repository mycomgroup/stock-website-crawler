# 波动率过滤后相关性最小ETF轮动 - RiceQuant版本
# 原文：波动率过滤后相关性最小etf轮动
# 作者：开心果
# 原文：https://www.joinquant.com/post/49615
# 逻辑：从ETF池中筛选波动率适中的，选相关性最小的4只，按动量评分选最优

import numpy as np
import pandas as pd
import math


ETF_POOL = [
    '512660.XSHG', '511010.XSHG', '510880.XSHG', '159915.XSHE', '513050.XSHG',
    '510050.XSHG', '588100.XSHG', '512100.XSHG', '518800.XSHG', '513060.XSHG',
    '512980.XSHG', '512010.XSHG', '513100.XSHG', '512720.XSHG', '512070.XSHG',
    '515880.XSHG', '159920.XSHE', '159922.XSHE', '513520.XSHG', '515000.XSHE',
    '515790.XSHG', '515700.XSHG', '159825.XSHE', '512400.XSHG', '512200.XSHG',
    '513360.XSHG', '512480.XSHG', '510230.XSHG', '159647.XSHE', '159928.XSHE',
]


def min_corr_etfs(etf_pool, nday=120):
    """选相关性最小的4只ETF（波动率过滤后）"""
    price_data = {}
    for etf in etf_pool:
        try:
            prices = history_bars(etf, nday, '1d', 'close')
            if prices is not None and len(prices) >= nday:
                price_data[etf] = np.array(prices, dtype=float)
        except Exception:
            continue

    if len(price_data) < 4:
        return list(price_data.keys())[:4]

    # 计算对数收益率
    returns = {}
    for etf, p in price_data.items():
        r = np.diff(np.log(p))
        returns[etf] = r

    # 波动率过滤
    valid_etfs = []
    for etf, r in returns.items():
        vol = np.std(r) * math.sqrt(243)
        if 0.05 < vol < 0.33:
            valid_etfs.append(etf)

    if len(valid_etfs) < 4:
        valid_etfs = list(returns.keys())

    # 计算相关性矩阵，选平均相关性最小的4只
    ret_matrix = np.array([returns[e] for e in valid_etfs])
    corr = np.corrcoef(ret_matrix)
    corr_mean = {valid_etfs[i]: np.mean(np.abs(corr[i])) for i in range(len(valid_etfs))}
    return sorted(corr_mean, key=corr_mean.get)[:4]


def get_best_etf(etf_pool, m_days=25):
    """按动量评分选最优ETF"""
    scores = {}
    for etf in etf_pool:
        try:
            prices = history_bars(etf, m_days, '1d', 'close')
            if prices is None or len(prices) < m_days:
                continue
            y = np.log(np.array(prices, dtype=float))
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            annualized = math.exp(slope * 250) - 1
            y_hat = slope * x + intercept
            ss_res = np.sum((y - y_hat) ** 2)
            ss_tot = (len(y) - 1) * np.var(y, ddof=1)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            score = annualized * r2
            if -0.5 < score < 4.5:
                scores[etf] = score
        except Exception:
            continue
    return sorted(scores, key=scores.get, reverse=True)


def init(context):
    context.etf_pool = ETF_POOL
    context.m_days = 25
    scheduler.run_daily(trade, time_rule=market_open(minute=0))



def handle_bar(context, bar_dict):
    pass

def trade(context, bar_dict):
    candidate_etfs = min_corr_etfs(context.etf_pool)
    ranked = get_best_etf(candidate_etfs, context.m_days)

    if not ranked:
        return

    target = ranked[0]

    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    order_target_value(target, context.portfolio.total_value * 0.95)
