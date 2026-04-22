# 原文链接：https://www.joinquant.com/post/52xxx
# 策略：增强型投资组合优化（EPO）方法研究
# 核心逻辑：EPO优化，用等权+最小方差混合权重，选低相关性ETF组合

import numpy as np

ETF_POOL = [
    '510300.XSHG',  # 沪深300
    '510500.XSHG',  # 中证500
    '159915.XSHE',  # 创业板
    '511010.XSHG',  # 国债
    '518880.XSHG',  # 黄金ETF
]
LOOKBACK = 60   # 回看天数
ALPHA = 0.5     # 等权与最小方差的混合比例

def calc_min_var_weights(returns_matrix):
    """计算最小方差权重（简化版）"""
    n = returns_matrix.shape[1]
    cov = np.cov(returns_matrix.T)
    # 简化：用方差倒数作为权重
    variances = np.diag(cov)
    variances = np.where(variances <= 0, 1e-6, variances)
    inv_var = 1.0 / variances
    weights = inv_var / inv_var.sum()
    return weights

def init(context):
    context.etf_pool = ETF_POOL
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    returns_list = []
    valid_etfs = []

    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, LOOKBACK + 1, '1d', 'close')
            if len(closes) < LOOKBACK + 1:
                continue
            rets = np.diff(closes) / closes[:-1]
            returns_list.append(rets)
            valid_etfs.append(etf)
        except Exception as e:
            logger.info(f"ETF {etf} 数据获取失败: {e}")

    if len(valid_etfs) < 2:
        return

    returns_matrix = np.array(returns_list).T  # shape: (days, n_etfs)
    n = len(valid_etfs)

    # 等权权重
    equal_weights = np.ones(n) / n
    # 最小方差权重
    min_var_weights = calc_min_var_weights(returns_matrix)
    # EPO混合权重
    epo_weights = ALPHA * equal_weights + (1 - ALPHA) * min_var_weights
    epo_weights = epo_weights / epo_weights.sum()

    total = context.portfolio.cash * 0.95
    for etf, w in zip(valid_etfs, epo_weights):
        order_target_value(etf, total * w)
        logger.info(f"EPO买入 {etf}，权重 {w:.4f}")
