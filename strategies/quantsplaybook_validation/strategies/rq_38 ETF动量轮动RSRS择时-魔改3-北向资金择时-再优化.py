# RiceQuant策略迁移
# 原文标题：ETF动量轮动RSRS择时-魔改3-北向资金择时-再优化
# 原文作者：秋天来了
# 原文网址：https://www.joinquant.com/post/35376

import numpy as np

# 初始化函数
def init(context):
    context.stock_pool = [
        '510050.XSHG',  # 上证50ETF
        '159928.XSHE',  # 中证消费ETF
        '510300.XSHG',  # 沪深300ETF
        '159949.XSHE',  # 创业板50ETF
    ]
    context.north_money = 0
    context.stock_num = 1
    context.momentum_day = 20
    context.momentum_day_t = 0
    context.ref_stock = '000300.XSHG'
    context.N = 18
    context.M = 300
    context.score_threshold = 0.7
    context.mean_day = 30
    context.mean_diff_day = 2
    context.slope_series = []  # 延迟到 handle_bar 第一次运行时初始化
    context.slope_initialized = False
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))
    scheduler.run_daily(check_lose, time_rule=market_open(minute=0))
    scheduler.run_daily(print_trade_info, time_rule=market_close(minute=30))

# 20日收益率动量拟合取斜率最大的

def handle_bar(context, bar_dict):
    if not context.slope_initialized:
        context.slope_series = initial_slope_series(context)[:-1]
        context.slope_initialized = True

def get_rank(context, stock_pool):
    rank = []
    for stock in context.stock_pool:
        data = history_bars(stock, context.momentum_day, '1d', 'close')
        if data is None or len(data) == 0:
            continue
        score = np.polyfit(np.arange(len(data)), data / data[0], 1)[0]
        rank.append([stock, score])
    rank.sort(key=lambda x: x[-1], reverse=True)
    return rank[0] if rank else [context.stock_pool[0], 0]

# 这里求R2的式子有点问题，但是这个效果更好，原因未找到！
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

# 因子标准化
def get_zscore(slope_series):
    mean = np.mean(slope_series)
    std = np.std(slope_series)
    return (slope_series[-1] - mean) / std

# 只看RSRS因子值作为买入、持有和清仓依据
def get_timing_signal(context, stock):
    context.mean_diff_day = 5
    close_data = history_bars(context.ref_stock, context.mean_day + context.mean_diff_day, '1d', 'close')
    highs = history_bars(context.ref_stock, context.N, '1d', 'high')
    lows = history_bars(context.ref_stock, context.N, '1d', 'low')
    if highs is None or lows is None:
        return "KEEP"

    intercept, slope, r2 = get_ols(lows, highs)
    context.slope_series.append(slope)
    rsrs_score = get_zscore(context.slope_series[-context.M:]) * r2

    if context.north_money < 0:
        return "SELL"

    if context.momentum_day_t > 0:
        data = history_bars(context.ref_stock, context.momentum_day_t, '1d', 'close')
        s_t = np.polyfit(np.arange(len(data)), data / data[0], 1)[0]

        if s_t < 0:
            return "SELL"
        else:
            context.momentum_day_t = 0
            if rsrs_score > context.score_threshold:
                return "BUY"
            elif rsrs_score < -context.score_threshold:
                return "SELL"
            else:
                return "KEEP"
    else:
        if rsrs_score > context.score_threshold:
            return "BUY"
        elif rsrs_score < -context.score_threshold:
            return "SELL"
        else:
            return "KEEP"

# 交易模块-自定义下单
def order_target_value_(security, value):
    if value == 0:
        print("Selling out %s" % (security))
    else:
        print("Order %s to value %f" % (security, value))
    return order_target_value(security, value)

# 交易模块-开仓
def open_position(security, value):
    order = order_target_value_(security, value)
    return order is not None

# 交易模块-平仓
def close_position(position):
    security = position.order_book_id
    order = order_target_value_(security, 0)
    if order is not None:
        return True
    return False

def adjust_position(context, buy_stocks):
    for stock in list(context.portfolio.positions.keys()):
        if stock not in buy_stocks:
            print("[%s]已不在应买入列表中" % (stock))
            position = context.portfolio.positions.get(stock)
            if position is None: continue
            close_position(position)
        else:
            print("[%s]已经持有无需重复买入" % (stock))
    position_count = len(context.portfolio.positions)
    if context.stock_num > position_count:
        value = context.portfolio.cash / (context.stock_num - position_count)
        for stock in buy_stocks:
            pos = context.portfolio.positions.get(stock)
            if pos is None or pos.quantity == 0:
                if open_position(stock, value):
                    if len(context.portfolio.positions) == context.stock_num:
                        break

# 交易主函数
def my_trade(context, bar_dict):
    get_north_money(context)
    check_out_list = get_rank(context, context.stock_pool)
    timing_signal = get_timing_signal(context, context.ref_stock)
    print('今日自选及择时信号:{} {}'.format(check_out_list, timing_signal))
    if timing_signal == 'SELL':
        for stock in list(context.portfolio.positions.keys()):
            position = context.portfolio.positions.get(stock)
            if position is None: continue
            close_position(position)
    elif timing_signal == 'BUY' or timing_signal == 'KEEP':
        adjust_position(context, check_out_list)

def get_north_money(context):
    # 北向资金数据在RQ中不可用，默认设为0（不影响策略运行）
    context.north_money = 0

# 这个函数几乎没用
def check_lose(context, bar_dict):
    for position in list(context.portfolio.positions.values()):
        securities = position.order_book_id
        cost = position.avg_price
        price = position.avg_price
        ret = 100 * (price / cost - 1)
        value = position.market_value
        amount = position.quantity
        if ret <= -4:
            order_target_value(position.order_book_id, 0)
            print("！！！！！！触发止损信号: 标的={},标的价值={},浮动盈亏={}% ！！！！！！"
                .format(securities, format(value, '.2f'), format(ret, '.2f')))
            context.momentum_day_t = 5

def print_trade_info(context, bar_dict):
    # 打印当天成交记录
    trades = {}
    for _trade in trades.values():
        print('成交记录：' + str(_trade))
    print('———————————————————————————————————————分割线————————————————————————————————————————')
