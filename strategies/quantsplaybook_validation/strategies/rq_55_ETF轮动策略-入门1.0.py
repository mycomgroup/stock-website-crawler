# RiceQuant策略 - ETF轮动策略-入门1.0
# 原文：https://www.joinquant.com/post/35136
# 作者：vzhb
# 克隆自JoinQuant策略

import numpy as np

def init(context):
    # 设定沪深300作为基准
    # 用真实价格交易
    # 打开防未来函数
    # 将滑点设置为0.001
    # 设置交易成本万分之一
    # 过滤order中低于error级别的日志
    # # logger.set_level('order', 'error')
    # 初始化各类全局变量
    # 股票池
    context.stock_pool = [
        '159915.XSHE', # 易方达创业板ETF
        '510300.XSHG', # 华泰柏瑞沪深300ETF
        '510500.XSHG', # 南方中证500ETF
    ]
    # 动量轮动参数
    context.stock_num = 1 # 买入评分最高的前stock_num只股票
    context.momentum_day = 29 # 最新动量参考最近momentum_day的
    # rsrs择时参数
    context.ref_stock = '000300.XSHG' # 用ref_stock做择时计算的基础数据
    context.N = 18 # 计算最新斜率slope，拟合度r2参考最近N天
    context.M = 300 # 计算最新标准分zscore，rsrs_score参考最近M天
    context.score_threshold = 0.7 # rsrs标准分指标阈值
    # ma择时参数
    context.mean_day = 20 # 计算结束ma收盘价，参考最近mean_day
    context.mean_diff_day = 3 # 计算初始ma收盘价，参考(mean_day + mean_diff_day)天前
    context.slope_series = []
    context.slope_initialized = False
    # 设置交易时间，每天运行
    scheduler.run_daily(my_trade, time_rule=market_open(minute=0))
    scheduler.run_daily(check_lose, time_rule=market_open(minute=0))
    scheduler.run_daily(print_trade_info, time_rule=market_open(minute=0))



def handle_bar(context, bar_dict):
    pass

def initial_slope_series(context):
    """初始化斜率序列 - 用当前时间往前拉足够数据"""
    total = context.N + context.M
    highs = history_bars(context.ref_stock, total, '1d', 'high')
    lows = history_bars(context.ref_stock, total, '1d', 'low')
    if highs is None or lows is None or len(highs) < total:
        return []
    slope_list = []
    for i in range(context.M):
        _lows = lows[i: i + context.N]
        _highs = highs[i: i + context.N]
        slope, _ = np.polyfit(_lows, _highs, 1)
        slope_list.append(slope)
    return slope_list


def get_rank(context, stock_pool):
    """选股模块-动量因子轮动"""
    score_list = []
    for stock in context.stock_pool:
        close_prices = history_bars(stock, context.momentum_day, '1d', 'close')
        if close_prices is None or len(close_prices) < context.momentum_day:
            continue
        y = np.log(close_prices)
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        annualized_returns = np.exp(slope * 250) - 1
        r_squared = 1 - (np.sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
        score = annualized_returns * r_squared
        score_list.append((stock, score))
    score_list.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in score_list[:context.stock_num]]


def get_ols(x, y):
    """择时模块-计算线性回归统计值"""
    slope, intercept = np.polyfit(x, y, 1)
    return intercept, slope


def get_rsrs_score(context):
    """计算RSRS择时信号"""
    stock = context.ref_stock
    N = context.N
    M = context.M

    lows = history_bars(stock, N, '1d', 'low')
    highs = history_bars(stock, N, '1d', 'high')
    if lows is None or highs is None or len(lows) < N or len(highs) < N:
        return 0

    x = lows  # low
    y = highs  # high

    _, slope = get_ols(x, y)
    context.slope_series = np.append(context.slope_series, slope)

    # 计算zscore
    if len(context.slope_series) < M:
        return 0

    mean = np.mean(context.slope_series[-M:])
    std = np.std(context.slope_series[-M:])
    zscore = (slope - mean) / std if std != 0 else 0

    # 修正标准分：用当前窗口的R²
    fitted = slope * x + np.polyfit(x, y, 1)[1]
    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    rsrs_score = zscore * r2

    return rsrs_score


def my_trade(context, bar_dict):
    """每日交易函数"""
    # 获取RSRS信号
    rsrs_score = get_rsrs_score(context)

    if rsrs_score < context.score_threshold:
        # 平仓
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    # 动量选股
    rank_stock = get_rank(context, context.stock_pool)
    if not rank_stock:
        return

    target_stock = rank_stock[0]

    # 买入评分最高的ETF
    for stock in list(context.portfolio.positions.keys()):
        if stock != target_stock:
            order_target_value(stock, 0)

    order_target_value(target_stock, context.portfolio.total_value)


def check_lose(context, bar_dict):
    """检查止损"""
    pass


def print_trade_info(context, bar_dict):
    """打印交易信息"""
    positions = list(context.portfolio.positions.keys())
    print('当前持仓: %s' % positions)
    print('账户价值: %.2f' % context.portfolio.total_value)