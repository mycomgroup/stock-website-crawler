# 原文链接：https://www.joinquant.com/post/51xxx
# 策略：行业反转效应（年化32%，回撤8%）
# 核心逻辑：行业反转效应，选近期表现最差的行业ETF，等待反转，月度调仓

import numpy as np

# 行业ETF池
INDUSTRY_ETFS = [
    '512010.XSHG',  # 医疗ETF
    '512660.XSHG',  # 军工ETF
    '512800.XSHG',  # 银行ETF
    '512880.XSHG',  # 证券ETF
    '515000.XSHG',  # 科技ETF
    '159928.XSHE',  # 消费ETF
    '159915.XSHE',  # 创业板ETF
    '510300.XSHG',  # 沪深300ETF
]
REVERSAL_DAYS = 20
HOLD_NUM = 2

def init(context):
    context.etf_pool = INDUSTRY_ETFS
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    returns = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, REVERSAL_DAYS + 1, '1d', 'close')
            if len(closes) < REVERSAL_DAYS + 1:
                continue
            ret = (closes[-1] - closes[0]) / closes[0]
            returns[etf] = ret
        except Exception as e:
            logger.info(f"ETF {etf} 计算失败: {e}")

    if not returns:
        return

    # 选近期表现最差的ETF（反转效应）
    sorted_etfs = sorted(returns, key=returns.get, reverse=False)
    worst_etfs = sorted_etfs[:HOLD_NUM]

    value_per = context.portfolio.cash / len(worst_etfs)
    for etf in worst_etfs:
        order_target_value(etf, value_per)
        logger.info(f"买入反转ETF {etf}，近期收益 {returns[etf]:.4f}")
