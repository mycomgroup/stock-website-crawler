# 原文链接：https://www.joinquant.com/post/45280
# 策略：中证500指增+CTA，胜率52%盈亏比1.9。不输顶尖私募
# 作者：CTA研究员
# 核心逻辑：中证500ETF+RSRS择时，趋势跟踪策略
# 注：原版用jqlib_ta+futures_logic，此处改为ETF代理期货

import numpy as np


ETF_500 = '510500.XSHG'   # 中证500ETF
BOND_ETF = '511010.XSHG'  # 国债ETF（空仓时持有）


def calc_rsrs(prices, n=18):
    """RSRS斜率指标"""
    if len(prices) < n:
        return None
    y = np.array(prices[-n:], dtype=float)
    x = np.arange(n, dtype=float)
    b = np.polyfit(x, y, 1)
    return b[0]


def calc_rsrs_zscore(prices, n=18, m=600):
    """RSRS标准分"""
    if len(prices) < n + m:
        return None
    slopes = []
    for i in range(m):
        idx = len(prices) - m + i
        if idx < n:
            continue
        y = np.array(prices[idx - n:idx], dtype=float)
        x = np.arange(n, dtype=float)
        b = np.polyfit(x, y, 1)
        slopes.append(b[0])
    if len(slopes) < 10:
        return None
    s = np.array(slopes)
    return (s[-1] - np.mean(s)) / (np.std(s) + 1e-9)


def init(context):
    context.etf = ETF_500
    context.bond = BOND_ETF
    context.in_market = False
    scheduler.run_daily(rsrs_trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rsrs_trade(context, bar_dict):
    """日度RSRS择时"""
    prices = history_bars(context.etf, 700, '1d', 'close')
    if prices is None or len(prices) < 200:
        return

    p = np.array(prices, dtype=float)

    # 简化RSRS：用18日线性回归斜率的滚动Z-score
    zscore = calc_rsrs_zscore(p, n=18, m=min(600, len(p) - 20))

    if zscore is None:
        # 数据不足时用简单动量
        ma20 = np.mean(p[-20:])
        ma60 = np.mean(p[-60:]) if len(p) >= 60 else ma20
        signal_up = p[-1] > ma20 > ma60
        signal_down = p[-1] < ma20
    else:
        signal_up   = zscore > 0.7
        signal_down = zscore < -0.7

    if signal_up and not context.in_market:
        context.in_market = True
        order_target_value(context.bond, 0)
        if context.etf in bar_dict and bar_dict[context.etf].is_trading:
            order_target_value(context.etf, context.portfolio.total_value * 0.95)
        logger.info(f"[中证500CTA] 入场 zscore={zscore}")

    elif signal_down and context.in_market:
        context.in_market = False
        order_target_value(context.etf, 0)
        if context.bond in bar_dict and bar_dict[context.bond].is_trading:
            order_target_value(context.bond, context.portfolio.total_value * 0.95)
        logger.info(f"[中证500CTA] 出场 zscore={zscore}")
