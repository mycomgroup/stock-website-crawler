# 纯真波动率因子（剔除跨期截面相关性）选股策略 - RiceQuant版本
# 来源：《剔除跨期截面相关性的纯真波动率因子》
# 核心逻辑：特质波动率（IVOL）= 个股收益率对市场收益率回归后的残差标准差
#           低特质波动率股票未来收益更高（低波动率异象）

import numpy as np


def calc_idiosyncratic_vol(stock_returns, market_returns, window=60):
    """
    计算特质波动率（IVOL）
    用OLS回归剔除市场因子后的残差标准差
    """
    if len(stock_returns) < window or len(market_returns) < window:
        return None

    y = np.array(stock_returns[-window:], dtype=float)
    x = np.array(market_returns[-window:], dtype=float)

    # OLS回归
    x_with_const = np.column_stack([np.ones(window), x])
    try:
        beta = np.linalg.lstsq(x_with_const, y, rcond=None)[0]
        residuals = y - x_with_const @ beta
        ivol = np.std(residuals)
        return ivol
    except Exception:
        return None


def init(context):
    context.index = '000300.XSHG'
    context.market = '000300.XSHG'
    context.window = 60
    context.top_n = 30
    context.month = -1
    context.market_returns = None


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    # 获取市场收益率
    market_prices = history_bars(context.market, context.window + 1, '1d', 'close')
    if market_prices is None:
        return
    market_prices = np.array(market_prices, dtype=float)
    market_returns = np.diff(market_prices) / market_prices[:-1]

    stocks = index_components(context.index)
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            if prices is None or len(prices) < context.window + 1 or prices[-1] == 0:
                continue
            prices = np.array(prices, dtype=float)
            stock_returns = np.diff(prices) / prices[:-1]

            ivol = calc_idiosyncratic_vol(stock_returns, market_returns, context.window)
            if ivol is not None:
                scores[stock] = ivol
        except Exception:
            continue

    if not scores:
        return

    # 选低特质波动率股票（低波动率异象）
    sorted_stocks = sorted(scores, key=scores.get, reverse=False)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
