# 宽基ETF动量轮动+钝化RSRS择时策略 - RiceQuant版本
# 原文：宽基ETF动量轮动钝化RSRS择时-回撤小
# 作者：DominicLiu
# 原文：https://www.joinquant.com/post/37120
# 逻辑：3只宽基指数按动量评分选最优，叠加钝化RSRS择时信号

import numpy as np
import math


ETF_MAP = {
    '000300.XSHG': '510300.XSHG',  # 沪深300 -> ETF
    '000905.XSHG': '510500.XSHG',  # 中证500 -> ETF
    '399006.XSHE': '159915.XSHE',  # 创业板 -> ETF
}
CASH_ETF = '511880.XSHG'  # 货币基金

RSRS_PARAMS = {
    '000300.XSHG': {'N': 18, 'M': 700, 'threshold': 0.7},
    '000905.XSHG': {'N': 18, 'M': 800, 'threshold': 1.0},
    '399006.XSHE': {'N': 18, 'M': 500, 'threshold': 0.4},
}


def get_momentum_score(stock, period=29):
    try:
        prices = history_bars(stock, period, '1d', 'close')
        if prices is None or len(prices) < period:
            return None
        y = np.log(np.array(prices, dtype=float))
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        annualized = math.exp(slope * 250) - 1
        y_hat = slope * x + intercept
        ss_res = np.sum((y - y_hat) ** 2)
        ss_tot = (len(y) - 1) * np.var(y, ddof=1)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return annualized * r2
    except Exception:
        return None


def get_rsrs_signal(stock, N=18, M=700, threshold=0.7):
    """计算钝化RSRS信号"""
    try:
        total = N + M
        highs = history_bars(stock, total, '1d', 'high')
        lows = history_bars(stock, total, '1d', 'low')
        closes = history_bars(stock, total, '1d', 'close')
        if any(x is None for x in [highs, lows, closes]):
            return 'KEEP'

        h = np.array(highs, dtype=float)
        l = np.array(lows, dtype=float)
        c = np.array(closes, dtype=float)

        # 计算滚动beta序列
        betas = []
        r2s = []
        for i in range(M):
            hi = h[i:i+N]
            li = l[i:i+N]
            if np.std(li) == 0:
                continue
            slope, intercept = np.polyfit(li, hi, 1)
            y_hat = slope * li + intercept
            ss_res = np.sum((hi - y_hat) ** 2)
            ss_tot = (N - 1) * np.var(hi, ddof=1)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            betas.append(slope)
            r2s.append(r2)

        if len(betas) < 10:
            return 'KEEP'

        betas = np.array(betas)
        zscore = (betas[-1] - np.mean(betas)) / (np.std(betas) + 1e-10)

        # 收益率波动率分位数
        ret = np.diff(c) / c[:-1]
        ret_std_window = [np.std(ret[i:i+N]) for i in range(max(0, len(ret)-M), len(ret)-N+1)]
        if not ret_std_window:
            return 'KEEP'
        current_std = np.std(ret[-N:])
        quantile = np.sum(np.array(ret_std_window) <= current_std) / len(ret_std_window)

        rsrs_score = zscore * r2s[-1] ** (2 * quantile)

        if rsrs_score > threshold:
            return 'BUY'
        elif rsrs_score < -threshold:
            return 'SELL'
        return 'KEEP'
    except Exception:
        return 'KEEP'


def init(context):
    context.indices = list(ETF_MAP.keys())
    context.max_value = None
    context.last_value = None
    scheduler.run_daily(calculate_and_trade, time_rule=market_open(minute=0))
    scheduler.run_daily(calculate_and_trade, time_rule=market_open(minute=110))



def handle_bar(context, bar_dict):
    pass

def calculate_and_trade(context, bar_dict):
    # 动量选股
    scores = {}
    for idx in context.indices:
        score = get_momentum_score(idx)
        if score is not None:
            scores[idx] = score

    if not scores:
        return

    best_idx = max(scores, key=scores.get)
    signal = get_rsrs_signal(best_idx, **{k: v for k, v in RSRS_PARAMS[best_idx].items()})
    target_etf = ETF_MAP[best_idx]

    # 止损控制
    if context.max_value is None:
        context.max_value = context.portfolio.total_value
    if context.last_value is None:
        context.last_value = context.portfolio.total_value

    daily_change = context.portfolio.total_value / context.last_value - 1
    max_drawdown = context.portfolio.total_value / context.max_value - 1

    if daily_change < -0.02 or max_drawdown < -0.1:
        for code in list(context.portfolio.positions.keys()):
            order_target_value(code, 0)
        context.max_value = context.portfolio.total_value
        context.last_value = context.portfolio.total_value
        return

    context.last_value = context.portfolio.total_value
    if context.portfolio.total_value > context.max_value:
        context.max_value = context.portfolio.total_value

    if signal == 'SELL':
        for code in list(context.portfolio.positions.keys()):
            if code != CASH_ETF:
                order_target_value(code, 0)
        order_target_value(CASH_ETF, context.portfolio.total_value * 0.95)
    elif signal in ('BUY', 'KEEP'):
        held = list(context.portfolio.positions.keys())
        if target_etf not in held or len(held) == 0:
            for code in held:
                if code != target_etf:
                    order_target_value(code, 0)
            order_target_value(target_etf, context.portfolio.total_value * 0.95)
