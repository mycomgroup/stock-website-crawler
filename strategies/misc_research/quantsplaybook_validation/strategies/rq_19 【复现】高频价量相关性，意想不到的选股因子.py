# 原文链接：https://www.joinquant.com/post/44600
# 策略：【复现】高频价量相关性，意想不到的选股因子
# 作者：复现系列
# 核心逻辑：计算个股近N日价格与成交量的相关系数作为因子，
#           选相关性最低（量价背离）的股票，月度调仓
# 注：原版用sklearn PCA，此处改为直接用价量相关性因子选股

import numpy as np


def calc_price_volume_corr(stock, n=20):
    """计算价量相关系数，越低说明量价背离越强"""
    closes = history_bars(stock, n, '1d', 'close')
    volumes = history_bars(stock, n, '1d', 'volume')
    if closes is None or volumes is None or len(closes) < n:
        return None
    closes = np.array(closes, dtype=float)
    volumes = np.array(volumes, dtype=float)
    if np.std(closes) < 1e-9 or np.std(volumes) < 1e-9:
        return None
    corr = np.corrcoef(closes, volumes)[0, 1]
    return corr


def init(context):
    context.n_stocks = 10
    context.lookback = 20
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    # 获取沪深300成分股
    stocks = index_components('000300.XSHG')
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 计算价量相关系数
    corr_dict = {}
    for s in stocks:
        c = calc_price_volume_corr(s, context.lookback)
        if c is not None:
            corr_dict[s] = c

    if not corr_dict:
        logger.info("[价量相关] 无有效数据")
        return

    # 选相关性最低的股票（量价背离最强）
    sorted_stocks = sorted(corr_dict.keys(), key=lambda x: corr_dict[x])
    context.stock_pool = sorted_stocks[:context.n_stocks]
    logger.info(f"[价量相关] 选股={context.stock_pool}")

    # 卖出不在池中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    # 等权买入
    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
