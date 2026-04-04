# 成交额加权回归钝化 RSRS 择时策略 - RiceQuant 标准回测版本
# 候选3: 成交额加权回归 + 钝化 RSRS (V11)
# 构造: 成交额加权WLS回归计算 beta + 钝化公式
# 参数: N=19, M=500, 阈值=0.8
# 标的: 沪深300 (000300.XSHG)
# 修复：从 notebook 脚本格式改为 RiceQuant 标准 init/handle_bar 格式

import numpy as np
import statsmodels.api as sm


def init(context):
    context.security = '000300.XSHG'
    context.N = 19          # 回归窗口
    context.M = 500         # 标准分窗口
    context.BUY_THRESHOLD = 0.8
    context.SELL_THRESHOLD = -0.8

    # 历史数据缓存
    context.beta_history = []
    context.r2_history = []
    context.return_history = []
    context.prev_close = None
    context.in_market = False


def handle_bar(context, bar_dict):
    bar = bar_dict[context.security]
    close = bar.close

    # 更新收益率历史
    if context.prev_close is not None and context.prev_close > 0:
        ret = (close - context.prev_close) / context.prev_close
        context.return_history.append(ret)
    context.prev_close = close

    # 获取历史高低价和成交量
    highs = history_bars(context.security, context.N + 1, '1d', 'high')
    lows = history_bars(context.security, context.N + 1, '1d', 'low')
    closes = history_bars(context.security, context.N + 1, '1d', 'close')
    volumes = history_bars(context.security, context.N + 1, '1d', 'volume')

    if any(x is None for x in [highs, lows, closes, volumes]):
        return
    if len(highs) < context.N:
        return

    h = np.array(highs[-context.N:], dtype=float)
    l = np.array(lows[-context.N:], dtype=float)
    c = np.array(closes[-context.N:], dtype=float)
    v = np.array(volumes[-context.N:], dtype=float)

    # 成交额 = volume * close
    turnover = v * c
    total_turnover = np.sum(turnover)
    if total_turnover > 0:
        weights = turnover / total_turnover
    else:
        weights = np.ones(context.N) / context.N

    X = sm.add_constant(l)
    try:
        model = sm.WLS(h, X, weights=weights).fit()
        beta = model.params[1]
        r2 = model.rsquared
    except Exception:
        return

    context.beta_history.append(beta)
    context.r2_history.append(r2)

    # 需要足够历史数据
    if len(context.beta_history) < context.M:
        return

    beta_window = np.array(context.beta_history[-context.M:])
    mu = np.mean(beta_window)
    sigma = np.std(beta_window)
    if sigma == 0:
        return

    z = (beta - mu) / sigma

    # 计算收益率波动率分位数
    if len(context.return_history) < context.N:
        return

    ret_arr = np.array(context.return_history)
    ret_std_window = []
    start = max(0, len(ret_arr) - context.M)
    for i in range(start, len(ret_arr) - context.N + 1):
        s = np.std(ret_arr[i:i + context.N])
        ret_std_window.append(s)

    if len(ret_std_window) == 0:
        return

    current_std = np.std(ret_arr[-context.N:])
    quantile = np.sum(np.array(ret_std_window) <= current_std) / len(ret_std_window)

    # 钝化 RSRS 指标
    rsrs_dampened = z * r2 * quantile

    # 交易逻辑
    if rsrs_dampened > context.BUY_THRESHOLD and not context.in_market:
        order_target_percent(context.security, 0.95)
        context.in_market = True
    elif rsrs_dampened < context.SELL_THRESHOLD and context.in_market:
        order_target_percent(context.security, 0)
        context.in_market = False
