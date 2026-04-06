# 欧奈尔RPS选股战法 - RiceQuant版本
# 逻辑：计算每只股票的RPS（相对价格强度，近12个月涨幅排名），选RPS>80的股票

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    # 从沪深300中计算RPS
    stocks = index_components('000300.XSHG')
    if not stocks:
        return

    context.month = current_month

    # 计算12个月涨幅
    returns_12m = {}
    for stock in stocks:
        try:
            closes = history_bars(stock, 252, '1d', 'close')
            if closes is None or len(closes) < 60:
                continue
            closes = np.array(closes, dtype=float)
            ret = closes[-1] / closes[0] - 1
            returns_12m[stock] = ret
        except Exception:
            continue

    if len(returns_12m) < 10:
        return

    # 计算RPS排名（百分位）
    all_returns = np.array(list(returns_12m.values()))
    rps_scores = {}
    for stock, ret in returns_12m.items():
        rps = np.sum(all_returns <= ret) / len(all_returns) * 100
        rps_scores[stock] = rps

    # 选RPS>80的股票
    high_rps = {s: rps_scores[s] for s in rps_scores if rps_scores[s] > 80}
    if not high_rps:
        return

    sorted_stocks = sorted(high_rps, key=high_rps.get, reverse=True)
    target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
