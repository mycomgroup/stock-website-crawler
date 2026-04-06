# 小资金短线策略 - RiceQuant版本
# 原文：小资金短线策略
# 逻辑：选中证500成分股中，近期强势（突破布林带上轨）的股票，短线持有

import numpy as np


def init(context):
    context.max_hold_stocknum = 3
    context.candidates = []
    scheduler.run_daily(select_candidates, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))


def handle_bar(context, bar_dict):
    pass


# before_trading_start removed (not supported in RQ)


def select_candidates(context, bar_dict):
    try:
        universe = index_components('000905.XSHG')
    except Exception:
        universe = []
    if not universe:
        return

    candidates = []
    for stock in universe:
        try:
            closes = history_bars(stock, 25, '1d', 'close')
            if closes is None or len(closes) < 25:
                continue
            closes = np.array(closes, dtype=float)
            ma = np.mean(closes[-20:])
            std = np.std(closes[-20:])
            upper = ma + 2 * std
            if closes[-1] > upper:
                candidates.append(stock)
        except Exception:
            continue
    context.candidates = candidates[:context.max_hold_stocknum * 3]

def trade(context, bar_dict):
    # 止损：持仓跌幅超过5%
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        if bar.close / pos.avg_cost - 1 < -0.05:
            order_target_value(stock, 0)

    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.max_hold_stocknum:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
