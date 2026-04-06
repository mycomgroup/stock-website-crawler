# 原文链接：https://www.joinquant.com/post/ETF核心资产轮动动量因子加RSRS择时每日策略
# 策略：ETF核心资产轮动动量因子加RSRS择时每日策略
# 核心逻辑：宽基ETF动量轮动+RSRS择时，每日调仓。ETF池：510300/510500/159915/512880/511010。

import numpy as np

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:]); y = np.array(high[-n:])
    b = np.polyfit(x, y, 1); return b[0]

def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300ETF
        '510500.XSHG',  # 中证500ETF
        '159915.XSHE',  # 创业板ETF
        '512880.XSHG',  # 证券ETF
        '511010.XSHG',  # 国债ETF（避险）
    ]
    context.bond_etf = '511010.XSHG'
    context.rsrs_threshold = 1.0
    context.momentum_n = 20
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 计算RSRS择时信号（用沪深300ETF）
    try:
        high = history_bars('510300.XSHG', 20, '1d', 'high')
        low = history_bars('510300.XSHG', 20, '1d', 'low')
        rsrs = calc_rsrs(high, low, 18)
    except Exception:
        rsrs = 1.0

    if rsrs < context.rsrs_threshold:
        # RSRS信号弱，持有债券ETF
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info(f"RSRS={rsrs:.2f}，持有债券ETF")
        return

    # 计算各ETF动量
    momentum = {}
    for etf in context.etf_pool:
        if etf == context.bond_etf:
            continue
        try:
            prices = history_bars(etf, context.momentum_n + 1, '1d', 'close')
            if len(prices) > context.momentum_n:
                mom = (prices[-1] - prices[0]) / prices[0]
                momentum[etf] = mom
        except Exception:
            continue

    if not momentum:
        return

    # 选动量最强的ETF
    best_etf = max(momentum, key=momentum.get)
    if momentum[best_etf] < 0:
        best_etf = context.bond_etf

    for s in list(context.portfolio.positions.keys()):
        if s != best_etf:
            order_target_value(s, 0)
    order_target_value(best_etf, context.portfolio.total_value * 0.95)
    logger.info(f"RSRS={rsrs:.2f}，选择ETF: {best_etf}，动量: {momentum.get(best_etf, 0):.2%}")
