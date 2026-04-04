# 高频价量相关性（CPV）因子选股策略 - RiceQuant版本
# 来源：《高频价量相关性，意想不到的选股因子》
# 核心逻辑：CPV = 价格变化与成交量变化的相关系数
#           CPV为负（量价背离）时，股票被高估，未来收益低；
#           CPV为正（量价共振）时，趋势确认，未来收益高

import numpy as np


def calc_cpv(prices, volumes, window=20):
    """
    计算价量相关性因子 CPV
    """
    if len(prices) < window + 1 or len(volumes) < window:
        return None

    price_changes = np.diff(np.array(prices[-window-1:], dtype=float))
    vol_changes = np.diff(np.array(volumes[-window:], dtype=float))

    if len(price_changes) < 2 or len(vol_changes) < 2:
        return None

    # 计算相关系数
    if np.std(price_changes) == 0 or np.std(vol_changes) == 0:
        return None

    corr = np.corrcoef(price_changes, vol_changes)[0, 1]
    return corr


def init(context):
    context.index = '000300.XSHG'
    context.window = 20
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
            prices = history_bars(stock, context.window + 2, '1d', 'close')
            volumes = history_bars(stock, context.window + 1, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            cpv = calc_cpv(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
                context.window
            )
            if cpv is not None:
                scores[stock] = cpv
        except Exception:
            continue

    if not scores:
        return

    # 选CPV最高的股票（量价共振）
    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
