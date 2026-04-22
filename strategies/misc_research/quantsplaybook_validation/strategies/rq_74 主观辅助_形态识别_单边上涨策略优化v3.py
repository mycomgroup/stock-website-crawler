# 形态识别_单边上涨策略优化v3 - RiceQuant版本
# 原文：形态识别_单边上涨v3
# 逻辑：识别单边上涨形态（连续N日收盘价高于均线且均线向上），选强势股

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
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

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

            # 单边上涨形态：用线性回归斜率判断
            x = np.arange(len(closes))
            beta, r2 = _ols_beta_r2(x, closes / closes[0])
            if beta is None:
                continue
            slope = beta

            # 斜率为正且R²高（线性上涨）
            if slope > 0 and r2 > 0.7:
                # 当前价格在20日均线上方
                ma20 = np.mean(closes[-20:])
                if closes[-1] > ma20:
                    result.append((stock, slope * r2))
        except Exception:
            continue

    candidates.sort(key=lambda x: x[1], reverse=True)
    target = []
    for stock, _ in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
