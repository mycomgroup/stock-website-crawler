# 注意：原策略使用 talib 计算 RSI/MA 做择时、scipy.optimize 做均值方差优化（MVO）、
# inout_cash 每日注入 400 元模拟定投，均为聚宽平台专属或外部依赖。
# 此版本删除上述依赖，改用等权重 + 动量过滤替代 MVO，同时删除定投功能，逻辑有所简化。
#
# 原策略来源：https://www.joinquant.com/post/24542
# 原作者：富在知足

"""
FOF 养老成长基金策略（RiceQuant 简化版）

策略逻辑：
1. 基金池：价值100ETF、中证红利、红利低波ETF、上证50ETF、
           沪深300ETF、黄金ETF、国债ETF、中概互联ETF
2. 每月调仓一次
3. 计算每只基金过去 lookback 天的动量（总收益率）
4. 选取动量为正的基金，等权持有
5. 若全部动量为负，则持有国债ETF（防御仓位）
"""

import numpy as np

FUND_POOL = [
    '515520.XSHG',  # 价值100ETF
    '161907.XSHE',  # 中证红利
    '512890.XSHG',  # 红利低波ETF
    '510050.XSHG',  # 上证50ETF
    '510310.XSHG',  # 沪深300ETF
    '518880.XSHG',  # 黄金ETF
    '511010.XSHG',  # 国债ETF（同时作为防御标的）
    '513050.XSHG',  # 中概互联ETF
]

DEFENSIVE_ASSET = '511010.XSHG'  # 全部动量为负时的防御仓位


def init(context):
    context.fund_pool = FUND_POOL
    context.lookback = 60      # 动量回看天数
    context.month = -1         # 上次调仓月份


def handle_bar(context, bar_dict):
    # 月度调仓
    if context.now.month == context.month:
        return
    context.month = context.now.month

    positive_momentum = []

    for fund in context.fund_pool:
        prices = history_bars(fund, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback + 1:
            continue

        p = np.array(prices, dtype=float)
        momentum = p[-1] / p[0] - 1

        if momentum > 0:
            positive_momentum.append(fund)

    # 确定目标持仓
    if positive_momentum:
        targets = positive_momentum
    else:
        # 全部动量为负，切换至防御资产
        targets = [DEFENSIVE_ASSET]

    # 等权重分配，留 5% 现金缓冲
    weight = 0.95 / len(targets)

    # 清仓不在目标列表的持仓
    for fund in list(context.portfolio.positions.keys()):
        if fund not in targets:
            order_target_value(fund, 0)

    # 按等权重下单
    for fund in targets:
        target_value = context.portfolio.total_value * weight
        order_target_value(fund, target_value)
