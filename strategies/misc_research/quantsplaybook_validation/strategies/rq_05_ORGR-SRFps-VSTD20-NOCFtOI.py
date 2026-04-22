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


# ORGR-SRFps-VSTD20-NOCFtOI 多因子策略 - RiceQuant版本
# 因子：营收增速(ORGR) + EPS(SRFps) + 成交量稳定性(VSTD20) + 现金流质量(NOCFtOI)
# 逻辑：选营收增速高、EPS高、成交量稳定的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8'))]

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'inc_net_profit_year_on_year', 'eps'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['market_cap'] > 10]
        df = df[df['inc_net_profit_year_on_year'] > 0.1]
        df = df.sort_values(['inc_net_profit_year_on_year', 'eps'], ascending=[False, False]).head(context.stock_num * 10)
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            volumes = history_bars(stock, 20, '1d', 'volume')
            if volumes is None or len(volumes) < 20:
                continue
            volumes = np.array(volumes, dtype=float)
            vstd20 = np.std(volumes) / (np.mean(volumes) + 1e-10)
            eps = df.loc[stock, 'eps'] if stock in df.index else 0
            growth = df.loc[stock, 'inc_net_profit_year_on_year'] if stock in df.index else 0
            scores[stock] = (growth / 100) * 0.4 + (eps / 5) * 0.4 - vstd20 * 0.2
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]
    if not target:
        target = sorted_stocks[:context.stock_num]

    if not target:
        return
    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
