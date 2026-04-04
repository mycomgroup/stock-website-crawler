# A股动量因子构建策略 - RiceQuant版本
# 来源：《A股市场中如何构造动量因子？》
# 核心逻辑：A股反转强于动量，使用短期反转（20日）而非长期动量
#           同时控制市值暴露，在中证500中选股

import numpy as np


def init(context):
    context.index = '000905.XSHG'   # 中证500
    context.reversal_window = 20     # 短期反转窗口
    context.vol_window = 60          # 波动率窗口
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    stocks = index_components(context.index)
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.vol_window + 1, '1d', 'close')
            if prices is None or len(prices) < context.vol_window + 1 or prices[-1] == 0:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]

            # 短期反转因子（取负值，反转效应）
            r20 = (prices[-1] / prices[-context.reversal_window-1]) - 1
            reversal_factor = -r20  # 反转：过去跌的选

            # 风险调整
            sigma = np.std(returns[-context.vol_window:])
            if sigma == 0:
                continue

            # 风险调整后的反转因子
            adj_factor = reversal_factor / sigma

            scores[stock] = adj_factor
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
