# 多个成长因子评分策略 - RiceQuant版本
# 逻辑：净利润增速+营收增速+ROE+EPS综合评分，月度调仓20只

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe', 'inc_net_profit_year_on_year', 'eps', 'gross_profit_margin'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 1e9]   # NOTE: RQ market_cap is yuan (元), JQ was 亿
        df = df[df['market_cap'] < 5e10]
        df = df[df['roe'] > 0.05]          # NOTE: RQ roe is decimal, JQ was percent
        df = df[df['inc_net_profit_year_on_year'] > 0.05]
        candidates = df.index.tolist()
    except Exception:
        return
    def zscore(arr):
        s = np.std(arr)
        return (arr - np.mean(arr)) / s if s > 0 else np.zeros_like(arr)

    valid = df.index.tolist()
    if len(valid) < 5:
        return

    growth_z = zscore(df['inc_net_profit_year_on_year'].values)
    roe_z = zscore(df['roe'].values)
    eps_z = zscore(df['eps'].values)
    gpm_z = zscore(df['gross_profit_margin'].values)

    scores = {valid[i]: growth_z[i] * 0.35 + roe_z[i] * 0.3 + eps_z[i] * 0.2 + gpm_z[i] * 0.15
              for i in range(len(valid))}

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
