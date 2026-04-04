# 高质量动量因子选股策略 - RiceQuant版本
# 来源：《高质量动量因子选股》
# 核心逻辑：使用风险调整后的60日动量因子（r60 - 3*sigma_annual^2）
#           在中证500成分股中选股，月度调仓

import numpy as np


def init(context):
    context.index = '000905.XSHG'   # 中证500
    context.lookback = 60            # 动量计算窗口
    context.top_n = 30               # 持仓数量
    context.rebalance_day = 1        # 每月第1个交易日调仓
    context.month = -1


def handle_bar(context, bar_dict):
    # 月度调仓
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    # 获取中证500成分股
    stocks = index_components(context.index)
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.lookback + 1, '1d', 'close')
            if prices is None or len(prices) < context.lookback + 1:
                continue
            prices = np.array(prices, dtype=float)
            # 跳过停牌（最新价为0或与前日相同超过5天）
            if prices[-1] == 0:
                continue
            returns = np.diff(prices) / prices[:-1]

            r60 = (prices[-1] / prices[0]) - 1
            # 年化波动率（原论文用年化标准差）
            sigma_annual = np.std(returns) * np.sqrt(252)
            # 风险调整动量因子：r60 - 3 * sigma_annual^2
            # 原论文系数约为3（年化），不是3000（日化）
            momentum_factor = r60 - 3 * sigma_annual ** 2
            scores[stock] = momentum_factor
        except Exception:
            continue

    if not scores:
        return

    # 按因子值降序排列，选前N只
    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    # 卖出不在目标中的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    # 等权买入目标股票
    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
