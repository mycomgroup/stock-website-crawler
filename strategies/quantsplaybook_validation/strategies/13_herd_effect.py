# 羊群效应CCK择时策略 - RiceQuant版本
# 来源：《国泰君安-基于CCK模型的股票市场羊群效应研究》
# 检测市场羊群效应程度进行择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20  # 计算周期
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    # 获取历史收盘价
    prices = history_bars(security, period + 30, '1d', 'close')
    if prices is None or len(prices) < period + 10:
        return

    closes = np.array(prices)

    # 计算市场收益率
    market_returns = np.diff(closes) / closes[:-1]

    if len(market_returns) < period:
        return

    # CCK羊群效应指标
    # 羊群效应 = 市场收益率离散度的非线性变化
    # 简化实现：使用收益率的横截面方差变化

    # 计算滚动波动率
    vol_history = []
    for i in range(period, len(market_returns)):
        vol = np.std(market_returns[i-period:i])
        vol_history.append(vol)

    current_vol = np.std(market_returns[-period:])

    # 波动率变化率
    if len(vol_history) > 0:
        avg_vol = np.mean(vol_history)
        vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1
    else:
        vol_ratio = 1

    # 计算收益率的绝对值均值
    abs_returns = np.abs(market_returns[-period:])
    mean_abs_return = np.mean(abs_returns)

    # 羊群效应指标：波动率与收益率的比率
    # 高比率 + 低波动 → 羊群效应强
    # 低比率 + 高波动 → 羊群效应弱

    # 计算历史分位数
    abs_history = []
    for i in range(period, len(market_returns)):
        abs_history.append(np.mean(np.abs(market_returns[i-period:i])))

    abs_percentile = np.mean(mean_abs_return > np.array(abs_history)) if abs_history else 0.5
    vol_percentile = np.mean(current_vol > np.array(vol_history)) if vol_history else 0.5

    # 交易逻辑
    # 羊群效应强(低波动分位 + 高收益分位) → 市场一致性强，跟随趋势
    # 羊群效应弱(高波动分位) → 市场分歧大，观望

    # 简化：低波动+正收益趋势 → 买入
    recent_return = np.mean(market_returns[-5:])

    if vol_percentile < 0.3 and recent_return > 0 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: vol_pct={vol_percentile:.2f}, trend={recent_return:.4f}")
    elif vol_percentile > 0.7 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: vol_pct={vol_percentile:.2f}")