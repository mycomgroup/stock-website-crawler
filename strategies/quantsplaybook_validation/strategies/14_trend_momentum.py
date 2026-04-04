# 趋与势量化定义择时策略 - RiceQuant版本
# 来源：《国泰君安-数量化专题之六十四：趋与势的量化定义研究》
# 通过量化"趋"(方向)和"势"(强度)进行择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.trend_period = 20  # 趋势周期
    context.momentum_period = 10  # 动量周期
    context.pos = False

def calculate_trend(closes, period):
    """计算趋：价格方向"""
    if len(closes) < period:
        return 0

    # 趋 = 线性回归斜率方向
    x = np.arange(period)
    y = closes[-period:]

    # 简单线性回归
    n = period
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)

    # 归一化斜率
    trend = slope / closes[-1] * 100  # 百分比

    return trend

def calculate_momentum(closes, period):
    """计算势：价格强度"""
    if len(closes) < period + 1:
        return 0

    # 势 = 收益率的一致性和幅度
    returns = np.diff(closes[-period-1:]) / closes[-period-1:-1]

    # 正收益占比
    positive_ratio = np.sum(returns > 0) / len(returns)

    # 平均收益幅度
    avg_return = np.mean(returns)

    # 势 = 方向一致性 * 幅度
    momentum = positive_ratio * np.sign(avg_return) * np.abs(avg_return) * 100

    return momentum

def handle_bar(context, bar_dict):
    security = context.security
    trend_period = context.trend_period
    momentum_period = context.momentum_period

    # 获取历史收盘价
    prices = history_bars(security, max(trend_period, momentum_period) + 20, '1d', 'close')
    if prices is None or len(prices) < trend_period + 10:
        return

    closes = np.array(prices)

    # 计算趋和势
    trend = calculate_trend(closes, trend_period)
    momentum = calculate_momentum(closes, momentum_period)

    # 综合信号
    # 趋 > 0 且 势 > 0 → 上涨趋势
    # 趋 < 0 且 势 < 0 → 下跌趋势

    # 计算历史分位数
    trend_history = []
    momentum_history = []

    for i in range(trend_period + 10, len(closes)):
        t = calculate_trend(closes[:i], trend_period)
        m = calculate_momentum(closes[:i], momentum_period)
        trend_history.append(t)
        momentum_history.append(m)

    if trend_history:
        trend_pct = np.mean(trend > np.array(trend_history))
        momentum_pct = np.mean(momentum > np.array(momentum_history))
    else:
        trend_pct = 0.5
        momentum_pct = 0.5

    # 交易逻辑
    # 趋势共振：趋和势方向一致且强度高

    if trend > 0 and momentum > 0 and trend_pct > 0.6 and momentum_pct > 0.6 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: 趋={trend:.4f}, 势={momentum:.4f}")
    elif (trend < 0 or momentum < 0) and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: 趋={trend:.4f}, 势={momentum:.4f}")