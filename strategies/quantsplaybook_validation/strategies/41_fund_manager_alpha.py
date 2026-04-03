# 来自优秀基金经理的超额收益选股策略 - RiceQuant版本
# 来源：《来自优秀基金经理的超额收益》
# 核心逻辑：跟踪优秀基金经理的重仓股，选择被多位优秀基金经理共同持有的股票
#           代理实现：用近期大资金净流入（机构行为代理）选股

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.lookback = 60
    context.top_n = 20
    context.quarter = -1


def handle_bar(context, bar_dict):
    # 季度调仓
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
            highs = history_bars(stock, context.lookback, '1d', 'high')
            lows = history_bars(stock, context.lookback, '1d', 'low')
            if any(x is None for x in [prices, volumes, highs, lows]):
                continue

            prices = np.array(prices, dtype=float)
            volumes = np.array(volumes, dtype=float)
            highs = np.array(highs, dtype=float)
            lows = np.array(lows, dtype=float)
            closes = prices[-context.lookback:]

            # 代理变量1：价格动量（优秀基金经理倾向持有上涨股）
            momentum = (prices[-1] / prices[-context.lookback]) - 1

            # 代理变量2：成交量趋势（机构建仓时成交量放大）
            recent_vol = volumes[-20:].mean()
            early_vol = volumes[:20].mean()
            vol_trend = recent_vol / (early_vol + 1e-10) - 1

            # 代理变量3：价格稳定性（机构持仓股波动相对小）
            returns = np.diff(prices[-context.lookback:]) / prices[-context.lookback:-1]
            stability = -np.std(returns)

            scores[stock] = momentum * 0.5 + vol_trend * 0.3 + stability * 0.2
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
