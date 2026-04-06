# 原文链接：https://www.joinquant.com/post/44810
# 策略：行业ETF轮动+择时，15年至今年化收益35%，回撤16%
# 作者：ETF轮动达人
# 核心逻辑：行业ETF动量轮动+BBI择时，选近期涨幅最强的行业ETF
# 注：原版用jqlib BBI指标，此处本地实现BBI

import numpy as np


# 行业ETF池
SECTOR_ETFS = [
    '512880.XSHG',  # 证券ETF
    '512690.XSHG',  # 酒ETF
    '159869.XSHE',  # 消费ETF
    '512760.XSHG',  # 芯片ETF
    '159992.XSHE',  # 创新药ETF
    '515030.XSHG',  # 新能源车ETF
    '512980.XSHG',  # 传媒ETF
    '515000.XSHG',  # 地产ETF
    '512400.XSHG',  # 有色金属ETF
    '516160.XSHG',  # 新能源ETF
]

MARKET_ETF = '510300.XSHG'  # 大盘择时用


def calc_bbi(prices):
    """BBI = (MA3 + MA6 + MA12 + MA24) / 4"""
    if len(prices) < 24:
        return None
    ma3  = np.mean(prices[-3:])
    ma6  = np.mean(prices[-6:])
    ma12 = np.mean(prices[-12:])
    ma24 = np.mean(prices[-24:])
    return (ma3 + ma6 + ma12 + ma24) / 4.0


def init(context):
    context.etf_pool = SECTOR_ETFS
    context.n_hold = 3
    context.lookback = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：BBI择时 + 动量选ETF"""
    # 大盘BBI择时
    mkt_prices = history_bars(MARKET_ETF, 30, '1d', 'close')
    if mkt_prices is not None and len(mkt_prices) >= 24:
        p = np.array(mkt_prices, dtype=float)
        bbi = calc_bbi(p)
        if bbi is not None and p[-1] < bbi:
            # 大盘在BBI下方，空仓
            for s in list(context.portfolio.positions.keys()):
                order_target_value(s, 0)
            logger.info("[行业ETF] BBI择时：大盘弱势，空仓")
            return

    # 计算各ETF动量
    momentum = {}
    for etf in context.etf_pool:
        prices = history_bars(etf, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback:
            continue
        p = np.array(prices, dtype=float)
        ret = p[-1] / p[0] - 1
        momentum[etf] = ret

    if not momentum:
        return

    sorted_etfs = sorted(momentum.keys(), key=lambda x: momentum[x], reverse=True)
    target = sorted_etfs[:context.n_hold]
    logger.info(f"[行业ETF] 目标={target}")

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
