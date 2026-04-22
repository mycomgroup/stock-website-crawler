# RiceQuant策略迁移
# 原文标题：ETF动量轮动RSRS择时-魔改4-低通滤波
# 原文作者：莫急莫急
# 原文网址：https://www.joinquant.com/post/35338

import numpy as np

def init(context):
    context.stock_pool = [
        '510050.XSHG',  # 上证50ETF
        '159928.XSHE',  # 中证消费ETF
        '510300.XSHG',  # 沪深300ETF
        '159949.XSHE',  # 创业板500
    ]
    context.stock_num = 1
    context.momentum_day = 20
    context.ref_stock = '000300.XSHG'
    context.N = 18
    context.M = 300
    context.score_threshold = 0.7
    context.slope_series = []  # 延迟到 handle_bar 第一次运行时初始化
    context.slope_initialized = False
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))
    scheduler.run_daily(check_lose, time_rule=market_open(minute=0))
    scheduler.run_daily(print_trade_info, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    if not context.slope_initialized:
        context.slope_series = initial_slope_series(context)[:-1]
        context.slope_initialized = True


def fftFilter(fs, N, dr):
    y = np.fft.fft(dr)
    for i in range(len(y)):
        if (i > fs) and (i < N - fs):
            y[i] = 0.0
    return np.fft.ifft(y)


def get_rank(context, stock_pool):
    rank = []
    fs, N = 60, 250
    for stock in context.stock_pool:
        data = history_bars(stock, N, '1d', 'close')
        if data is None or len(data) < N:
            continue
        dr = np.log(data / data[0])
        newdr = fftFilter(fs, N, dr)
        score = np.polyfit(np.arange(context.momentum_day), newdr[-context.momentum_day:], 1)[0].real
        rank.append([stock, score])
    rank.sort(key=lambda x: x[-1], reverse=True)
    return rank[0] if rank else [context.stock_pool[0], 0]


def get_ols(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    var_y = np.var(y, ddof=1)
    if var_y == 0 or len(y) <= 1:
        return (intercept, slope, 0)
    r2 = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * var_y))
    return (intercept, slope, r2)


def initial_slope_series(context):
    highs = history_bars(context.ref_stock, context.N + context.M, '1d', 'high')
    lows = history_bars(context.ref_stock, context.N + context.M, '1d', 'low')
    if highs is None or lows is None:
        return []
    return [get_ols(lows[i:i + context.N], highs[i:i + context.N])[1] for i in range(context.M)]


def get_zscore(slope_series):
    mean = np.mean(slope_series)
    std = np.std(slope_series)
    return (slope_series[-1] - mean) / std


def get_timing_signal(context, stock):
    highs = history_bars(context.ref_stock, 18, '1d', 'high')
    lows = history_bars(context.ref_stock, 18, '1d', 'low')
    if highs is None or lows is None:
        return "KEEP"
    intercept, slope, r2 = get_ols(lows, highs)
    context.slope_series.append(slope)
    rsrs_score = get_zscore(context.slope_series[-context.M:]) * r2
    print('rsrs_score {:.3f}'.format(rsrs_score))
    if rsrs_score > context.score_threshold:
        return "BUY"
    elif rsrs_score < -context.score_threshold:
        return "SELL"
    else:
        return "KEEP"


def order_target_value_(security, value):
    return order_target_value(security, value)


def open_position(security, value):
    order = order_target_value_(security, value)
    return order is not None


def close_position(position):
    security = position.order_book_id
    order_target_value_(security, 0)
    return True


def adjust_position(context, buy_stocks):
    for stock in list(context.portfolio.positions.keys()):
        if stock not in buy_stocks:
            print("[%s]已不在应买入列表中" % stock)
            pos = context.portfolio.positions.get(stock)
            if pos: close_position(pos)
        else:
            print("[%s]已经持有无需重复买入" % stock)
    position_count = len(context.portfolio.positions)
    if context.stock_num > position_count:
        value = context.portfolio.cash / (context.stock_num - position_count)
        for stock in buy_stocks:
            pos = context.portfolio.positions.get(stock)
            if pos is None or pos.quantity == 0:
                if open_position(stock, value):
                    if len(context.portfolio.positions) == context.stock_num:
                        break


def my_trade(context, bar_dict):
    check_out_list = get_rank(context, context.stock_pool)
    timing_signal = get_timing_signal(context, context.ref_stock)
    print('今日自选及择时信号:{} {}'.format(check_out_list, timing_signal))
    if timing_signal == 'SELL':
        for stock in list(context.portfolio.positions.keys()):
            pos = context.portfolio.positions.get(stock)
            if pos: close_position(pos)
    elif timing_signal == 'BUY' or timing_signal == 'KEEP':
        adjust_position(context, check_out_list)


def check_lose(context, bar_dict):
    for position in list(context.portfolio.positions.values()):
        securities = position.order_book_id
        cost = position.avg_price
        price = position.avg_price
        ret = 100 * (price / cost - 1)
        value = position.market_value
        if ret <= -90:
            order_target_value(position.order_book_id, 0)
            print("触发止损: 标的={},价值={},盈亏={}%".format(
                securities, format(value, '.2f'), format(ret, '.2f')))


def print_trade_info(context, bar_dict):
    trades = {}
    for _trade in trades.values():
        print('成交记录：' + str(_trade))
    print('---分割线---')
