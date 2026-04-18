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


# 四年多翻9倍年化73成长因子评分筛选 - RiceQuant版本
# 逻辑：营收增速+净利润增速+ROE综合成长因子评分，月度调仓

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
            ['pe_ratio', 'market_cap', 'roe', 'gross_profit_margin', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pe_ratio'] > 0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['roe'] > 0.10]
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
    gpm_z = zscore(df['gross_profit_margin'].values)

    scores = {valid[i]: growth_z[i] * 0.4 + roe_z[i] * 0.35 + gpm_z[i] * 0.25
              for i in range(len(valid))}

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
