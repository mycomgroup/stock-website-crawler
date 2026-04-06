# 全新因子方法超稳定策略 - RiceQuant版本
# 逻辑：综合ROE、PB、动量、市值的多因子z-score评分，月度调仓20只

import numpy as np


def init(context):
    context.stock_num = 20
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
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 5e+08]
        df = df[df['market_cap'] < 2e+10]
        df = df[df['roe'] > 0.05]
        candidates = df.index.tolist()
    except Exception:
        return
    def zscore(arr):
        s = np.std(arr)
        return (arr - np.mean(arr)) / s if s > 0 else np.zeros_like(arr)

    momentum = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is not None and len(closes) >= 21:
                momentum[stock] = closes[-1] / closes[0] - 1
        except Exception:
            pass

    valid = [s for s in candidates if s in momentum]
    if len(valid) < 5:
        return

    mom_z = zscore(np.array([momentum[s] for s in valid]))
    roe_z = zscore(np.array([df.loc[s, 'roe'] if s in df.index else 0 for s in valid]))
    pb_z = zscore(np.array([df.loc[s, 'pb_ratio'] if s in df.index else 5 for s in valid]))
    growth_z = zscore(np.array([df.loc[s, 'inc_net_profit_year_on_year'] if s in df.index else 0 for s in valid]))

    scores = {valid[i]: mom_z[i] * 0.25 + roe_z[i] * 0.35 - pb_z[i] * 0.15 + growth_z[i] * 0.25
              for i in range(len(valid))}

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
