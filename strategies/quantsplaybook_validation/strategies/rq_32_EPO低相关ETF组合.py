# EPO优化低相关ETF组合策略 - RiceQuant版本
# 原文：EPO优化低相关etf组合
# 作者：开心果
# 原文：https://www.joinquant.com/post/50253
# 逻辑：用增强型组合优化(EPO)方法对低相关ETF进行权重优化

import numpy as np
import pandas as pd


ETF_POOL = [
    '159985.XSHE',  # 豆粕ETF
    '518880.XSHG',  # 黄金ETF
    '513100.XSHG',  # 纳指100
    '513500.XSHG',  # 标普500ETF（原德国ETF已退市）
    '159930.XSHE',  # 能源化工ETF
    '159981.XSHE',  # 能源ETF
    '159980.XSHE',  # 有色金属ETF
    '510880.XSHG',  # 红利ETF
    '510230.XSHG',  # 金融ETF
]


def epo_weights(returns, lambda_=10, w=0.6):
    """简化版EPO权重计算"""
    n = returns.shape[1]
    vcov = np.cov(returns.T)
    V = np.diag(np.diag(vcov))
    std = np.sqrt(V)

    corr = np.corrcoef(returns.T)
    I = np.eye(n)
    shrunk_cor = (1 - w) * corr + w * I
    cov_tilde = std @ shrunk_cor @ std

    d = np.diag(vcov)
    signal = (1 / d) / np.sum(1 / d)

    try:
        inv_cov = np.linalg.inv(cov_tilde)
        raw_weights = (1 / lambda_) * inv_cov @ signal
        raw_weights = np.maximum(raw_weights, 0)
        total = np.sum(raw_weights)
        if total > 0:
            return raw_weights / total
        return np.ones(n) / n
    except Exception:
        return np.ones(n) / n


def init(context):
    context.etf_pool = ETF_POOL
    context.lookback = 250
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    price_data = {}
    for etf in context.etf_pool:
        try:
            prices = history_bars(etf, context.lookback, '1d', 'close')
            if prices is not None and len(prices) >= context.lookback:
                price_data[etf] = np.array(prices, dtype=float)
        except Exception:
            continue

    if len(price_data) < 3:
        return

    valid_etfs = list(price_data.keys())
    returns = np.column_stack([np.diff(price_data[e]) / price_data[e][:-1] for e in valid_etfs])

    weights_arr = epo_weights(returns)
    weights = dict(zip(valid_etfs, weights_arr))

    for etf in list(context.portfolio.positions.keys()):
        if etf not in weights:
            order_target_value(etf, 0)

    total_value = context.portfolio.total_value
    for etf, w in weights.items():
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(etf, total_value * w * 0.95)
