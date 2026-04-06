# 迪马克TD趋势反转指标策略 - RiceQuant版本
# 逻辑：TD序列，连续9根K线收盘价低于4根前时买入沪深300ETF

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.etf = '510300.XSHG'
    context.pos = False
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
def handle_bar(context, bar_dict):
    closes = history_bars(context.security, 20, '1d', 'close')
    if closes is None or len(closes) < 14:
        return
    closes = np.array(closes, dtype=float)

    buy_count = 0
    sell_count = 0
    for i in range(4, len(closes)):
        if closes[i] < closes[i - 4]:
            buy_count += 1
            sell_count = 0
        elif closes[i] > closes[i - 4]:
            sell_count += 1
            buy_count = 0
        else:
            buy_count = 0
            sell_count = 0

    bar = (bar_dict[context.etf] if context.etf in bar_dict else None)
    if bar is None or not bar.is_trading:
        return

    if buy_count >= 9 and not context.pos:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.pos = True
    elif sell_count >= 9 and context.pos:
        order_target_value(context.etf, 0)
        context.pos = False
