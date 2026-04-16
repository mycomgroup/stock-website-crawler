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


# PEG+EBIT+市值+换手率因子策略 - RiceQuant版本
# 逻辑：低PEG + 高ROE(EBIT代理) + 小市值 + 低换手率波动，月度调仓

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
            ['market_cap', 'pe_ratio', 'roe', 'inc_net_profit_year_on_year', 'peg_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 60.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['roe'] > 0.08]
        df = df[df['inc_net_profit_year_on_year'] > 0.05]
        df = df[df['inc_net_profit_year_on_year'] > 0]
        df = df[df['peg_ratio'] > 0]
        candidates = df.index.tolist()
    except Exception:
        return
    # 换手率稳定性因子
    scores = {}
    for stock in candidates[:context.stock_num * 3]:
        try:
            volumes = history_bars(stock, 20, '1d', 'volume')
            if volumes is None or len(volumes) < 20:
                continue
            volumes = np.array(volumes, dtype=float)
            vol_cv = np.std(volumes) / (np.mean(volumes) + 1e-10)
            peg = float(df.at[stock, 'peg_ratio']) if stock in df.index else 99
            roe = float(df.at[stock, 'roe']) if stock in df.index else 0
            scores[stock] = -peg * 0.4 + (roe / 100) * 0.4 - vol_cv * 0.2
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
