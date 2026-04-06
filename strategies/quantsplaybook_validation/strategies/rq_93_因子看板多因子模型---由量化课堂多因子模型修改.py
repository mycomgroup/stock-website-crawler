# 多因子模型策略 - RiceQuant版本
# 原文：因子看板多因子模型---由量化课堂多因子模型修改
# 逻辑：综合成长（净利润增速）、质量（ROE）、价值（PB）、动量多因子选股

import numpy as np


def init(context):
    context.N = 30          # 持仓数量
    context.tc = 30         # 调仓周期（天）
    context.day_count = 0
    # before_trading_start不支持，选股逻辑已移入handle_bar


def handle_bar(context, bar_dict):
    context.day_count += 1
    if context.day_count % context.tc != 0:
        return

    stocks = index_components('000905.XSHG')
    if not stocks or len(stocks) < 10:
        return

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pb_ratio', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['roe'] > 0.00]
        candidates = df.index.tolist()
    except Exception:
        return
    # 动量因子
    momentum = {}
    for stock in df.index:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is not None and len(closes) >= 21:
                momentum[stock] = closes[-1] / closes[0] - 1
        except Exception:
            pass

    # 综合评分（z-score标准化）
    def zscore(vals):
        arr = np.array(vals, dtype=float)
        std = np.std(arr)
        if std == 0:
            return np.zeros_like(arr)
        return (arr - np.mean(arr)) / std

    valid = [s for s in df.index if s in momentum]
    if len(valid) < 5:
        return

    mom_vals = zscore([momentum[s] for s in valid])
    roe_vals = zscore([df.loc[s, 'roe'] if 'roe' in df.columns else 0 for s in valid])
    pb_vals = zscore([df.loc[s, 'pb_ratio'] if 'pb_ratio' in df.columns else 5 for s in valid])
    growth_vals = zscore([df.loc[s, 'inc_net_profit_year_on_year'] if 'inc_net_profit_year_on_year' in df.columns else 0 for s in valid])

    scores = {}
    for i, stock in enumerate(valid):
        scores[stock] = mom_vals[i] * 0.25 + roe_vals[i] * 0.35 - pb_vals[i] * 0.15 + growth_vals[i] * 0.25

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = []
    for stock in sorted_stocks:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.N:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


# before_trading_start removed (not supported in RQ)

