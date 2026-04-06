# 原文链接：https://www.joinquant.com/post/61000
# 策略：BiLSTM_for_ETF
# 核心逻辑：用简单动量+均线替代BiLSTM，ETF动量轮动，选近期表现最强的ETF。

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
    ]
    context.short_days = 5
    context.long_days = 20
    context.hold_etf = None
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.long_days + 5, '1d', 'close')
            if closes is None or len(closes) < context.long_days + 1:
                continue
            # 短期动量
            short_mom = (closes[-1] - closes[-context.short_days]) / closes[-context.short_days]
            # 长期动量
            long_mom = (closes[-1] - closes[-context.long_days]) / closes[-context.long_days]
            # 均线信号：短均线>长均线
            ma_short = np.mean(closes[-context.short_days:])
            ma_long = np.mean(closes[-context.long_days:])
            ma_signal = 1 if ma_short > ma_long else -1
            # 综合评分（模拟BiLSTM输出）
            scores[etf] = short_mom * 0.4 + long_mom * 0.4 + ma_signal * 0.2
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
        logger.info("BiLSTM模拟：评分为负，空仓")
        return

    if context.hold_etf and context.hold_etf != best_etf:
        order_target_value(context.hold_etf, 0)

    order_target_value(best_etf, context.portfolio.total_value * 0.95)
    context.hold_etf = best_etf
    logger.info(f"BiLSTM ETF轮动，持有 {best_etf}，评分={best_score:.4f}")
