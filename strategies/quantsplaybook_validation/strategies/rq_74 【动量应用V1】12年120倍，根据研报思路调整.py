# 【动量应用V1】12年120倍，根据研报思路调整 - RiceQuant版本
# 原文：https://www.joinquant.com/post/38163
# 作者：free
# 注：残差波动率用历史波动率近似，RSRS择时

import numpy as np


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_index = '000300.XSHG'
    context.hold_num = 20
    context.vol_window = 60
    context.N = 18
    context.M = 300
    context.score_threshold = 0.7
    context.slope_series = []
    context.slope_initialized = False
    context.last_month = -1
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def _init_slopes(context):
    total = context.N + context.M
    highs = history_bars('000300.XSHG', total, '1d', 'high')
    lows = history_bars('000300.XSHG', total, '1d', 'low')
    if highs is None or lows is None or len(highs) < total:
        return []
    result = []
    for i in range(context.M):
        _lows = lows[i: i + context.N]
        _highs = highs[i: i + context.N]
        slope, _ = np.polyfit(_lows, _highs, 1)
        result.append(slope)
    return result


def _rsrs_signal(context):
    highs = history_bars('000300.XSHG', context.N, '1d', 'high')
    lows = history_bars('000300.XSHG', context.N, '1d', 'low')
    if highs is None or lows is None or len(highs) < context.N:
        return 'KEEP'
    lows = lows
    highs = highs
    slope, intercept = np.polyfit(lows, highs, 1)
    context.slope_series.append(slope)
    series = context.slope_series[-context.M:]
    if len(series) < 2:
        return 'KEEP'
    mean = np.mean(series)
    std = np.std(series)
    if std == 0:
        return 'KEEP'
    fitted = slope * lows + intercept
    ss_res = np.sum((highs - fitted) ** 2)
    ss_tot = np.sum((highs - np.mean(highs)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    zscore = (series[-1] - mean) / std * r2
    if zscore > context.score_threshold:
        return 'BUY'
    if zscore < -context.score_threshold:
        return 'SELL'
    return 'KEEP'


def get_stock_list(context, bar_dict):
    stocks = index_components(context.stock_index)
    valid = [s for s in stocks if s in bar_dict and bar_dict[s].is_trading]
    if not valid:
        return []
    vols = {}
    for s in valid:
        prices = history_bars(s, context.vol_window + 1, '1d', 'close')
        if prices is None or len(prices) < context.vol_window + 1:
            continue
        rets = np.diff(np.log(prices + 1e-10))
        vols[s] = np.std(rets)
    if not vols:
        return []
    sorted_stocks = sorted(vols, key=vols.get)
    return sorted_stocks[: context.hold_num]


def trade(context, bar_dict):
    if context.now.month == context.last_month:
        return
    context.last_month = context.now.month

    signal = _rsrs_signal(context)

    if signal == 'SELL':
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    target = get_stock_list(context, bar_dict)
    if not target:
        return

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    w = 1.0 / len(target)
    for s in target:
        order_target_value(s, context.portfolio.total_value * w * 0.95)
