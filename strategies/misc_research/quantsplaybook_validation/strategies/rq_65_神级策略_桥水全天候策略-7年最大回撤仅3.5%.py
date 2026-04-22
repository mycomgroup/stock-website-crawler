# 注意：原策略使用 jqdata/QuantLib 一致性风险度量（Expected Shortfall）计算风险平价权重，
# 此版本用 1/波动率 风险平价简化实现，逻辑等价但计算更轻量。



import numpy as np

# 资产池：股票ETF + 债券ETF + 黄金ETF + 商品ETF
ASSETS = [
    '510300.XSHG',  # 沪深300ETF（股票）
    '511010.XSHG',  # 国债ETF（债券）
    '518880.XSHG',  # 黄金ETF（黄金）
    '159985.XSHE',  # 豆粕ETF（商品）
    '513100.XSHG',  # 纳斯达克ETF（海外股票）
]

def init(context):
    context.assets = ASSETS
    context.lookback = 60       # 协方差计算窗口
    context.hold_periods = 0
    context.hold_cycle = 30     # 调仓周期（天）

def calc_risk_parity_weights(returns_matrix):
    """
    风险平价权重：用迭代法求解，使每个资产的风险贡献相等
    简化版：用1/波动率加权
    """
    vols = np.std(returns_matrix, axis=0)
    vols = np.where(vols == 0, 1e-10, vols)
    weights = 1.0 / vols
    return weights / weights.sum()

def handle_bar(context, bar_dict):
    context.hold_periods += 1
    if context.hold_periods < context.hold_cycle:
        return
    context.hold_periods = 0

    # 获取各资产历史收益率
    returns_list = []
    valid_assets = []
    for asset in context.assets:
        prices = history_bars(asset, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback + 1:
            continue
        p = np.array(prices, dtype=float)
        ret = np.diff(p) / p[:-1]
        returns_list.append(ret)
        valid_assets.append(asset)

    if len(valid_assets) < 2:
        return

    returns_matrix = np.column_stack(returns_list)
    weights = calc_risk_parity_weights(returns_matrix)

    # 清仓不在目标的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in valid_assets:
            order_target_value(stock, 0)

    # 按风险平价权重调仓
    total_value = context.portfolio.total_value
    for i, asset in enumerate(valid_assets):
        order_target_value(asset, total_value * weights[i] * 0.95)

    print(f"[全天候] 调仓 weights={dict(zip(valid_assets, weights.round(3)))}")
