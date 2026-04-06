# 原文链接：https://www.joinquant.com/post/64000
# 策略：A股最强板块动量趋势最终版
# 核心逻辑：板块动量趋势，选近期涨幅最强的行业ETF，持有至动量减弱。

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
        '512010.XSHG',  # 军工ETF
        '512800.XSHG',  # 银行ETF
        '512880.XSHG',  # 证券ETF
        '515030.XSHG',  # 新能源ETF
        '516160.XSHG',  # 新能源车ETF
        '159915.XSHE',  # 创业板ETF
        '159928.XSHE',  # 消费ETF
        '512760.XSHG',  # 芯片ETF
        '515700.XSHG',  # 新能源车ETF
        '159938.XSHE',  # 医疗ETF
        '512660.XSHG',  # 军工ETF
        '515000.XSHG',  # 地产ETF
    ]
    context.short_mom = 5
    context.long_mom = 20
    context.hold_etf = None
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.long_mom + 5, '1d', 'close')
            highs = history_bars(etf, 25, '1d', 'high')
            lows = history_bars(etf, 25, '1d', 'low')
            if closes is None or len(closes) < context.long_mom + 1:
                continue
            short_m = (closes[-1] - closes[-context.short_mom]) / closes[-context.short_mom]
            long_m = (closes[-1] - closes[-context.long_mom]) / closes[-context.long_mom]
            rsrs = calc_rsrs(highs, lows) if highs is not None and lows is not None else 1.0
            scores[etf] = short_m * 0.5 + long_m * 0.3 + rsrs * 0.2
        except Exception:
            continue

    if not scores:
        return

    best_etf = max(scores, key=scores.get)
    best_score = scores[best_etf]

    if best_score < 0:
        if context.hold_etf:
            order_target_value(context.hold_etf, 0)
            context.hold_etf = None
        logger.info("板块动量为负，空仓")
        return

    if context.hold_etf and context.hold_etf != best_etf:
        order_target_value(context.hold_etf, 0)

    order_target_value(best_etf, context.portfolio.total_value * 0.95)
    context.hold_etf = best_etf
    logger.info(f"最强板块动量，持有 {best_etf}，评分={best_score:.4f}")
