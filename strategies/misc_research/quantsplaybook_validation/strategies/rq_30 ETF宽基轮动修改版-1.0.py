# Auto-generated alias for placeholder rq_30 ETF宽基轮动修改版-1.0.txt
# Reuses migrated RiceQuant implementation from rq_30_ETF宽基轮动.py
# Shared original URL: https://www.joinquant.com/post/29165

# ETF宽基轮动策略 - RiceQuant版本
# 原文：ETF宽基轮动修改版-1.0
# 作者：几米哥
# 原文：https://www.joinquant.com/post/29165
# 逻辑：7只宽基ETF按动量+均线双重过滤，选前4只轮动

import numpy as np
import pandas as pd


# ETF池：[指数代码, ETF代码]
ETF_MAP = {
    '513100.XSHG': '513100.XSHG',  # 纳指100
    '513500.XSHG': '513500.XSHG',  # 标普500
    '518880.XSHG': '518880.XSHG',  # 黄金ETF
    '159915.XSHE': '159915.XSHE',  # 创业板ETF
    '510300.XSHG': '510300.XSHG',  # 沪深300ETF
    '510500.XSHG': '510500.XSHG',  # 中证500ETF
    '159920.XSHE': '159920.XSHE',  # 恒生ETF
}
CASH_ETF = '511010.XSHG'  # 国债ETF（避险）


def get_signal(etf_list, lag1=20, lag2=10, ma_threshold=0.9, mtm_threshold=2):
    scores = {}
    for etf in etf_list:
        try:
            prices = history_bars(etf, lag1 + 1, '1d', 'close')
            if prices is None or len(prices) < lag1 + 1:
                continue
            p = np.array(prices, dtype=float)
            current_price = p[-1]
            # 动量：相对lag1天前的涨幅
            cp_increase = 100 * (current_price / p[0] - 1)
            # 均线差：当前价格 - MA(lag2) * threshold
            ma_n = np.mean(p[-lag2:])
            ma_diff = current_price - ma_n * ma_threshold
            # 双重过滤：动量>阈值 且 价格在均线上方
            if cp_increase > mtm_threshold and ma_diff > 0:
                scores[etf] = cp_increase
        except Exception:
            continue
    return scores


def init(context):
    context.etf_list = list(ETF_MAP.keys())
    context.top_n = 4
    scheduler.run_daily(trade, time_rule=market_open(minute=60))



def handle_bar(context, bar_dict):
    pass

def trade(context, bar_dict):
    scores = get_signal(context.etf_list)

    if not scores:
        # 无信号时持有国债ETF
        for etf in list(context.portfolio.positions.keys()):
            if etf != CASH_ETF:
                order_target_value(etf, 0)
        order_target_value(CASH_ETF, context.portfolio.total_value * 0.95)
        return

    target = sorted(scores, key=scores.get, reverse=True)[:context.top_n]

    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_target_value(etf, 0)

    # 按动量权重分配
    total_score = sum(scores[e] for e in target)
    for etf in target:
        if not target:
            return
        weight = scores[etf] / total_score if total_score > 0 else 1.0 / len(target)
        order_target_value(etf, context.portfolio.total_value * weight * 0.95)
