# 因子择时策略 - RiceQuant版本
# 来源：《因子择时研究》
# 核心逻辑：根据市场状态（牛市/熊市/震荡）动态切换因子
#           牛市用动量因子，熊市用低波动因子，震荡市用反转因子

import numpy as np


def detect_market_regime(index_prices, short_window=20, long_window=60):
    """
    判断市场状态
    - 牛市：短期均线 > 长期均线 且 趋势向上
    - 熊市：短期均线 < 长期均线 且 趋势向下
    - 震荡：其他
    """
    if len(index_prices) < long_window:
        return 'neutral'

    prices = np.array(index_prices, dtype=float)
    ma_short = np.mean(prices[-short_window:])
    ma_long = np.mean(prices[-long_window:])

    # 趋势强度
    trend = (prices[-1] / prices[-long_window]) - 1

    if ma_short > ma_long and trend > 0.05:
        return 'bull'
    elif ma_short < ma_long and trend < -0.05:
        return 'bear'
    else:
        return 'neutral'


def init(context):
    context.index = '000300.XSHG'
    context.market_index = '000300.XSHG'
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    # 判断市场状态
    market_prices = history_bars(context.market_index, 65, '1d', 'close')
    if market_prices is None:
        return
    regime = detect_market_regime(market_prices)

    stocks = index_components(context.index)
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, 65, '1d', 'close')
            if prices is None or len(prices) < 65 or prices[-1] == 0:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]

            if regime == 'bull':
                # 牛市：动量因子
                factor = (prices[-1] / prices[-60]) - 1
            elif regime == 'bear':
                # 熊市：低波动因子（取负值，低波动排前）
                factor = -np.std(returns[-60:])
            else:
                # 震荡：反转因子
                factor = -((prices[-1] / prices[-20]) - 1)

            scores[stock] = factor
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
    print(f"市场状态: {regime}, 持仓: {len(target)}只")
