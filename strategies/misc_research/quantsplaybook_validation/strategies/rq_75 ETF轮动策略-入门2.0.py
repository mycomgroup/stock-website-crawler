# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/38120
# 标题：ETF轮动策略-入门2.0
# 作者：vzhb1998

# 导入函数库
import numpy as np
import numpy
import datetime
import math

def init(context):
    # 设定300作为基准
    # 用真实价格交易
    # 打开防未来函数
    # 将滑点设置为0.001
    # 设置交易成本万分之一
    # 过滤order中低于error级别的日志
    # # # log.set_level('order', 'error')  # DELETED: not available in RQ

    # 股票池
    context.stock_pool = [
        '159915.XSHE', # 易方达创业板ETF
        '510300.XSHG', # 华泰柏瑞沪深300ETF
        '510500.XSHG', # 南方中证500ETF
    ]

    # 北向净流入数据
    context.Northbound = []
    context.Northbound_val = 15
    context.north_money = 0

    # 动量轮动参数
    context.stock_num = 1  # 买入评分最高的前stock_num只股票
    context.momentum_day = 27  # 最新动量参考最近momentum_day的
    # rsrs择时参数
    context.ref_stock = '000300.XSHG'  # 用ref_stock做择时计算的基础数据
    context.N = 18  # 计算最新斜率slope，拟合度r2参考最近N(18)天
    context.M = 300  # 计算最新标准分zscore，rsrs_score参考最近M(600)天
    context.score_threshold = 0.7  # rsrs标准分指标阈值
    # ma择时参数
    context.mean_day = 20  # 计算结束ma收盘价，参考最近mean_day
    context.mean_diff_day = 5  # 计算初始ma收盘价，参考(mean_day + mean_diff_day)天前
    context.slope_series = []
    context.slope_initialized = False

    # 设置交易时间，每天运行
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))
    scheduler.run_daily(check_lose, time_rule=market_open(minute=0))
    scheduler.run_daily(print_trade_info, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    if not context.slope_initialized:
        context.slope_series = initial_slope_series(context)[:-1]
        context.slope_initialized = True

# 1-1 选股模块-动量因子轮动
def get_rank(context, stock_pool):
    score_list = []
    for stock in context.stock_pool:
        close_prices = history_bars(stock, context.momentum_day, '1d', 'close')
        if close_prices is None or len(close_prices) == 0:
            continue
        y = np.log(close_prices)
        x = np.arange(y.size)
        slope, intercept = np.polyfit(x, y, 1)
        annualized_returns = math.pow(math.exp(slope), 250) - 1
        r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
        score = annualized_returns * r_squared
        score_list.append(score)
    stock_dict = dict(zip(context.stock_pool, score_list))
    sort_list = sorted(stock_dict.items(), key=lambda item: item[1], reverse=True)
    code_list = []
    for i in range(len(context.stock_pool)):
        code_list.append(sort_list[i][0])
    rank_stock = code_list[0:context.stock_num]
    print(code_list[0:5])
    return rank_stock


# 2-1 择时模块-计算线性回归统计值
def get_ols(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    var_y = np.var(y, ddof=1)
    if var_y == 0 or len(y) <= 1:
        return (intercept, slope, 0)
    r2 = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * var_y))
    return (intercept, slope, r2)

# 2-2 择时模块-设定初始斜率序列
def initial_slope_series(context):
    highs = history_bars(context.ref_stock, context.N + context.M, '1d', 'high')
    lows = history_bars(context.ref_stock, context.N + context.M, '1d', 'low')
    if highs is None or lows is None:
        return []
    return [get_ols(lows[i:i+context.N], highs[i:i+context.N])[1] for i in range(context.M)]

# 2-3 择时模块-计算标准分
def get_zscore(slope_series):
    mean = np.mean(slope_series)
    std = np.std(slope_series)
    return (slope_series[-1] - mean) / std

# 2-4 择时模块-计算综合信号
def get_timing_signal(context, stock):
    # 计算MA信号
    close_data = history_bars(context.ref_stock, context.mean_day + context.mean_diff_day, '1d', 'close')
    today_MA = close_data[context.mean_diff_day:].mean()
    before_MA = close_data[:-context.mean_diff_day].mean()
    # 计算rsrs信号
    high_data = history_bars(context.ref_stock, context.N, '1d', 'high')
    low_data = history_bars(context.ref_stock, context.N, '1d', 'low')
    intercept, slope, r2 = get_ols(low_data, high_data)
    context.slope_series.append(slope)
    rsrs_score = get_zscore(context.slope_series[-context.M:]) * r2
    # 综合判断所有信号
    if rsrs_score > context.score_threshold and today_MA > before_MA:
        print('BUY')
        return "BUY"
    elif rsrs_score < -context.score_threshold and today_MA < before_MA:
        print('SELL')
        return "SELL"
    else:
        print('KEEP')
        return "KEEP"

# 3-1 过滤模块-过滤停牌股票
def filter_paused_stock(stock_list):
    result = []
    for stock in stock_list:
        bars = history_bars(stock, 1, '1d', 'close')
        if bars is not None and len(bars) > 0:
            result.append(stock)
    return result

# 3-2 过滤模块-过滤ST及其他具有退市标签的股票
def filter_st_stock(stock_list):
    result = []
    for stock in stock_list:
        inst = instruments(stock)
        name = inst.symbol
        special = getattr(inst, 'special_type', None)
        special_str = str(special) if special else ''
        if 'ST' not in special_str \
                and 'ST' not in name \
                and '*' not in name \
                and '退' not in name:
            result.append(stock)
    return result

# 3-3 过滤模块-过滤涨停的股票
def filter_limitup_stock(context, stock_list):
    result = []
    for stock in stock_list:
        if stock in context.portfolio.positions.keys():
            result.append(stock)
            continue
        closes = history_bars(stock, 1, '1d', 'close')
        _pre_stock = history_bars(stock, 1, '1d', 'close')
        limit_ups = _pre_stock * 1.1 if _pre_stock is not None else None
        if closes is not None and limit_ups is not None and len(closes) > 0 and len(limit_ups) > 0:
            last_price = closes[-1]
            limit_up = limit_ups[-1]
            if last_price < limit_up:
                result.append(stock)
    return result

# 3-4 过滤模块-过滤跌停的股票
def filter_limitdown_stock(context, stock_list):
    result = []
    for stock in stock_list:
        if stock in context.portfolio.positions.keys():
            result.append(stock)
            continue
        closes = history_bars(stock, 1, '1d', 'close')
        _pre_stock = history_bars(stock, 1, '1d', 'close')
        limit_downs = _pre_stock * 0.9 if _pre_stock is not None else None
        if closes is not None and limit_downs is not None and len(closes) > 0 and len(limit_downs) > 0:
            last_price = closes[-1]
            limit_down = limit_downs[-1]
            if last_price > limit_down:
                result.append(stock)
    return result

def getPreDayPrice(security):
    close_data = history_bars(security, 1, '1d', 'close')
    current_price = close_data[-1]
    return current_price

# 4-1 交易模块-择时交易
def my_trade(context, bar_dict):
    # 获取选股列表并过滤掉:st,st*,退市,涨停,跌停,停牌
    check_out_list = get_rank(context, context.stock_pool)
    check_out_list = filter_st_stock(check_out_list)
    check_out_list = filter_limitup_stock(context, check_out_list)
    check_out_list = filter_limitdown_stock(context, check_out_list)
    check_out_list = filter_paused_stock(check_out_list)
    print('今日自选股:{}'.format(check_out_list))
    # 获取综合择时信号
    timing_signal = get_timing_signal(context, context.ref_stock)
    print('今日择时信号:{}{}'.format(check_out_list, timing_signal))
    # 开始交易
    if timing_signal == 'SELL':
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
    elif timing_signal == 'BUY' or timing_signal == 'KEEP':
        # 根据股票数量分仓
        position_count = len(context.portfolio.positions)
        if context.stock_num > position_count:
            value = context.portfolio.cash / (context.stock_num - position_count)
            for stock in check_out_list:
                pos = context.portfolio.positions.get(stock)
                if pos is None or pos.quantity == 0:
                    order_target_value(stock, value)
                    if len(context.portfolio.positions) == context.stock_num:
                        break
    else:
        pass

# 4-2 交易模块-止损
def check_lose(context, bar_dict):
    for position in list(context.portfolio.positions.values()):
        securities = position.order_book_id
        cost = position.avg_price
        if cost <= 0:
            continue
        bar = (bar_dict[securities] if securities in bar_dict else None)
        price = bar.close if bar is not None else (position.market_value / position.quantity if position.quantity else cost)
        ret = 100 * (price / cost - 1)
        value = position.market_value
        amount = position.quantity
        if ret <= -50:
            order_target_value(position.order_book_id, 0)
            print("触发止损: 标的={},价值={},盈亏={}%".format(
                securities, format(value, '.2f'), format(ret, '.2f')))

# 5-1 复盘模块-打印
def print_trade_info(context, bar_dict):
    trades = {}
    for _trade in trades.values():
        print('成交记录：' + str(_trade))
    for position in list(context.portfolio.positions.values()):
        securities = position.order_book_id
        cost = position.avg_price
        if cost <= 0:
            continue
        bar = (bar_dict[securities] if securities in bar_dict else None)
        price = bar.close if bar is not None else (position.market_value / position.quantity if position.quantity else cost)
        ret = 100 * (price / cost - 1)
        value = position.market_value
        amount = position.quantity
        print('代码:{} 成本:{} 现价:{} 收益:{}% 持仓:{} 市值:{}'.format(
            securities, format(cost, '.2f'), price, format(ret, '.2f'), amount, format(value, '.2f')))
    print('一天结束')
