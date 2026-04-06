# EPS+MS因子的大盘蓝筹策略 - RiceQuant版本
# 原文：https://www.joinquant.com/post/34372
# 作者：wywy1995
# 逻辑：沪深300成分股，先按EPS筛选前25%，再按净利润率筛选前25%，
#       按市值降序排列取前5只，月度调仓 + RSRS择时

import numpy as np


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_pool = '000300.XSHG'
    context.stock_num = 5
    context.percentile = 0.25
    context.N = 18          # RSRS回归窗口
    context.M = 300         # RSRS zscore历史长度
    context.score_threshold = 0.7
    context.last_month = -1
    context.slope_series = []
    context.slope_initialized = False
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


# ── RSRS 初始化：预填历史斜率序列 ──────────────────────────────────────────────

def _init_slopes(context):
    need = context.M + context.N
    highs = history_bars('000300.XSHG', need, '1d', 'high')
    lows = history_bars('000300.XSHG', need, '1d', 'low')
    if highs is None or lows is None or len(highs) < need:
        return []
    slopes = []
    for i in range(context.M):
        seg_low = lows[i: i + context.N]
        seg_high = highs[i: i + context.N]
        slope = np.polyfit(seg_low, seg_high, 1)[0]
        slopes.append(slope)
    return slopes


# ── RSRS 信号 ─────────────────────────────────────────────────────────────────

def _rsrs_signal(context):
    highs = history_bars('000300.XSHG', context.N, '1d', 'high')
    lows = history_bars('000300.XSHG', context.N, '1d', 'low')
    if highs is None or lows is None or len(highs) < context.N:
        return 'KEEP'

    low = lows
    high = highs
    slope, intercept = np.polyfit(low, high, 1)
    context.slope_series.append(slope)

    series = np.array(context.slope_series[-context.M:])
    if len(series) < 30:
        return 'KEEP'

    mean = np.mean(series)
    std = np.std(series)
    if std == 0:
        return 'KEEP'

    # R² 修正
    fitted = slope * low + intercept
    ss_res = np.sum((high - fitted) ** 2)
    ss_tot = np.sum((high - np.mean(high)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    zscore = (series[-1] - mean) / std * r2

    # MA 辅助过滤
    closes = history_bars('000300.XSHG', 25, '1d', 'close')
    if closes is None or len(closes) < 25:
        return 'KEEP'
    ma_now = np.mean(closes[-22:])
    ma_before = np.mean(closes[:22])

    if zscore > context.score_threshold and ma_now > ma_before:
        return 'BUY'
    if zscore < -context.score_threshold and ma_now < ma_before:
        return 'SELL'
    return 'KEEP'


# ── 选股 ──────────────────────────────────────────────────────────────────────

def get_stock_list(context):
    stocks = index_components(context.stock_pool)
    if not stocks:
        return []

    today = str(context.now)
    try:
        prev_date = context.now.date()
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'net_profit_margin', 'eps', 'net_profit'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['eps'] > 0.0]
        df = df[df['net_profit_margin'] > 0.0]
        df = df.head(100)
        candidates = df.index.tolist()
    except Exception:
        return []
    if df is None or len(df) == 0:
        return []

    # 第一层：EPS 前 25%
    n1 = max(1, int(context.percentile * len(df)))
    eps_top = df.nlargest(n1, 'eps')

    # 第二层：净利润率前 25%
    n2 = max(1, int(context.percentile * len(eps_top)))
    ms_top = eps_top.nlargest(n2, 'net_profit_margin')

    # 按流通市值降序，取前 N 只（大盘蓝筹）
    result = ms_top.sort_values('market_cap', ascending=False)
    return result.index.tolist()[: context.stock_num]


# ── 交易主函数 ────────────────────────────────────────────────────────────────

def my_trade(context, bar_dict):
    # 月度调仓
    if context.now.month == context.last_month:
        return
    context.last_month = context.now.month

    signal = _rsrs_signal(context)

    # 空仓信号：清仓
    if signal == 'SELL':
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    target = get_stock_list(context)
    if not target:
        return

    # 卖出不在目标列表的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    # 等权买入目标股票
    w = 1.0 / len(target)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, context.portfolio.total_value * w * 0.95)
