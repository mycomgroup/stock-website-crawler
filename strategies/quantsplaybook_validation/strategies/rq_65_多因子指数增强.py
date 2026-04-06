# 多因子指数增强策略 - RiceQuant版本
# 原文：多因子指数增强
# 逻辑：在中证500成分股中，用成长（净利润增速）、质量（ROE）、价值（PB）、动量多因子做指数增强

import numpy as np


def init(context):
    context.index = '000905.XSHG'
    context.stock_num = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components(context.index)
    if not stocks or len(stocks) < 10:
        return

    context.month = current_month

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pb_ratio', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        candidates = df.index.tolist()
    except Exception:
        return
    # 动量因子
    momentum = {}
    for stock in df.index:
        try:
            closes = history_bars(stock, 61, '1d', 'close')
            if closes is not None and len(closes) >= 61:
                momentum[stock] = closes[-1] / closes[0] - 1
        except Exception:
            pass

    valid = [s for s in df.index if s in momentum]
    if len(valid) < 5:
        return

    # z-score标准化各因子
    def zscore(vals):
        arr = np.array(vals, dtype=float)
        std = np.std(arr)
        return (arr - np.mean(arr)) / std if std > 0 else np.zeros_like(arr)

    mom_z = zscore([momentum[s] for s in valid])
    roe_z = zscore([df.loc[s, 'roe'] if 'roe' in df.columns else 0 for s in valid])
    pb_z = zscore([df.loc[s, 'pb_ratio'] if 'pb_ratio' in df.columns else 5 for s in valid])
    growth_z = zscore([df.loc[s, 'inc_net_profit_year_on_year'] if 'inc_net_profit_year_on_year' in df.columns else 0 for s in valid])

    scores = {valid[i]: mom_z[i] * 0.25 + roe_z[i] * 0.35 - pb_z[i] * 0.15 + growth_z[i] * 0.25
              for i in range(len(valid))}

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = []
    for stock in sorted_stocks:
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
