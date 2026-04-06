# 韶华研究之七_基本面三角 - RiceQuant版本
# 逻辑：ROE+PB+净利润增速三角形评分，选三角形面积最大的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
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
            ['pb_ratio', 'market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['roe'] > 0.05]
        df = df[df['inc_net_profit_year_on_year'] > 0]
        candidates = df.index.tolist()
    except Exception:
        return
    def zscore(arr):
        s = np.std(arr)
        return (arr - np.mean(arr)) / s if s > 0 else np.zeros_like(arr)

    valid = df.index.tolist()
    if len(valid) < 5:
        return

    roe_z = zscore(df['roe'].values)
    pb_z = -zscore(df['pb_ratio'].values)
    growth_z = zscore(df['inc_net_profit_year_on_year'].values)

    scores = {}
    for i, stock in enumerate(valid):
        a, b, c = roe_z[i], pb_z[i], growth_z[i]
        if a > 0 and b > 0 and c > 0:
            scores[stock] = a * b * c
        else:
            scores[stock] = a * 0.4 + b * 0.3 + c * 0.3

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
