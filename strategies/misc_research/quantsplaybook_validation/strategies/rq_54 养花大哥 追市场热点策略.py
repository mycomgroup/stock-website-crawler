# 原文链接：https://www.joinquant.com/post/54000
# 策略：养花大哥 追市场热点策略
# 核心逻辑：追市场热点，选近5日涨幅最强的行业ETF，持有至动量减弱。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    # 行业ETF池
    context.etf_pool = [
        '512010.XSHG',  # 军工ETF
        '512660.XSHG',  # 军工ETF
        '512800.XSHG',  # 银行ETF
        '512880.XSHG',  # 证券ETF
        '515000.XSHG',  # 地产ETF
        '515030.XSHG',  # 新能源ETF
        '516160.XSHG',  # 新能源车ETF
        '159915.XSHE',  # 创业板ETF
        '159928.XSHE',  # 消费ETF
        '159938.XSHE',  # 医疗ETF
        '512760.XSHG',  # 芯片ETF
        '515700.XSHG',  # 新能源车ETF
    ]
    context.hold_etf = None
    context.momentum_days = 5
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

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

    # 动量为负则空仓
    if best_mom < 0:
        if context.hold_etf:
            order_target_value(context.hold_etf, 0)
            context.hold_etf = None
            logger.info("热点动量为负，空仓")
        return

    if context.hold_etf and context.hold_etf != best_etf:
        order_target_value(context.hold_etf, 0)

    order_target_value(best_etf, context.portfolio.total_value * 0.95)
    context.hold_etf = best_etf
    logger.info(f"追热点买入 {best_etf}，5日动量={best_mom:.2%}")
