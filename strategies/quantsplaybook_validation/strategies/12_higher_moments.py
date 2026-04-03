# 指数高阶矩择时策略 - RiceQuant版本
# 来源：《广发证券-交易性择时策略研究之八：指数高阶矩择时策略》
# 利用收益率的偏度和峰度进行市场择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 60  # 计算周期
    context.pos = False

def calculate_moments(returns):
    """计算高阶矩：偏度和峰度"""
    n = len(returns)
    if n < 2:
        return 0, 0

    mean = np.mean(returns)
    std = np.std(returns)

    if std == 0:
        return 0, 0

    # 标准化
    standardized = (returns - mean) / std

    # 偏度 (三阶矩) - 衡量分布不对称性
    skewness = np.mean(standardized ** 3)

    # 峰度 (四阶矩) - 衡量分布尾部厚度
    kurtosis = np.mean(standardized ** 4) - 3  # 超额峰度

    return skewness, kurtosis

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    # 获取历史收盘价
    prices = history_bars(security, period + 10, '1d', 'close')
    if prices is None or len(prices) < period:
        return

    closes = np.array(prices)

    # 计算收益率
    returns = np.diff(closes) / closes[:-1]

    if len(returns) < period:
        return

    # 使用最近period天的收益率
    recent_returns = returns[-period:]

    # 计算高阶矩
    skewness, kurtosis = calculate_moments(recent_returns)

    # 计算历史偏度分位数
    skew_history = []
    for i in range(period, len(returns)):
        r = returns[i-period:i]
        s, _ = calculate_moments(r)
        skew_history.append(s)

    skew_percentile = np.mean(skewness > np.array(skew_history)) if skew_history else 0.5

    # 交易逻辑
    # 负偏度高分位 → 极端下跌风险释放 → 买入机会
    # 正偏度高分位 → 极端上涨情绪过热 → 卖出信号

    if skewness < -0.5 and skew_percentile < 0.3 and not context.pos:
        # 负偏度较大，市场恐慌，买入机会
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: skew={skewness:.3f}, kurt={kurtosis:.3f}")
    elif skewness > 0.5 and skew_percentile > 0.7 and context.pos:
        # 正偏度较大，市场过热，卖出
        order_to(security, 0)
        context.pos = False
        print(f"卖出: skew={skewness:.3f}, kurt={kurtosis:.3f}")