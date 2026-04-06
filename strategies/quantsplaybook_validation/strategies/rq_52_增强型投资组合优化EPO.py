# 原文链接：https://www.joinquant.com/post/35307（EPO方法研究）
# 策略：增强型投资组合优化（EPO）方法
# 核心逻辑：用EPO（Enhanced Portfolio Optimization）方法优化ETF组合权重
# 注：原版用 scipy.linalg.solve，此处用 numpy.linalg.solve 替代

import numpy as np

ETF_POOL = [
    '510300.XSHG',  # 沪深300
    '510500.XSHG',  # 中证500
    '159915.XSHE',  # 创业板
    '511010.XSHG',  # 国债
    '518880.XSHG',  # 黄金
]
LOOKBACK = 60   # 协方差计算窗口
W = 0.5         # 收缩参数


def epo_weights(returns_matrix, signal, lambda_=1.0, w=W):
    """
    EPO 简化版：用收缩协方差矩阵计算最优权重
    returns_matrix: (T, N) 收益率矩阵
    signal: (N,) 动量信号
    """
    n = returns_matrix.shape[1]
    vcov = np.cov(returns_matrix.T)
    corr = np.corrcoef(returns_matrix.T)
    std_diag = np.sqrt(np.diag(vcov))
    V = np.diag(std_diag)
    I = np.eye(n)

    # 收缩相关矩阵
    shrunk_cor = (1 - w) * corr + w * I
    cov_tilde = V @ shrunk_cor @ V

    try:
        inv_cov = np.linalg.solve(cov_tilde, np.eye(n))
    except np.linalg.LinAlgError:
        return np.ones(n) / n

    epo = (1.0 / lambda_) * inv_cov @ signal
    # 只保留正权重
    epo = np.maximum(epo, 0)
    total = epo.sum()
    if total == 0:
        return np.ones(n) / n
    return epo / total


def init(context):
    context.etf_pool = ETF_POOL
    context.month = -1
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    if context.now.month == context.month:
        return
    context.month = context.now.month

    # 获取各ETF历史收益率
    returns_list = []
    valid_etfs = []
    for etf in context.etf_pool:
        prices = history_bars(etf, LOOKBACK + 1, '1d', 'close')
        if prices is None or len(prices) < LOOKBACK + 1:
            continue
        p = np.array(prices, dtype=float)
        ret = np.diff(p) / p[:-1]
        returns_list.append(ret)
        valid_etfs.append(etf)

    if len(valid_etfs) < 2:
        return

    returns_matrix = np.column_stack(returns_list)

    # 动量信号：过去60天收益率
    signal = np.array([returns_list[i].sum() for i in range(len(valid_etfs))])

    weights = epo_weights(returns_matrix, signal)

    # 清仓不在目标的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in valid_etfs:
            order_target_value(s, 0)

    # 按EPO权重调仓
    total_value = context.portfolio.total_value
    for i, etf in enumerate(valid_etfs):
        order_target_value(etf, total_value * weights[i] * 0.95)

    print(f"[EPO] weights={dict(zip(valid_etfs, weights.round(3)))}")
