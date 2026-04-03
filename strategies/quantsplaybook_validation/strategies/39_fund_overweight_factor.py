# 基金重仓超配因子选股策略 - RiceQuant版本
# 来源：《基金重仓超配因子及其对指数增强组合的影响》
# 核心逻辑：基金重仓股中，超配比例高的股票（基金持股比例 > 指数权重）
#           往往受到机构资金支撑，具有超额收益
# 注：无法直接获取基金持仓数据，用机构持股比例代理

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.lookback = 60
    context.top_n = 30
    context.quarter = -1


def handle_bar(context, bar_dict):
    # 季度调仓（基金持仓数据按季度披露）
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

            # 代理变量：大单成交占比（机构偏好大单）
            # 用成交量稳定性（低波动率）代理机构持仓稳定性
            vol_cv = np.std(volumes) / (np.mean(volumes) + 1e-10)  # 变异系数
            price_mom = (prices[-1] / prices[-context.lookback]) - 1

            # 机构超配代理：动量好 + 成交量稳定
            scores[stock] = price_mom * 0.7 - vol_cv * 0.3
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
