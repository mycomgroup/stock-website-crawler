# 原文链接：https://www.joinquant.com/post/50xxx
# 策略：ETF动量轮动RSRS择时-V2.1
# 核心逻辑：ETF动量轮动V2.1，RSRS择时+动量评分，ETF池：510300/510500/159915/512880/511010

import numpy as np

ETF_POOL = ['510300.XSHG', '510500.XSHG', '159915.XSHE', '512880.XSHG', '511010.XSHG']
RSRS_N = 18
RSRS_THRESHOLD = 0.8
CASH_ETF = '511010.XSHG'  # 国债ETF作为现金替代

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:]); y = np.array(high[-n:])
    b = np.polyfit(x, y, 1)
    return b[0]

def init(context):
    context.etf_pool = ETF_POOL
    scheduler.run_weekly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 大盘RSRS择时
    try:
        hs300_high = history_bars('000300.XSHG', RSRS_N + 5, '1d', 'high')
        hs300_low = history_bars('000300.XSHG', RSRS_N + 5, '1d', 'low')
        market_rsrs = calc_rsrs(hs300_high, hs300_low, RSRS_N)
        market_ok = market_rsrs > RSRS_THRESHOLD
    except Exception:
        market_ok = True

    scores = {}
    for etf in context.etf_pool:
        if etf == CASH_ETF:
            continue
        try:
            closes = history_bars(etf, 25, '1d', 'close')
            highs = history_bars(etf, RSRS_N + 5, '1d', 'high')
            lows = history_bars(etf, RSRS_N + 5, '1d', 'low')
            if len(closes) < 20:
                continue
            mom_20 = (closes[-1] - closes[-20]) / closes[-20]
            mom_5 = (closes[-1] - closes[-5]) / closes[-5]
            rsrs = calc_rsrs(highs, lows, RSRS_N)
            # 综合评分
            scores[etf] = mom_20 * 0.6 + mom_5 * 0.4
            if rsrs < 0.5:
                scores[etf] *= 0.5
        except Exception as e:
            logger.info(f"ETF {etf} 计算失败: {e}")

    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    if not market_ok or not scores:
        # 市场不好，持有国债ETF
        order_target_value(CASH_ETF, context.portfolio.cash * 0.95)
        logger.info("市场RSRS偏低，持有国债ETF")
        return

    best = max(scores, key=scores.get)
    if scores[best] > 0:
        order_target_value(best, context.portfolio.cash * 0.95)
        logger.info(f"买入 {best}，评分 {scores[best]:.4f}")
    else:
        order_target_value(CASH_ETF, context.portfolio.cash * 0.95)
