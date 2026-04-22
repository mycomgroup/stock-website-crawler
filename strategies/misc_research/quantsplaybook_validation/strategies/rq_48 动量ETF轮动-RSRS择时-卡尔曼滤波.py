# 原文链接：https://www.joinquant.com/post/48xxx
# 策略：动量ETF轮动-RSRS择时-卡尔曼滤波
# 核心逻辑：ETF动量轮动+RSRS择时，用简单线性滤波代替卡尔曼滤波，ETF池：510300/510500/159915/511010

import numpy as np

ETF_POOL = ['510300.XSHG', '510500.XSHG', '159915.XSHE', '511010.XSHG']
RSRS_N = 18
RSRS_THRESHOLD = 0.7

def ema(p, n):
    k = 2.0 / (n + 1); e = p[0]; r = []
    for x in p: e = x * k + e * (1 - k); r.append(e)
    return np.array(r)

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:]); y = np.array(high[-n:])
    b = np.polyfit(x, y, 1)
    return b[0]

def linear_filter(prices, window=5):
    """简单线性滤波代替卡尔曼滤波"""
    weights = np.arange(1, window + 1, dtype=float)
    weights /= weights.sum()
    if len(prices) < window:
        return prices[-1]
    return np.dot(prices[-window:], weights)

def init(context):
    context.etf_pool = ETF_POOL
    scheduler.run_weekly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 30, '1d', 'close')
            highs = history_bars(etf, RSRS_N + 5, '1d', 'high')
            lows = history_bars(etf, RSRS_N + 5, '1d', 'low')
            if len(closes) < 25 or len(highs) < RSRS_N or len(lows) < RSRS_N:
                continue
            # 动量评分：近20日收益率
            momentum = (closes[-1] - closes[-20]) / closes[-20]
            # RSRS择时
            rsrs = calc_rsrs(highs, lows, RSRS_N)
            # 线性滤波平滑价格
            filtered_price = linear_filter(closes, window=5)
            trend = 1 if filtered_price > np.mean(closes[-20:]) else 0
            scores[etf] = momentum * trend * (1 if rsrs > RSRS_THRESHOLD else 0.3)
        except Exception as e:
            logger.info(f"ETF {etf} 计算失败: {e}")

    # 清仓不在候选的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in scores or scores.get(stock, 0) <= 0:
            order_target_value(stock, 0)

    if not scores:
        return

    # 选最高分ETF
    best = max(scores, key=scores.get)
    if scores[best] > 0:
        order_target_value(best, context.portfolio.cash * 0.95)
        logger.info(f"买入 {best}，评分 {scores[best]:.4f}")
