# 原文链接：https://www.joinquant.com/post/44850
# 策略："开弓"ETF轮动模型——改
# 作者：开弓量化
# 核心逻辑：宽基ETF轮动，用动量+波动率评分选ETF，月度调仓

import numpy as np


# 宽基ETF池
ETF_POOL = [
    '510300.XSHG',  # 沪深300ETF
    '510500.XSHG',  # 中证500ETF
    '159915.XSHE',  # 创业板ETF
    '588000.XSHG',  # 科创50ETF
    '510050.XSHG',  # 上证50ETF
    '159949.XSHE',  # 创业板50ETF
    '511010.XSHG',  # 国债ETF（避险）
]


def calc_score(prices, lookback=20):
    """动量/波动率综合评分：动量高、波动低得分高"""
    if len(prices) < lookback + 1:
        return None
    p = np.array(prices, dtype=float)
    ret = p[-1] / p[-lookback - 1] - 1
    vol = np.std(np.diff(np.log(p[-lookback:])))
    if vol < 1e-9:
        return None
    return ret / vol  # 夏普比率近似


def init(context):
    context.etf_pool = ETF_POOL
    context.n_hold = 3
    context.lookback = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：动量+波动率评分选ETF"""
    scores = {}
    for etf in context.etf_pool:
        prices = history_bars(etf, context.lookback + 5, '1d', 'close')
        if prices is None:
            continue
        s = calc_score(prices, context.lookback)
        if s is not None:
            scores[etf] = s

    if not scores:
        logger.info("[开弓ETF] 无有效数据")
        return

    sorted_etfs = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    target = sorted_etfs[:context.n_hold]
    logger.info(f"[开弓ETF] 目标={target} 评分={[round(scores[e],3) for e in target]}")

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for etf in target:
        if etf in bar_dict and bar_dict[etf].is_trading:
            order_target_value(etf, value)
