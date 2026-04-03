# 股票网络中心度因子选股策略 - RiceQuant版本
# 来源：《股票网络与网络中心度因子研究》
# 核心逻辑：构建股票收益率相关性网络，计算每只股票的度中心度
#           网络中心度高的股票（与其他股票相关性强）往往是市场领涨/领跌股

import numpy as np


def calc_network_centrality(returns_matrix, threshold=0.3):
    """
    计算股票网络度中心度
    returns_matrix: shape (n_stocks, n_days)
    threshold: 相关系数阈值，超过则建立连接
    """
    n = returns_matrix.shape[0]
    if n < 2:
        return np.zeros(n)

    # 计算相关系数矩阵
    corr_matrix = np.corrcoef(returns_matrix)

    # 构建邻接矩阵（相关系数绝对值超过阈值）
    adj = (np.abs(corr_matrix) > threshold).astype(float)
    np.fill_diagonal(adj, 0)

    # 度中心度 = 连接数 / (n-1)
    degree = adj.sum(axis=1) / (n - 1)
    return degree


def init(context):
    context.index = '000300.XSHG'
    context.lookback = 60
    context.sample_n = 80      # 取样本股票数（避免计算量过大）
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    stocks = index_components(context.index)
    stocks = [s for s in stocks if s in bar_dict]

    # 取样本
    if len(stocks) > context.sample_n:
        stocks = stocks[:context.sample_n]

    # 收集收益率矩阵
    returns_list = []
    valid_stocks = []
    for stock in stocks:
        try:
            prices = history_bars(stock, context.lookback + 1, '1d', 'close')
            if prices is None or len(prices) < context.lookback + 1:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]
            returns_list.append(returns)
            valid_stocks.append(stock)
        except:
            continue

    if len(valid_stocks) < 10:
        return

    returns_matrix = np.array(returns_list)
    centrality = calc_network_centrality(returns_matrix)

    scores = dict(zip(valid_stocks, centrality))

    # 选中心度高的股票（市场核心股）
    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
