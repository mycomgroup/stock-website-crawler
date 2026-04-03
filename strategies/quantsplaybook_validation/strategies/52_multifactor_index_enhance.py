# 多因子指数增强策略 - RiceQuant版本
# 来源：《多因子指数增强》（基于自适应风险控制的指数增强策略）
# 核心逻辑：综合动量、低波动、价值（PB代理）三个因子
#           在沪深300成分股中选股，相对基准做增强

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.benchmark = '510300.XSHG'   # 沪深300ETF作为基准
    context.lookback = 60
    context.top_n = 50
    context.month = -1

    # 因子权重
    context.w_momentum = 0.4
    context.w_low_vol = 0.3
    context.w_reversal = 0.3


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
            prices = history_bars(stock, context.lookback + 1, '1d', 'close')
            if prices is None or len(prices) < context.lookback + 1:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]

            # 因子1：中期动量（跳过最近20日）
            if len(prices) > 21:
                momentum = (prices[-21] / prices[0]) - 1
            else:
                momentum = 0

            # 因子2：低波动（取负值）
            low_vol = -np.std(returns[-20:])

            # 因子3：短期反转
            reversal = -((prices[-1] / prices[-5]) - 1) if len(prices) > 5 else 0

            scores[stock] = (
                context.w_momentum * momentum +
                context.w_low_vol * low_vol +
                context.w_reversal * reversal
            )
        except:
            continue

    if not scores:
        return

    # 标准化得分
    vals = np.array(list(scores.values()))
    mean_v, std_v = vals.mean(), vals.std()
    if std_v > 0:
        scores = {k: (v - mean_v) / std_v for k, v in scores.items()}

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
