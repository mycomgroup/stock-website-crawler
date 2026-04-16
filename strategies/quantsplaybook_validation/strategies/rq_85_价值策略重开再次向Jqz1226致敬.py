def _normalize_factor_frame(factor_df):
    if factor_df is None:
        return None
    try:
        if hasattr(factor_df, 'empty') and factor_df.empty:
            return factor_df
        if not hasattr(factor_df, 'columns'):
            factor_df = factor_df.to_frame()
        index = getattr(factor_df, 'index', None)
        if index is not None and getattr(index, 'nlevels', 1) > 1:
            factor_df = factor_df.groupby(level=-1).last()
        return factor_df.dropna()
    except Exception:
        return None


# 价值策略重开，再次向Jqz1226致敬 - RiceQuant版本
# 原文：价值策略重开，再次向Jqz1226致敬
# 逻辑：RSRS择时 + 价值选股（低PB、高ROE），大盘弱势时持债券ETF

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
    context.security = '000300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.stock_num = 10
    context.N = 18
    context.M = 300
    context.buy_threshold = 0.7
    context.sell_threshold = -0.7
    context.month = -1
    context.beta_history = []
    context.r2_history = []
    context.in_stock = False


def handle_bar(context, bar_dict):
    if not context.beta_history:
        context.beta_history, context.r2_history = _bootstrap_rsrs_history(context.security, context.N, context.M)
    # RSRS择时
    highs = history_bars(context.security, context.N + 1, '1d', 'high')
    lows = history_bars(context.security, context.N + 1, '1d', 'low')
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
    zscore = (beta_arr[-1] - mu) / sigma
    rsrs = zscore * beta_arr[-1] * context.r2_history[-1]

    # 月度选股
    current_month = context.now.month
    if rsrs > context.buy_threshold:
        if current_month != context.month:
            if rebalance_stocks(context, bar_dict):
                context.month = current_month
        context.in_stock = True
    elif rsrs < context.sell_threshold:
        for stock in list(context.portfolio.positions.keys()):
            if stock != context.bond_etf:
                order_target_value(stock, 0)
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is None or bar.is_trading:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        context.in_stock = False
    elif not context.in_stock:
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is None or bar.is_trading:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)


def rebalance_stocks(context, bar_dict):
    # 清仓债券ETF
    if context.bond_etf in context.portfolio.positions:
        order_target_value(context.bond_etf, 0)

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return False
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return False
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 4.0]
        df = df[df['market_cap'] > 3e+09]
        df = df[df['roe'] > 0.10]
        df = df.sort_values(['pb_ratio', 'roe'], ascending=[True, False]).head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return False
    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return False

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
    return True
