# 原文链接：https://www.joinquant.com/post/45130
# 策略：年初至今4倍，极致的Day Trading，56.8%胜率
# 作者：Day Trading达人
# 核心逻辑：BBI多头+量能放大的日内交易策略，开盘买入收盘卖出
# 注：原版用jqlib BBI，此处本地实现BBI

import numpy as np


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
    context.n_stocks = 5
    context.stock_pool = []
    scheduler.run_daily(before_open, time_rule=market_open(minute=0))
    scheduler.run_daily(open_buy, time_rule=market_open(minute=5))
    scheduler.run_daily(close_sell, time_rule=market_close(minute=5))


def handle_bar(context, bar_dict):
    pass


def before_open(context, bar_dict):
    """盘前：BBI多头+量能放大筛选"""
    stocks_500 = index_components('000905.XSHG')
    stocks_500 = [s for s in stocks_500 if not s.startswith('688')]

    candidates = []
    for s in stocks_500:
        prices  = history_bars(s, 30, '1d', 'close')
        volumes = history_bars(s, 10, '1d', 'volume')
        if prices is None or len(prices) < 24:
            continue
        if volumes is None or len(volumes) < 5:
            continue

        p = np.array(prices, dtype=float)
        v = np.array(volumes, dtype=float)

        bbi = calc_bbi(p)
        if bbi is None:
            continue

        # BBI多头：收盘价在BBI上方
        if p[-1] <= bbi:
            continue

        # 量能放大：近3日均量 > 近10日均量 * 1.2
        vol_recent = np.mean(v[-3:])
        vol_avg    = np.mean(v)
        if vol_recent < vol_avg * 1.2:
            continue

        candidates.append(s)

    context.stock_pool = candidates[:context.n_stocks]
    logger.info(f"[Day Trading] 候选={len(context.stock_pool)}")


def open_buy(context, bar_dict):
    """开盘后5分钟买入"""
    # 先清仓昨日持仓
    for s in list(context.portfolio.positions.keys()):
        order_target_value(s, 0)

    if not context.stock_pool:
        return

    n = len(context.stock_pool)
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
            logger.info(f"[Day Trading] 买入 {s}")


def close_sell(context, bar_dict):
    """收盘前5分钟清仓"""
    for s in list(context.portfolio.positions.keys()):
        order_target_value(s, 0)
    logger.info("[Day Trading] 收盘清仓")
