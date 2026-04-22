# 高评分ETF策略之核心资产轮动 - RiceQuant版本
# 原文：【回顾3】ETF策略之核心资产轮动
# 作者：wywy1995
# 原文：https://www.joinquant.com/post/42673
# 逻辑：4只核心ETF按年化收益*R²动量评分，每日选最优1只持仓

import numpy as np
import pandas as pd
import math


ETF_POOL = [
    '518880.XSHG',  # 黄金ETF
    '513100.XSHG',  # 纳指100
    '159915.XSHE',  # 创业板100
    '510330.XSHG',  # 沪深300ETF华夏（原上证180ETF已退市）
]


def get_rank(etf_pool, m_days=25):
    scores = {}
    for etf in etf_pool:
        try:
            closes = history_bars(etf, m_days, '1d', 'close')
            if closes is None or len(closes) < m_days:
                continue
            y = np.log(np.array(closes, dtype=float))
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            annualized = math.pow(math.exp(slope), 250) - 1
            y_hat = slope * x + intercept
            ss_res = np.sum((y - y_hat) ** 2)
            ss_tot = (len(y) - 1) * np.var(y, ddof=1)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            scores[etf] = annualized * r2
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
    ranked = get_rank(context.etf_pool, context.m_days)
    if not ranked:
        return

    target = ranked[0]

    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    order_target_value(target, context.portfolio.total_value * 0.95)
