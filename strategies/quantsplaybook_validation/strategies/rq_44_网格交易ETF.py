# 网格交易ETF策略 - RiceQuant版本
# 原文：最易上手的网格策略v2.0
# 作者：xfera16
# 原文：https://www.joinquant.com/post/36074
# 逻辑：对中证500ETF进行网格交易，每格5%，每格投入2万

import numpy as np


ETF = '510500.XSHG'   # 中证500ETF
NET_RANGE = 0.05      # 网格大小5%
PER_SHARE = 20000     # 每格金额
LOOKBACK = 60         # 基准价参考天数


def init(context):
    context.etf = ETF
    context.net_range = NET_RANGE
    context.per_share = PER_SHARE
    context.base_price = None
    context.net_level = 0  # 当前网格层数


def handle_bar(context, bar_dict):
    bar = (bar_dict[context.etf] if context.etf in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    current_price = bar.close

    # 首次建仓：在历史均值附近
    if context.base_price is None:
        prices = history_bars(context.etf, LOOKBACK, '1d', 'close')
        if prices is None or len(prices) < LOOKBACK:
            return
        ma = np.mean(np.array(prices, dtype=float))
        # 当前价格在均值±20%范围内才建仓
        if abs(current_price / ma - 1) < 0.2:
            context.base_price = current_price
            shares = int(context.per_share / current_price / 100) * 100
            if shares > 0 and context.portfolio.cash >= shares * current_price:
                order_shares(context.etf, shares)
        return

    # 计算当前网格层数
    price_change = (current_price - context.base_price) / context.base_price
    target_level = int(price_change / context.net_range)

    if target_level < context.net_level:
        # 价格下跌，买入一格
        shares = int(context.per_share / current_price / 100) * 100
        if shares > 0 and context.portfolio.cash >= shares * current_price:
            order_shares(context.etf, shares)
            context.net_level = target_level

    elif target_level > context.net_level:
        # 价格上涨，卖出一格
        pos = context.portfolio.positions.get(context.etf)
        if pos and pos.quantity > 0:
            shares = int(context.per_share / current_price / 100) * 100
            sell_shares = min(shares, pos.quantity)
            if sell_shares > 0:
                order_shares(context.etf, -sell_shares)
                context.net_level = target_level
