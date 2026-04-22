# RiceQuant策略迁移
# 原文标题：ETF动量轮动MA乖离择时
# 原文网址：https://www.joinquant.com/post/35005
# 作者：莫急莫急
# 注：原策略使用talib.MA，此处用numpy手动实现

import numpy as np

def init(context):

    context.stock_pool = [
        '510050.XSHG',
        '159928.XSHE',
        '510300.XSHG',
        '159949.XSHE',
    ]
    context.stock_num = 1
    context.momentum_day = 20
    context.ref_stock = '000300.XSHG'

    scheduler.run_daily(my_trade, time_rule=market_close(minute=10))
    scheduler.run_daily(check_lose, time_rule=market_open(minute=0))


def handle_bar(context, bar_dict):
    pass


def ma(data, period):
    """简单移动平均"""
    result = np.full(len(data), np.nan)
    for i in range(period - 1, len(data)):
        result[i] = np.mean(data[i - period + 1:i + 1])
    return result


def get_rank(context):
    rank = []
    for stock in context.stock_pool:
        data = history_bars(stock, context.momentum_day, '1d', 'close')
        if data is None or len(data) == 0:
            continue
        scores = np.polyfit(np.arange(len(data)), data / data[0], 1)[0]
        rank.append([stock, scores])
    rank.sort(key=lambda x: x[-1], reverse=True)
    return rank[0] if rank else None


def get_zscore(series):
    mean = np.mean(series)
    std = np.std(series)
    return (series[-1] - mean) / std if std > 0 else 0


def get_timing_signal(context):
    score_threshold = 4.0
    data = history_bars(context.ref_stock, 200, '1d', 'close')
    if data is None or len(data) < 60:
        return 'KEEP'

    ma60 = ma(data, 60)
    bias = data / ma60
    # 过滤nan
    valid_bias = bias[~np.isnan(bias)]
    if len(valid_bias) < 10:
        return 'KEEP'

    bias_ma10 = ma(valid_bias, 10)
    valid_bias_ma = bias_ma10[~np.isnan(bias_ma10)]
    if len(valid_bias_ma) < 30:
        return 'KEEP'

    score = get_zscore(valid_bias_ma[-30:])
    if score > score_threshold:
        return 'BUY'
    if score < -score_threshold:
        return 'SELL'
    return 'KEEP'


def close_position(position):
    order_target_value(position.order_book_id, 0)


def adjust_position(context, buy_stocks):
    for stock in list(context.portfolio.positions.keys()):
        if stock not in buy_stocks:
            print('换仓!')
            pos = context.portfolio.positions.get(stock)
            if pos: close_position(pos)

    position_count = len(context.portfolio.positions)
    if context.stock_num > position_count:
        value = context.portfolio.cash / (context.stock_num - position_count)
        for stock in buy_stocks:
            pos = context.portfolio.positions.get(stock)
            if pos is None or pos.quantity == 0:
                order_target_value(stock, value)


def my_trade(context, bar_dict):
    check_out_list = get_rank(context)
    if check_out_list is None:
        return

    timing_signal = get_timing_signal(context)
    print('今日自选及择时信号: %s %s' % (check_out_list, timing_signal))

    if timing_signal == 'SELL':
        for stock in list(context.portfolio.positions.keys()):
            pos = context.portfolio.positions.get(stock)
            if pos: close_position(pos)
    elif timing_signal in ['BUY', 'KEEP']:
        adjust_position(context, [check_out_list[0]])


def check_lose(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        position = context.portfolio.positions.get(stock)
        if position is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        if position.avg_price > 0 and bar.close / position.avg_price < 0.9:
            print('触发止损!')
            order_target_value(stock, 0)
