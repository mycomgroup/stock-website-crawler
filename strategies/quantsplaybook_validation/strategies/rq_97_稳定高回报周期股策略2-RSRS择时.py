# 稳定高回报周期股策略2+RSRS择时 - RiceQuant版本
# 逻辑：选周期行业（能源、材料、工业）中低PB高股息的股票，RSRS择时

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



def init(context):
    context.stock_num = 15
    context.month = -1
    context.N = 18
    context.M = 200
    context.beta_history = []
    context.r2_history = []
    context.ref = '000300.XSHG'
    context.in_market = False
    # 周期行业指数（能源+材料+工业）
    context.cycle_indices = ['399975.XSHE', '399976.XSHE']  # 中证能源、中证材料


def handle_bar(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    # RSRS择时
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

    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    # 获取周期股票池
    pool = []
    for idx in context.cycle_indices:
        try:
            comps = index_components(idx)
            if comps:
                pool.extend(comps)
        except Exception:
            pass

    if not pool:
        instruments_df = all_instruments('CS')
        pool = [s for s in stock_ids
                if not s.startswith(('688', '4', '8'))][:500]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stock_ids,
            ['market_cap', 'pb_ratio', 'dividend_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 3.0]
        df = df[df['market_cap'] > 5e+09]
        df = df[df['dividend_ratio'] > 0.010]
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
