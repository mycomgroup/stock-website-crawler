# 注意：原策略使用 jqfactor 获取 ROIC 等因子、talib 计算技术指标、pickle 持久化模型，
# 均为聚宽平台专属依赖，无法在 RiceQuant 直接运行。
# 此版本改用风险平价（波动率倒数加权）+ 动量过滤替代原逻辑，逻辑有所简化。
#
# 原策略来源：https://www.joinquant.com/post/48819
# 原作者：MarioC

"""
全天候轮动策略（RiceQuant 简化版）

策略逻辑：
1. 资产池：沪深300ETF、中证500ETF、国债ETF、黄金ETF、豆粕ETF
2. 每月调仓一次
3. 计算过去 lookback 天的动量（总收益率）和波动率（年化标准差）
4. 动量为负的资产剔除
5. 剩余资产按 1/波动率 做风险平价加权，归一化后分配仓位
6. 仓位上限 95%（留少量现金应对赎回）
"""

import numpy as np

ASSETS = [
    '510300.XSHG',  # 沪深300ETF
    '510500.XSHG',  # 中证500ETF
    '511010.XSHG',  # 国债ETF
    '518880.XSHG',  # 黄金ETF
    '159985.XSHE',  # 豆粕ETF（商品代表）
]


def init(context):
    context.assets = ASSETS
    context.lookback = 60      # 动量/波动率回看天数
    context.month = -1         # 上次调仓月份，初始化为 -1 确保首日触发


def handle_bar(context, bar_dict):
    # 月度调仓：同月内只执行一次
    if context.now.month == context.month:
        return
    context.month = context.now.month

    weights = {}

    for asset in context.assets:
        prices = history_bars(asset, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback + 1:
            continue

        p = np.array(prices, dtype=float)

        # 动量：区间总收益率
        momentum = p[-1] / p[0] - 1
        if momentum <= 0:
            continue  # 动量为负，跳过该资产

        # 波动率：日收益率年化标准差
        daily_returns = np.diff(p) / p[:-1]
        vol = np.std(daily_returns) * np.sqrt(252)
        if vol > 0:
            weights[asset] = 1.0 / vol  # 风险平价权重

    if not weights:
        # 全部动量为负时空仓（可选：改为持有国债ETF）
        for asset in list(context.portfolio.positions.keys()):
            order_target_value(asset, 0)
        return

    # 归一化权重
    total = sum(weights.values())

    # 先清仓不在目标池的持仓
    for asset in list(context.portfolio.positions.keys()):
        if asset not in weights:
            order_target_value(asset, 0)

    # 按目标权重下单，留 5% 现金缓冲
    for asset, w in weights.items():
        target_value = context.portfolio.total_value * (w / total) * 0.95
        order_target_value(asset, target_value)
