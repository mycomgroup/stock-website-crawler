# 原文链接：https://www.joinquant.com/post/44750
# 策略：以"网红"ETF轮动为例
# 作者：ETF爱好者
# 核心逻辑：经典ETF动量轮动，选近N日涨幅最高的ETF持有，月度调仓

import numpy as np


# 网红ETF池
ETF_POOL = [
    '510300.XSHG',  # 沪深300ETF
    '510500.XSHG',  # 中证500ETF
    '159915.XSHE',  # 创业板ETF
    '512880.XSHG',  # 证券ETF
    '512690.XSHG',  # 酒ETF
    '159869.XSHE',  # 消费ETF
    '512760.XSHG',  # 芯片ETF
    '159992.XSHE',  # 创新药ETF
    '515030.XSHG',  # 新能源车ETF
    '159740.XSHE',  # 恒生科技ETF
]


def init(context):
    context.etf_pool = ETF_POOL
    context.n_hold = 3
    context.lookback = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：选动量最强的ETF"""
    momentum = {}
    for etf in context.etf_pool:
        prices = history_bars(etf, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback:
            continue
        p = np.array(prices, dtype=float)
        ret = p[-1] / p[0] - 1
        momentum[etf] = ret

    if not momentum:
        logger.info("[ETF轮动] 无有效数据")
        return

    # 按动量降序排列，选前N只
    sorted_etfs = sorted(momentum.keys(), key=lambda x: momentum[x], reverse=True)
    target = sorted_etfs[:context.n_hold]
    logger.info(f"[ETF轮动] 目标ETF={target} 动量={[round(momentum[e]*100,2) for e in target]}%")

    # 卖出不在目标中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    # 等权买入目标ETF
    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for etf in target:
        if etf in bar_dict and bar_dict[etf].is_trading:
            order_target_value(etf, value)
