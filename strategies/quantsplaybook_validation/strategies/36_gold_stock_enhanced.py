# 金股增强策略 - RiceQuant版本
# 来源：《金股增强策略》
# 核心逻辑：基于券商金股推荐数据，对被多家券商推荐的股票进行增强选股
#           由于无法获取实时金股数据，用分析师覆盖度+近期涨幅作为代理变量

import numpy as np


def init(context):
    context.index = '000300.XSHG'   # 沪深300
    context.lookback = 20
    context.top_n = 20
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
            prices = history_bars(stock, context.lookback + 1, '1d', 'close')
            volumes = history_bars(stock, context.lookback, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            prices = np.array(prices, dtype=float)
            volumes = np.array(volumes, dtype=float)

            # 代理变量1：近期动量（金股通常是近期表现好的股票）
            momentum = (prices[-1] / prices[0]) - 1

            # 代理变量2：成交量放大（机构关注度提升）
            vol_ratio = volumes[-5:].mean() / (volumes.mean() + 1e-10)

            # 综合得分
            scores[stock] = momentum * 0.6 + (vol_ratio - 1) * 0.4
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
