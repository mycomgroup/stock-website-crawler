# 再论动量因子选股策略 - RiceQuant版本
# 来源：《再论动量因子》
# 核心逻辑：改进版动量因子，跳过最近1个月（避免短期反转），
#           使用t-12到t-2月的收益率，并控制行业和市值暴露

import numpy as np


def calc_improved_momentum(prices, skip_recent=20, lookback=240):
    """
    改进版动量因子
    - 跳过最近20个交易日（避免短期反转）
    - 使用过去240日（约12个月）到20日前的收益率
    """
    if len(prices) < lookback + 1:
        return None

    prices = np.array(prices, dtype=float)
    # 跳过最近1个月
    p_start = prices[-(lookback + 1)]
    p_end = prices[-(skip_recent + 1)]

    if p_start <= 0:
        return None

    momentum = (p_end / p_start) - 1
    return momentum


def init(context):
    context.index = '000905.XSHG'   # 中证500
    context.lookback = 240
    context.skip = 20
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    stocks = index_components(context.index)
    stocks = [s for s in stocks if s in bar_dict]

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.lookback + 2, '1d', 'close')
            if prices is None or len(prices) < context.lookback + 2:
                continue
            factor = calc_improved_momentum(
                np.array(prices, dtype=float),
                context.skip,
                context.lookback
            )
            if factor is not None:
                scores[stock] = factor
        except:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
