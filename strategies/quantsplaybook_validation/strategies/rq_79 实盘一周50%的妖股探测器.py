# 实盘一周50%的妖股探测器 - RiceQuant版本
# 原文：https://www.joinquant.com/post/37894
# 作者：Dr.QYQ
# 逻辑：沪深300成分股中，MACD金叉 + KDJ金叉 + 量能放大，短线动量策略
#       MACD/KDJ 全部用 numpy 手动实现，周度调仓，持仓5只

import numpy as np


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_pool = '000300.XSHG'
    context.stock_num = 5
    context.last_week = -1
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


# ── 技术指标（numpy 实现）────────────────────────────────────────────────────

def _ema(arr, period):
    """指数移动平均"""
    k = 2.0 / (period + 1)
    result = np.zeros(len(arr))
    result[0] = arr[0]
    for i in range(1, len(arr)):
        result[i] = arr[i] * k + result[i - 1] * (1 - k)
    return result


def calc_macd(closes, fast=12, slow=26, signal=9):
    """返回 (dif, dea, hist) 各为 numpy 数组"""
    ema_fast = _ema(closes, fast)
    ema_slow = _ema(closes, slow)
    dif = ema_fast - ema_slow
    dea = _ema(dif, signal)
    hist = dif - dea
    return dif, dea, hist


def calc_kdj(highs, lows, closes, n=9, m=3):
    """返回 (K, D, J) 各为 numpy 数组"""
    length = len(closes)
    rsv = np.zeros(length)
    for i in range(length):
        start = max(0, i - n + 1)
        h_max = np.max(highs[start: i + 1])
        l_min = np.min(lows[start: i + 1])
        denom = h_max - l_min
        rsv[i] = (closes[i] - l_min) / denom * 100 if denom > 0 else 50.0

    K = _ema(rsv, m)
    D = _ema(K, m)
    J = 3 * K - 2 * D
    return K, D, J


# ── 单股信号判断 ──────────────────────────────────────────────────────────────

def _check_signal(stock):
    """返回 True 表示满足买入条件"""
    data_high = history_bars(stock, 60, '1d', 'high')
    data_low = history_bars(stock, 60, '1d', 'low')
    data_close = history_bars(stock, 60, '1d', 'close')
    data_volume = history_bars(stock, 60, '1d', 'volume')
    if data_high is None or data_low is None or data_close is None or len(data_close) < 40:
        return False

    closes = data_close.astype(float)
    highs = data_high.astype(float)
    lows = data_low.astype(float)
    volumes = data_volume.astype(float)

    # MACD 金叉：hist 由负转正（昨日 < 0，今日 >= 0）
    _, _, hist = calc_macd(closes)
    if hist[-2] >= 0 or hist[-1] < 0:
        return False

    # KDJ 金叉：J > K > D（多头排列）
    K, D, J = calc_kdj(highs, lows, closes)
    if not (J[-1] > K[-1] > D[-1]):
        return False

    # 量能放大：今日成交量 > 20日均量 × 1.5
    avg_vol = np.mean(volumes[-21:-1])
    if avg_vol <= 0 or volumes[-1] < avg_vol * 1.5:
        return False

    return True


# ── 选股 ──────────────────────────────────────────────────────────────────────

def get_stock_list(context, bar_dict):
    stocks = index_components(context.stock_pool)
    candidates = []
    for s in stocks:
        try:
            if s not in bar_dict or not bar_dict[s].is_trading:
                continue
            if _check_signal(s):
                candidates.append(s)
        except Exception:
            continue
    # 按当日涨幅排序，取动量最强的前 N 只
    if not candidates:
        return []
    scored = []
    for s in candidates:
        data = history_bars(s, 6, '1d', 'close')
        if data is not None and len(data) >= 6:
            momentum = data[-1] / data[0] - 1
            scored.append((s, momentum))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored[: context.stock_num]]


# ── 交易主函数 ────────────────────────────────────────────────────────────────

def my_trade(context, bar_dict):
    # 周度调仓（每周执行一次）
    week = context.now.isocalendar()[1]
    if week == context.last_week:
        return
    context.last_week = week

    target = get_stock_list(context, bar_dict)

    # 卖出不在目标列表的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    if not target:
        return

    w = 1.0 / len(target)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, context.portfolio.total_value * w * 0.95)
