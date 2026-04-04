# 市场微观结构反转因子选股策略 - RiceQuant版本
# 来源：《开源证券-市场微观结构研究系列（1）：A股反转之力的微观来源》
# 核心逻辑：A股反转效应来源于做市商的库存调整和散户的处置效应
#           短期（5日）反转因子在A股有显著效果
#           结合成交量加权，识别真实的反转信号

import numpy as np


def calc_microstructure_reversal(prices, volumes, window=5):
    """
    微观结构反转因子
    = 成交量加权的短期收益率（取负值）
    高成交量的下跌更可能反转（做市商库存调整）
    """
    if len(prices) < window + 1 or len(volumes) < window:
        return None

    p = np.array(prices[-window-1:], dtype=float)
    v = np.array(volumes[-window:], dtype=float)

    returns = np.diff(p) / p[:-1]

    # 成交量加权收益率
    v_sum = v.sum()
    if v_sum == 0:
        return None

    vw_return = np.average(returns, weights=v)

    # 反转因子（取负值）
    return -vw_return


def init(context):
    context.index = '000905.XSHG'
    context.window = 5
    context.top_n = 50      # 微观结构反转需要更多持仓分散
    context.week = -1


def handle_bar(context, bar_dict):
    # 周度调仓（短期反转）
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return
    context.week = current_week

    stocks = index_components(context.index)
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.window + 2, '1d', 'close')
            volumes = history_bars(stock, context.window + 1, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            factor = calc_microstructure_reversal(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
                context.window
            )
            if factor is not None:
                scores[stock] = factor
        except Exception:
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
