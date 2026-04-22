# 原文链接：https://www.joinquant.com/post/57002
# 策略：韶华研究之五_ETF轮动
# 核心逻辑：韶华ETF轮动，用动量+RSRS双信号选ETF，ETF池：510300/510500/159915/511010。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:])
    y = np.array(high[-n:])
    b = np.polyfit(x, y, 1)
    return b[0]

def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300ETF
        '510500.XSHG',  # 中证500ETF
        '159915.XSHE',  # 创业板ETF
        '511010.XSHG',  # 国债ETF（避险）
    ]
    context.momentum_days = 20
    context.rsrs_n = 18
    context.hold_etf = None
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.momentum_days + 1, '1d', 'close')
            highs = history_bars(etf, context.rsrs_n + 5, '1d', 'high')
            lows = history_bars(etf, context.rsrs_n + 5, '1d', 'low')
            if closes is None or highs is None or lows is None:
                continue
            if len(closes) < context.momentum_days + 1 or len(highs) < context.rsrs_n:
                continue
            mom = (closes[-1] - closes[0]) / closes[0]
            rsrs = calc_rsrs(highs, lows, context.rsrs_n)
            # 综合评分：动量 + RSRS归一化
            scores[etf] = mom + rsrs * 0.1
        except Exception:
            continue

    if not scores:
        return

    best_etf = max(scores, key=scores.get)
    best_score = scores[best_etf]

    # 国债ETF作为避险，若最优为国债则空仓股票
    if best_score < 0:
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        context.hold_etf = None
        logger.info("ETF轮动：综合评分为负，空仓")
        return

    if context.hold_etf and context.hold_etf != best_etf:
        order_target_value(context.hold_etf, 0)

    order_target_value(best_etf, context.portfolio.total_value * 0.95)
    context.hold_etf = best_etf
    logger.info(f"韶华ETF轮动，持有 {best_etf}，评分={best_score:.4f}")
