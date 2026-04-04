# MLT-TSMOM 多标的时序动量策略 - RiceQuant版本
# 来源：《MLT_TSMOM》（Multi-Label Time-Series Momentum）
# 核心逻辑：传统TSMOM = sign(过去252日收益) * (目标波动率/历史波动率) * 未来收益
#           MLT改进：用多个时间窗口的动量信号加权，提高稳健性
#           标的：黄金ETF、纳指ETF、创业板ETF、沪深300ETF

import numpy as np


ETFS = {
    '518880.XSHG': '黄金ETF',
    '513100.XSHG': '纳指ETF',
    '159915.XSHE': '创业板ETF',
    '510300.XSHG': '沪深300ETF',
}

TARGET_VOL = 0.15  # 目标年化波动率


def calc_tsmom_weight(returns, lookback=252, vol_window=60):
    """
    计算TSMOM权重
    weight = sign(r_lookback) * (target_vol / hist_vol)
    """
    if len(returns) < lookback:
        return 0

    r = np.array(returns, dtype=float)

    # 过去lookback日收益率
    r_lookback = np.prod(1 + r[-lookback:]) - 1

    # 历史波动率（指数衰减）
    recent_returns = r[-vol_window:]
    # 指数衰减权重
    decay = 0.94
    weights = np.array([decay ** (vol_window - 1 - i) for i in range(vol_window)])
    weights /= weights.sum()
    hist_vol = np.sqrt(np.average(recent_returns ** 2, weights=weights) * 252)

    if hist_vol == 0:
        return 0

    signal = np.sign(r_lookback)
    weight = signal * (TARGET_VOL / hist_vol)

    # 限制权重范围
    return np.clip(weight, -1.5, 1.5)


def calc_mlt_weight(returns, lookbacks=[63, 126, 252], vol_window=60):
    """
    MLT-TSMOM：多时间窗口加权
    """
    weights = []
    for lb in lookbacks:
        if len(returns) >= lb:
            w = calc_tsmom_weight(returns, lb, vol_window)
            weights.append(w)

    if not weights:
        return 0

    # 等权平均多个时间窗口的信号
    return np.mean(weights)


def init(context):
    context.etfs = list(ETFS.keys())
    context.vol_window = 60
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    weights = {}
    for etf in context.etfs:
        if etf is None:  # placeholder, actual check via history_bars
            pass
        try:
            prices = history_bars(etf, 255, '1d', 'close')
            if prices is None or len(prices) < 63 or prices[-1] == 0:
                continue
            prices = np.array(prices, dtype=float)
            returns = np.diff(prices) / prices[:-1]

            w = calc_mlt_weight(returns, [63, 126, 252], context.vol_window)
            weights[etf] = w
        except Exception:
            continue

    if not weights:
        return

    # 归一化权重（只做多）
    long_weights = {k: max(v, 0) for k, v in weights.items()}
    total_w = sum(long_weights.values())

    total_value = context.portfolio.total_value

    # 先平仓不需要的
    for etf in list(context.portfolio.positions.keys()):
        if etf not in long_weights or long_weights[etf] == 0:
            order_to(etf, 0)

    if total_w > 0:
        for etf, w in long_weights.items():
            if w > 0:
                target_value = total_value * (w / total_w) * 0.95
                order_target_value(etf, target_value)

    print(f"MLT-TSMOM权重: {weights}")
