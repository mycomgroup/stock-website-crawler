# 原文链接：https://www.joinquant.com/post/45340
# 策略：追涨大师（超额142）
# 作者：追涨大师
# 核心逻辑：选近20日涨幅最强的股票，追涨持有，周度调仓
# 注：原版用ml_lib辅助，此处改为纯动量追涨策略

import numpy as np


def init(context):
    context.n_stocks = 10
    context.lookback = 20
    context.stock_pool = []
    # 周度调仓
    scheduler.run_weekly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """周度再平衡：选近20日涨幅最强的股票"""
    # 从中证500+沪深300中选
    stocks_300 = set(index_components('000300.XSHG'))
    stocks_500 = set(index_components('000905.XSHG'))
    universe = list(stocks_300 | stocks_500)
    universe = [s for s in universe if not s.startswith('688')]

    # 计算动量
    momentum = {}
    for s in universe:
        prices = history_bars(s, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback:
            continue
        p = np.array(prices, dtype=float)
        ret = p[-1] / p[0] - 1
        momentum[s] = ret

    if not momentum:
        logger.info("[追涨大师] 无有效数据")
        return

    # 选涨幅最强的前N只
    sorted_stocks = sorted(momentum.keys(), key=lambda x: momentum[x], reverse=True)

    # 过滤：近5日涨幅不能超过30%（避免追高）
    filtered = []
    for s in sorted_stocks:
        prices = history_bars(s, 6, '1d', 'close')
        if prices is None or len(prices) < 5:
            continue
        p = np.array(prices, dtype=float)
        ret5 = p[-1] / p[0] - 1
        if ret5 < 0.30:  # 5日涨幅不超过30%
            filtered.append(s)
        if len(filtered) >= context.n_stocks:
            break

    context.stock_pool = filtered[:context.n_stocks]
    logger.info(f"[追涨大师] 选股={context.stock_pool} 动量={[round(momentum.get(s,0)*100,1) for s in context.stock_pool]}%")

    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
