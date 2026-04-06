# 原文链接：https://www.joinquant.com/post/61001
# 策略：简单ETF策略年化97
# 核心逻辑：简单ETF策略，选近N日涨幅最高的ETF持有，月度调仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300ETF
        '510500.XSHG',  # 中证500ETF
        '159915.XSHE',  # 创业板ETF
        '511010.XSHG',  # 国债ETF
        '518880.XSHG',  # 黄金ETF
        '159938.XSHE',  # 消费ETF
        '512760.XSHG',  # 芯片ETF
        '515030.XSHG',  # 新能源ETF
    ]
    context.momentum_days = 20
    context.hold_etf = None
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.momentum_days + 1, '1d', 'close')
            if closes is not None and len(closes) >= context.momentum_days + 1:
                mom = (closes[-1] - closes[0]) / closes[0]
                scores[etf] = mom
        except Exception:
            continue

    if not scores:
        return

    best_etf = max(scores, key=scores.get)
    best_mom = scores[best_etf]

    if best_mom < 0:
        if context.hold_etf:
            order_target_value(context.hold_etf, 0)
            context.hold_etf = None
        logger.info("ETF动量为负，空仓")
        return

    if context.hold_etf and context.hold_etf != best_etf:
        order_target_value(context.hold_etf, 0)

    order_target_value(best_etf, context.portfolio.total_value * 0.95)
    context.hold_etf = best_etf
    logger.info(f"简单ETF策略，持有 {best_etf}，{context.momentum_days}日动量={best_mom:.2%}")
