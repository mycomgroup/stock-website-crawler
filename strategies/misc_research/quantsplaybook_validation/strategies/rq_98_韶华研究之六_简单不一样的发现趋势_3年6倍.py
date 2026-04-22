# 韶华研究之六_发现趋势策略 - RiceQuant版本
# 逻辑：用线性回归斜率发现上升趋势，选斜率最大且R²>0.7的股票，月度调仓

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


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 2e+09]
        df = df[df['market_cap'] < 5e+10]
        df = df[df['pb_ratio'] > 0.0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 30, '1d', 'close')
            if closes is None or len(closes) < 30:
                continue
            closes = np.array(closes, dtype=float)
            # 对数价格线性回归
            y = np.log(closes)
            x = np.arange(len(y))
            beta, r2 = _ols_beta_r2(x, y)
            if beta is None:
                continue
            if beta > 0 and r2 > 0.7:
                annualized = np.exp(beta * 250) - 1
                result.append((stock, annualized * r2))
        except Exception:
            continue

    candidates.sort(key=lambda x: x[1], reverse=True)
    target = [s for s, _ in candidates if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
