# 原文链接：https://www.joinquant.com/post/45460
# 策略：穿越牛熊2.0（非小市值）年化50%的cta策略
# 作者：穿越牛熊
# 核心逻辑：用沪深300ETF做CTA趋势跟踪，RSRS择时
# 注：原版用futures_logic期货，此处改为ETF代理

import numpy as np


ETF_300  = '510300.XSHG'   # 沪深300ETF
BOND_ETF = '511010.XSHG'   # 国债ETF（空仓时持有）


def calc_rsrs_slope(prices, n=18):
    """计算RSRS斜率"""
    if len(prices) < n:
        return None
    y = np.array(prices[-n:], dtype=float)
    x = np.arange(n, dtype=float)
    b = np.polyfit(x, y, 1)
    return b[0]


def calc_rsrs_zscore(prices, n=18, window=250):
    """计算RSRS标准分（滚动Z-score）"""
    total = len(prices)
    if total < n + window:
        return None
    slopes = []
    for i in range(window):
        end = total - window + i + 1
        start = end - n
        if start < 0:
            continue
        y = np.array(prices[start:end], dtype=float)
        x = np.arange(n, dtype=float)
        b = np.polyfit(x, y, 1)
        slopes.append(b[0])
    if len(slopes) < 20:
        return None
    s = np.array(slopes)
    return (s[-1] - np.mean(s)) / (np.std(s) + 1e-9)


def init(context):
    context.etf = ETF_300
    context.bond = BOND_ETF
    context.in_market = False
    context.buy_threshold  =  0.7   # RSRS标准分买入阈值
    context.sell_threshold = -0.7   # RSRS标准分卖出阈值
    scheduler.run_daily(rsrs_cta, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rsrs_cta(context, bar_dict):
    """日度RSRS CTA策略"""
    prices = history_bars(context.etf, 350, '1d', 'close')
    if prices is None or len(prices) < 100:
        return

    p = np.array(prices, dtype=float)
    zscore = calc_rsrs_zscore(p, n=18, window=min(250, len(p) - 20))

    if zscore is None:
        # 数据不足时用均线替代
        if len(p) >= 60:
            ma20 = np.mean(p[-20:])
            ma60 = np.mean(p[-60:])
            signal_up   = p[-1] > ma20 and ma20 > ma60
            signal_down = p[-1] < ma20 * 0.98
        else:
            return
    else:
        signal_up   = zscore > context.buy_threshold
        signal_down = zscore < context.sell_threshold

    if signal_up and not context.in_market:
        context.in_market = True
        order_target_value(context.bond, 0)
        if context.etf in bar_dict and bar_dict[context.etf].is_trading:
            order_target_value(context.etf, context.portfolio.total_value * 0.95)
        logger.info(f"[穿越牛熊CTA] 入场 zscore={zscore}")

    elif signal_down and context.in_market:
        context.in_market = False
        order_target_value(context.etf, 0)
        if context.bond in bar_dict and bar_dict[context.bond].is_trading:
            order_target_value(context.bond, context.portfolio.total_value * 0.95)
        logger.info(f"[穿越牛熊CTA] 出场 zscore={zscore}")
