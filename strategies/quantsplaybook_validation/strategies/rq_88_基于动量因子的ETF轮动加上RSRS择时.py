# 风险及免责提示：该策略由聚宽用户分享，仅供学习交流使用。
# 克隆自聚宽文章：https://www.joinquant.com/post/26142
# 标题：基于动量因子的ETF轮动加上RSRS择时
# 作者：慕长风
# RiceQuant 移植说明：
#   history_bars() → history_bars()
#   get_index_stocks() → index_components()（本策略未使用）
#   RSRS 逻辑参考已验证的 05_rsrs_optimized.py

import numpy as np


def ols_beta_r2(x, y):
    x_mean, y_mean = np.mean(x), np.mean(y)
    ss_xx = np.sum((x - x_mean) ** 2)
    if ss_xx == 0:
        return None, None
    beta = np.sum((x - x_mean) * (y - y_mean)) / ss_xx
    alpha = y_mean - beta * x_mean
    y_hat = alpha + beta * x
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2


def bootstrap_rsrs_history(ref, n, m):
    highs = history_bars(ref, n + m, '1d', 'high')
    lows = history_bars(ref, n + m, '1d', 'low')
    if highs is None or lows is None or len(highs) < n + m or len(lows) < n + m:
        return [], []
    beta_history = []
    r2_history = []
    for i in range(m):
        h = np.array(highs[i:i + n], dtype=float)
        l = np.array(lows[i:i + n], dtype=float)
        beta, r2 = ols_beta_r2(l, h)
        if beta is None:
            continue
        beta_history.append(beta)
        r2_history.append(r2)
    return beta_history, r2_history


def init(context):

    context.index_pool = [
        ('000016.XSHG', '510050.XSHG'),
        ('000300.XSHG', '510300.XSHG'),
        ('399905.XSHE', '510500.XSHG'),
        ('399006.XSHE', '159915.XSHE'),
        ('000015.XSHG', '510880.XSHG'),
        ('399932.XSHE', '159928.XSHE'),
        ('399913.XSHE', '512010.XSHG'),
    ]
    context.stock_num = 2
    context.momentum_day = 15
    context.stock = '000300.XSHG'  # RSRS 择时标的
    context.N = 18                 # RSRS 回归窗口
    context.M = 200                # RSRS 标准分窗口
    context.score_threshold = 0.7
    context.beta_history = []
    context.r2_history = []

    scheduler.run_weekly(trade, weekday=3, time_rule=market_open(minute=30))



def handle_bar(context, bar_dict):
    pass

def get_rsrs_score(context):
    """计算 RSRS 右偏标准分"""
    if not context.beta_history:
        context.beta_history, context.r2_history = bootstrap_rsrs_history(context.stock, context.N, context.M)
    highs = history_bars(context.stock, context.N + 1, '1d', 'high')
    lows  = history_bars(context.stock, context.N + 1, '1d', 'low')
    if highs is None or lows is None or len(highs) < context.N:
        return None
    h = np.array(highs[-context.N:], dtype=float)
    l = np.array(lows[-context.N:], dtype=float)
    beta, r2 = ols_beta_r2(l, h)
    if beta is None:
        return None
    context.beta_history.append(beta)
    context.r2_history.append(r2)
    if len(context.beta_history) > context.M:
        context.beta_history = context.beta_history[-context.M:]
        context.r2_history   = context.r2_history[-context.M:]
    if len(context.beta_history) < context.M:
        return None
    beta_arr = np.array(context.beta_history)
    sigma = np.std(beta_arr)
    if sigma == 0:
        return None
    z = (beta - np.mean(beta_arr)) / sigma
    return z * beta * r2  # 右偏标准分


def trade(context, bar_dict):
    rsrs = get_rsrs_score(context)
    # RSRS 未就绪时不操作
    if rsrs is None:
        return

    # RSRS 低于阈值：清仓
    if rsrs < -context.score_threshold:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        print(f"[RSRS] 空仓信号 rsrs={rsrs:.3f}")
        return

    # RSRS 高于阈值：动量选 ETF
    if rsrs > context.score_threshold:
        scores = {}
        for _, etf in context.index_pool:
            prices = history_bars(etf, context.momentum_day + 1, '1d', 'close')
            if prices is None or len(prices) < context.momentum_day + 1:
                continue
            p = np.array(prices, dtype=float)
            momentum = p[-1] / p[0] - 1
            scores[etf] = momentum

        if not scores:
            return

        target = sorted(scores, key=scores.get, reverse=True)[:context.stock_num]

        for stock in list(context.portfolio.positions.keys()):
            if stock not in target:
                order_target_value(stock, 0)

        if not target:
            return
        weight = 1.0 / len(target)
        for etf in target:
            order_target_value(etf, context.portfolio.total_value * weight * 0.95)
        print(f"[RSRS] 买入信号 rsrs={rsrs:.3f} target={target}")
