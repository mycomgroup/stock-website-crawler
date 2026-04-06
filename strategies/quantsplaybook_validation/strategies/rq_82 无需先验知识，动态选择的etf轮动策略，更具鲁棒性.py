# 无需先验知识，动态选择的ETF轮动策略，更具鲁棒性 - RiceQuant版本
# 原文：https://www.joinquant.com/post/24429
# 作者：热爱大自然
# 注：固定ETF池，按流动性+动量动态选择，大盘成交量择时

import numpy as np


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)

    # 固定ETF池（覆盖宽基、行业、商品、债券等）
    context.etf_pool = [
        '510050.XSHG',  # 上证50 ETF
        '510300.XSHG',  # 沪深300 ETF
        '510500.XSHG',  # 中证500 ETF
        '159915.XSHE',  # 创业板 ETF
        '513100.XSHG',  # 纳指100 ETF
        '518880.XSHG',  # 黄金 ETF
        '511010.XSHG',  # 国债 ETF
        '159985.XSHE',  # 豆粕 ETF
        '162411.XSHE',  # 华宝油气
        '513500.XSHG',  # 标普500 ETF
        '510880.XSHG',  # 红利 ETF
        '159920.XSHE',  # 恒生 ETF
        '512880.XSHG',  # 证券 ETF
        '515000.XSHG',  # 地产 ETF
        '159949.XSHE',  # 创业板50 ETF
        '513520.XSHG',  # 日经225 ETF
    ]

    context.hold_num = 3          # 持仓ETF数量
    context.momentum_window = 20  # 动量计算窗口（交易日）
    context.ma_window = 20        # 均线窗口
    context.vol_ma_window = 20    # 成交量均线窗口
    context.cash_etf = '511010.XSHG'  # 空仓时持有国债ETF
    context.bear_days = 0         # 连续缩量天数计数
    context.bear_threshold = 6    # 连续缩量超过此天数则空仓

    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def _market_timing(context, bar_dict):
    """
    大盘成交量择时：
    若大盘成交量连续N天低于MA，则认为市场疲软，转入现金（国债ETF）
    """
    index_code = '000300.XSHG'
    vols = history_bars(index_code, context.vol_ma_window + 1, '1d', 'volume')
    if vols is None or len(vols) < context.vol_ma_window + 1:
        return True  # 数据不足，默认持仓

    vol_ma = np.mean(vols[:-1])
    current_vol = vols[-1]

    if current_vol < vol_ma:
        context.bear_days += 1
    else:
        context.bear_days = 0

    return context.bear_days < context.bear_threshold


def _get_valid_etfs(context):
    """过滤出具备足够历史数据的ETF"""
    return list(context.etf_pool)


def _calc_momentum(etf, window):
    """计算ETF近期动量（收益率）"""
    prices = history_bars(etf, window + 1, '1d', 'close')
    if prices is None or len(prices) < window + 1:
        return None
    return prices[-1] / prices[0] - 1


def _calc_volume_rank(etf, window):
    """计算ETF近期平均成交量（流动性代理）"""
    vols = history_bars(etf, window, '1d', 'volume')
    if vols is None or len(vols) < window:
        return 0
    return np.mean(vols)


def _above_ma(etf, window):
    """价格是否在均线之上（趋势过滤）"""
    prices = history_bars(etf, window + 1, '1d', 'close')
    if prices is None or len(prices) < window + 1:
        return False
    ma = np.mean(prices[:-1])
    return prices[-1] > ma


def select_etfs(context, bar_dict):
    """
    选股逻辑：
    1. 按近期平均成交量排序，取流动性最好的一半
    2. 在流动性过滤后，选动量为正且价格在均线上方的ETF
    3. 按动量排序，取前N只
    """
    valid = _get_valid_etfs(context)
    if not valid:
        return []

    # 流动性过滤：取成交量前50%
    vol_scores = {}
    for e in valid:
        v = _calc_volume_rank(e, context.momentum_window)
        if v > 0:
            vol_scores[e] = v

    if not vol_scores:
        return []

    sorted_by_vol = sorted(vol_scores, key=vol_scores.get, reverse=True)
    liquid_pool = sorted_by_vol[: max(1, len(sorted_by_vol) // 2)]

    # 动量过滤：正动量 + 价格在均线上方
    momentum_scores = {}
    for e in liquid_pool:
        mom = _calc_momentum(e, context.momentum_window)
        if mom is None:
            continue
        if mom > 0.01 and _above_ma(e, context.ma_window):
            momentum_scores[e] = mom

    if not momentum_scores:
        return []

    sorted_by_mom = sorted(momentum_scores, key=momentum_scores.get, reverse=True)
    return sorted_by_mom[: context.hold_num]


def trade(context, bar_dict):
    """每日执行：大盘择时 + ETF轮动"""
    in_market = _market_timing(context, bar_dict)

    if not in_market:
        # 市场疲软，全部转入国债ETF
        for e in list(context.portfolio.positions.keys()):
            if e != context.cash_etf:
                order_target_value(e, 0)
        order_target_value(context.cash_etf, context.portfolio.total_value * 0.95)
        return

    target = select_etfs(context, bar_dict)

    if not target:
        # 无合适ETF，持有国债ETF
        for e in list(context.portfolio.positions.keys()):
            if e != context.cash_etf:
                order_target_value(e, 0)
        order_target_value(context.cash_etf, context.portfolio.total_value * 0.95)
        return

    # 清仓不在目标列表的持仓
    for e in list(context.portfolio.positions.keys()):
        if e not in target:
            order_target_value(e, 0)

    # 等权买入目标ETF
    w = 1.0 / len(target)
    for e in target:
        order_target_value(e, context.portfolio.total_value * w * 0.95)
