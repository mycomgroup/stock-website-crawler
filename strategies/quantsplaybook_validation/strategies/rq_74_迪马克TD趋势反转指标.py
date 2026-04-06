# 迪马克TD趋势反转指标策略 - RiceQuant版本
# 逻辑：TD序列（连续9根K线收盘价高于/低于4根前的收盘价），选TD买入信号的股票

import numpy as np


def td_setup(closes):
    """计算TD Setup序列，返回买入/卖出计数"""
    n = len(closes)
    buy_count = 0
    sell_count = 0
    for i in range(4, n):
        if closes[i] < closes[i - 4]:
            buy_count += 1
            sell_count = 0
        elif closes[i] > closes[i - 4]:
            sell_count += 1
            buy_count = 0
        else:
            buy_count = 0
            sell_count = 0
    return buy_count, sell_count


def init(context):
    context.security = '000300.XSHG'
    context.etf = '510300.XSHG'
    context.pos = False


def handle_bar(context, bar_dict):
    closes = history_bars(context.security, 20, '1d', 'close')
    if closes is None or len(closes) < 14:
        return

    closes = np.array(closes, dtype=float)
    buy_count, sell_count = td_setup(closes)

    bar = (bar_dict[context.etf] if context.etf in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    # TD买入信号：连续9根收盘价低于4根前（超卖）
    if buy_count >= 9 and not context.pos:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.pos = True
    # TD卖出信号：连续9根收盘价高于4根前（超买）
    elif sell_count >= 9 and context.pos:
        order_target_value(context.etf, 0)
        context.pos = False
