# 原文链接：https://www.joinquant.com/post/44910
# 策略：菜场大妈高质低价法策略
# 作者：菜场大妈
# 核心逻辑：低PB+高ROE+KDJ金叉选股，月度调仓
# 注：原版用jqlib KD/VOL，此处本地实现KDJ

import numpy as np


def calc_kdj(highs, lows, closes, n=9, m1=3, m2=3):
    """计算KDJ指标"""
    length = len(closes)
    if length < n:
        return None, None, None
    k_arr = np.full(length, 50.0)
    d_arr = np.full(length, 50.0)
    for i in range(n - 1, length):
        hh = np.max(highs[i - n + 1:i + 1])
        ll = np.min(lows[i - n + 1:i + 1])
        rsv = (closes[i] - ll) / (hh - ll + 1e-9) * 100
        k_arr[i] = k_arr[i - 1] * (m1 - 1) / m1 + rsv / m1
        d_arr[i] = d_arr[i - 1] * (m2 - 1) / m2 + k_arr[i] / m2
    j_arr = 3 * k_arr - 2 * d_arr
    return k_arr, d_arr, j_arr


def init(context):
    context.n_stocks = 8
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：低PB+高ROE基本面筛选，再用KDJ金叉过滤"""
    stocks_300 = index_components('000300.XSHG')
    stocks_300 = [s for s in stocks_300 if not s.startswith('688')]

    # 基本面筛选：低PB + 高ROE
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks_300,
        ['pb_ratio', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 3.0]
    df = df[df['roe'] > 0.1]
    df = df.head(50)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    candidates = list(df.index)

    # KDJ金叉过滤
    kdj_stocks = []
    for s in candidates:
        highs  = history_bars(s, 20, '1d', 'high')
        lows   = history_bars(s, 20, '1d', 'low')
        closes = history_bars(s, 20, '1d', 'close')
        if highs is None or len(highs) < 15:
            continue
        k, d, j = calc_kdj(
            np.array(highs, dtype=float),
            np.array(lows, dtype=float),
            np.array(closes, dtype=float)
        )
        if k is None:
            continue
        # KDJ金叉：K上穿D
        if k[-1] > d[-1] and k[-2] <= d[-2] and k[-1] < 80:
            kdj_stocks.append(s)

    context.stock_pool = kdj_stocks[:context.n_stocks]
    if not context.stock_pool:
        # 无金叉则直接用基本面前N只
        context.stock_pool = candidates[:context.n_stocks]
    logger.info(f"[菜场大妈] 选股={context.stock_pool}")

    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
