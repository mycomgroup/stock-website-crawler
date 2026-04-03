# 企业生命周期选股策略 - RiceQuant版本
# 来源：《企业生命周期》
# 核心逻辑：根据现金流特征将企业分为成长期、成熟期、衰退期
#           成长期（经营CF+、投资CF-、融资CF+）和成熟期（经营CF+、投资CF-、融资CF-）
#           的企业具有更好的投资价值
# 注：RiceQuant可获取财务数据，用近似指标实现

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.lookback = 60
    context.top_n = 30
    context.quarter = -1


def handle_bar(context, bar_dict):
    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        return
    context.quarter = current_quarter

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
            returns = np.diff(prices) / prices[:-1]

            # 代理变量：用价格趋势+成交量趋势近似企业生命周期阶段
            # 成长期特征：价格上涨 + 成交量放大
            price_trend = np.polyfit(np.arange(context.lookback), prices[-context.lookback:], 1)[0]
            vol_trend = np.polyfit(np.arange(context.lookback), volumes, 1)[0]

            # 盈利质量代理：收益率稳定性（成熟期企业收益稳定）
            ret_stability = -np.std(returns)

            # 综合得分：趋势向上 + 成交量放大 + 收益稳定
            price_score = 1 if price_trend > 0 else -1
            vol_score = 1 if vol_trend > 0 else -1

            scores[stock] = price_score * 0.4 + vol_score * 0.3 + ret_stability * 0.3
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
