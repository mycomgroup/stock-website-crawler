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


# 基本面三角3.0策略 - RiceQuant版本
# 逻辑：ROE+PB+净利润增速三角形评分3.0版，加入大盘择时，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1
    context.index = '000300.XSHG'


def handle_bar(context, bar_dict):
    # 大盘择时
    idx_closes = history_bars(context.index, 60, '1d', 'close')
    if idx_closes is None or len(idx_closes) < 60:
        return
    idx_closes = np.array(idx_closes, dtype=float)
    ma20 = np.mean(idx_closes[-20:])
    ma60 = np.mean(idx_closes[-60:])
    if idx_closes[-1] < ma20 and ma20 < ma60:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

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
            ['pb_ratio', 'market_cap', 'roe', 'gross_profit_margin', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 5e+10]
        df = df[df['roe'] > 0.08]
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

    roe_z = zscore(df['roe'].values)
    pb_z = -zscore(df['pb_ratio'].values)
    growth_z = zscore(df['inc_net_profit_year_on_year'].values)
    gpm_z = zscore(df['gross_profit_margin'].values)

    scores = {}
    for i, stock in enumerate(valid):
        a, b, c = roe_z[i], pb_z[i], growth_z[i]
        # 三角形面积：三因子均正时乘积最大
        if a > 0 and b > 0 and c > 0:
            scores[stock] = a * b * c + gpm_z[i] * 0.1
        else:
            scores[stock] = a * 0.35 + b * 0.3 + c * 0.25 + gpm_z[i] * 0.1

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
