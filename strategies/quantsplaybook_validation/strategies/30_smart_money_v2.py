# 聪明钱因子2.0选股策略 - RiceQuant版本
# 来源：《聪明钱因子模型的2.0版本》
# 核心逻辑：从日线量价数据近似识别"聪明钱"交易，
#           大成交量+价格上涨的交易日视为聪明钱买入，构建选股因子

import numpy as np


def calc_smart_money_factor(prices, volumes, window=20):
    """
    近似聪明钱因子：
    - 原版使用分钟数据，按成交量*|收益率|排序取前20%
    - 日线近似：用 volume * |return| 加权的方向性收益
    """
    if len(prices) < window + 1:
        return None

    returns = np.diff(prices[-window-1:]) / prices[-window-1:-1]
    vols = np.array(volumes[-window:], dtype=float)

    # 聪明度指标 S = volume * |return|
    s_scores = vols * np.abs(returns)

    # 取S最大的前20%交易日
    threshold = np.percentile(s_scores, 80)
    smart_mask = s_scores >= threshold

    if smart_mask.sum() == 0:
        return None

    # 聪明钱方向：加权平均收益
    smart_returns = returns[smart_mask]
    smart_volumes = vols[smart_mask]
    smart_factor = np.average(smart_returns, weights=smart_volumes)

    return smart_factor


def init(context):
    context.index = '000300.XSHG'   # 沪深300
    context.lookback = 20
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
            volumes = history_bars(stock, context.lookback + 1, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            factor = calc_smart_money_factor(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
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
