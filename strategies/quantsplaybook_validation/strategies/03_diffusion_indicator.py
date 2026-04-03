# 扩散指标择时策略 - RiceQuant版本
# 来源：《东北证券-扩散指标择时研究之一》

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.N = 100  # 股票池数量
    context.lookback = 20  # 回看周期
    context.buy_threshold = 0.6
    context.sell_threshold = 0.4
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security

    # 获取沪深300成分股
    try:
        stocks = index_components(security)
    except:
        stocks = all_instruments('CS')['order_book_id'][:context.N].tolist()

    if len(stocks) < 50:
        return

    # 计算扩散指标：上涨股票占比
    up_count = 0
    valid_count = 0

    for stock in stocks[:context.N]:
        try:
            prices = history_bars(stock, 2, '1d', 'close')
            if prices is not None and len(prices) == 2:
                if prices[-1] > prices[-2]:
                    up_count += 1
                valid_count += 1
        except:
            continue

    if valid_count == 0:
        return

    diffusion = up_count / valid_count

    # 交易逻辑
    if diffusion > context.buy_threshold and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: 扩散指标={diffusion:.2%}")
    elif diffusion < context.sell_threshold and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: 扩散指标={diffusion:.2%}")