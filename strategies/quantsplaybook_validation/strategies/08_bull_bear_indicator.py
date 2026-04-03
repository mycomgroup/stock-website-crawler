# 牛熊指标择时策略 - RiceQuant版本
# 来源：《华泰证券-华泰金工量化择时系列：牛熊指标在择时轮动中的应用探讨》
# 使用波动率和换手率构建牛熊指标

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.vol_period = 20  # 波动率计算周期
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    vol_period = context.vol_period

    # 获取历史数据
    prices = history_bars(security, vol_period + 30, '1d', 'close')
    if prices is None or len(prices) < vol_period + 10:
        return

    closes = np.array(prices)

    # 计算收益率
    returns = np.diff(closes) / closes[:-1]

    # 计算波动率（标准差）
    vol = np.std(returns[-vol_period:]) * np.sqrt(252)  # 年化波动率

    # 计算历史波动率的分位数
    vol_history = []
    for i in range(vol_period, len(returns)):
        vol_history.append(np.std(returns[i-vol_period:i]) * np.sqrt(252))

    vol_percentile = np.mean(vol > np.array(vol_history))

    # 牛熊指标逻辑：
    # 高波动率（分位数>0.7）→ 熊市信号，卖出
    # 低波动率（分位数<0.3）→ 牛市信号，买入

    # 计算趋势确认
    ma_short = np.mean(closes[-5:])
    ma_long = np.mean(closes[-20:])
    trend_up = ma_short > ma_long

    # 交易逻辑
    if vol_percentile < 0.3 and trend_up and not context.pos:
        # 低波动+上升趋势 → 牛市信号
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入牛市信号: vol_pct={vol_percentile:.2f}, vol={vol:.2f}")
    elif vol_percentile > 0.7 and context.pos:
        # 高波动 → 熊市信号
        order_to(security, 0)
        context.pos = False
        print(f"卖出熊市信号: vol_pct={vol_percentile:.2f}, vol={vol:.2f}")