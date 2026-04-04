# APM因子模型选股策略 - RiceQuant版本
# 来源：《APM因子模型》
# 核心逻辑：APM（Abnormal Price Movement）= 个股收益率 - 预期收益率
#           预期收益率用市场因子+行业因子估计
#           APM高的股票有异常正向价格运动，未来可能延续

import numpy as np


def calc_apm_factor(stock_returns, market_returns, window=20):
    """
    计算APM因子
    APM = 实际收益率 - 预期收益率（市场模型）
    """
    if len(stock_returns) < window or len(market_returns) < window:
        return None

    y = np.array(stock_returns[-window:], dtype=float)
    x = np.array(market_returns[-window:], dtype=float)

    # 用前半段估计beta
    half = window // 2
    if half < 5:
        return None

    x_train = x[:half]
    y_train = y[:half]

    x_with_const = np.column_stack([np.ones(half), x_train])
    try:
        beta = np.linalg.lstsq(x_with_const, y_train, rcond=None)[0]
    except Exception:
        return None

    # 用后半段计算APM
    x_test = x[half:]
    y_test = y[half:]
    x_test_const = np.column_stack([np.ones(len(x_test)), x_test])
    expected = x_test_const @ beta
    apm = np.mean(y_test - expected)

    return apm


def init(context):
    context.index = '000300.XSHG'
    context.market = '000300.XSHG'
    context.window = 40
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

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

            apm = calc_apm_factor(stock_returns, market_returns, context.window)
            if apm is not None:
                scores[stock] = apm
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
