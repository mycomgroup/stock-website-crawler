# 凸显理论STR因子选股策略 - RiceQuant版本
# 来源：《凸显理论STR因子》
# 核心逻辑：基于凸显理论，投资者对极端收益（最高/最低）赋予过高权重
#           STR因子 = 过去一段时间内的最大单日涨幅（凸显性收益）
#           STR高的股票被高估，未来收益低（反转）；STR低的股票被低估

import numpy as np


def calc_str_factor(returns, window=52):
    """
    凸显性收益因子（STR）
    = 过去window周内的最大单周收益率
    日线版本：过去window日内的最大单日涨幅
    """
    if len(returns) < window:
        return None

    r = np.array(returns[-window:], dtype=float)
    # 最大单日涨幅（凸显性正收益）
    str_factor = np.max(r)
    return str_factor


def init(context):
    context.index = '000300.XSHG'
    context.window = 52      # 约一年的周数，日线用52天
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
            prices = history_bars(stock, context.window + 1, '1d', 'close')
            if prices is None or len(prices) < context.window + 1 or prices[-1] == 0:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]

            str_factor = calc_str_factor(returns, context.window)
            if str_factor is not None:
                scores[stock] = str_factor
        except Exception:
            continue

    if not scores:
        return

    # STR低的股票（凸显性低，被低估）→ 做多
    sorted_stocks = sorted(scores, key=scores.get, reverse=False)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
