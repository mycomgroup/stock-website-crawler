# 持续跑赢大盘_真蓝筹v2 - RiceQuant版本
# 逻辑：大市值蓝筹 + RSRS择时 + 低PB高ROE，适合大资金，季度调仓

import numpy as np

def _ols_beta_r2(x, y):
    """Pure numpy OLS: returns (beta, r2)"""
    xm, ym = x.mean(), y.mean()
    ss_xx = ((x - xm) ** 2).sum()
    if ss_xx == 0:
        return None, None
    beta = ((x - xm) * (y - ym)).sum() / ss_xx
    y_hat = ym + beta * (x - xm)
    ss_res = ((y - y_hat) ** 2).sum()
    ss_tot = ((y - ym) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2



def _bootstrap_rsrs_history(ref, n, m):
    highs = history_bars(ref, n + m, '1d', 'high')
    lows = history_bars(ref, n + m, '1d', 'low')
    if highs is None or lows is None or len(highs) < n + m or len(lows) < n + m:
        return [], []
    beta_history = []
    r2_history = []
    for i in range(m):
        h = np.array(highs[i:i + n], dtype=float)
        l = np.array(lows[i:i + n], dtype=float)
        beta, r2 = _ols_beta_r2(l, h)
        if beta is None:
            continue
        beta_history.append(beta)
        r2_history.append(r2)
    return beta_history, r2_history


def init(context):
    context.stock_num = 20
    context.quarter = -1
    context.N = 18
    context.M = 300
    context.ref = '000300.XSHG'
    context.beta_history = []
    context.r2_history = []
    context.in_market = False


def handle_bar(context, bar_dict):
    if not context.beta_history:
        context.beta_history, context.r2_history = _bootstrap_rsrs_history(context.ref, context.N, context.M)
    highs = history_bars(context.ref, context.N + 1, '1d', 'high')
    lows = history_bars(context.ref, context.N + 1, '1d', 'low')
    if highs is None or lows is None or len(highs) < context.N:
        return

    h = np.array(highs[-context.N:], dtype=float)
    l = np.array(lows[-context.N:], dtype=float)
    beta, r2 = _ols_beta_r2(l, h)
    if beta is None:
        return
    context.beta_history.append(beta)
    context.r2_history.append(r2)

    if len(context.beta_history) > context.M:
        context.beta_history = context.beta_history[-context.M:]
        context.r2_history = context.r2_history[-context.M:]

    if len(context.beta_history) < context.M:
        return

    beta_arr = np.array(context.beta_history)
    mu, sigma = np.mean(beta_arr), np.std(beta_arr)
    if sigma == 0:
        return
    rsrs = (beta_arr[-1] - mu) / sigma * beta_arr[-1] * context.r2_history[-1]

    if rsrs < -0.7 and context.in_market:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        context.in_market = False
        return

    if rsrs < 0.7:
        return

    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        return
    context.quarter = current_quarter

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 5e+10]
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 4.0]
        df = df[df['roe'] > 0.12]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = [s for s in candidates if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
    context.in_market = True
