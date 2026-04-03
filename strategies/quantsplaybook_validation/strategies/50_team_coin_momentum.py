# 个股动量效应识别及球队硬币因子选股策略 - RiceQuant版本
# 来源：《个股动量效应的识别及球队硬币因子》
# 核心逻辑：球队硬币因子（Team Coin Factor）
#           识别个股是否具有持续的动量效应（连续上涨/下跌的概率）
#           连续上涨概率高的股票具有动量特征，选择动量股

import numpy as np


def calc_team_coin_factor(returns, window=60):
    """
    球队硬币因子：
    计算个股收益率序列中，连续同向变动的概率
    P(up|up) - P(up|down) 越大，动量效应越强
    """
    if len(returns) < window:
        return None

    r = np.array(returns[-window:], dtype=float)
    signs = np.sign(r)

    # 计算条件概率
    up_after_up = 0
    up_after_down = 0
    count_up = 0
    count_down = 0

    for i in range(1, len(signs)):
        if signs[i-1] > 0:
            count_up += 1
            if signs[i] > 0:
                up_after_up += 1
        elif signs[i-1] < 0:
            count_down += 1
            if signs[i] > 0:
                up_after_down += 1

    if count_up == 0 or count_down == 0:
        return None

    p_up_given_up = up_after_up / count_up
    p_up_given_down = up_after_down / count_down

    # 球队硬币因子：动量强度
    team_coin = p_up_given_up - p_up_given_down
    return team_coin


def init(context):
    context.index = '000905.XSHG'
    context.window = 60
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
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            if prices is None or len(prices) < context.window + 1:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]

            factor = calc_team_coin_factor(returns, context.window)
            if factor is not None:
                scores[stock] = factor
        except:
            continue

    if not scores:
        return

    # 选动量效应强的股票
    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
