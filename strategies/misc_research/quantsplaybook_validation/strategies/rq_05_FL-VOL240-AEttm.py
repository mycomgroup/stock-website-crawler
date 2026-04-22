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


# FL-VOL240-AEttm 多因子策略 - RiceQuant版本
# 因子：低财务杠杆(FL) + 低240日波动率(VOL240) + 高资产效率ROA(AEttm)
# 逻辑：选低杠杆、低波动、高ROA的防御性优质股，月度调仓

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
            ['market_cap', 'pb_ratio', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 4.0]
        df = df[df['market_cap'] > 20]
        df = df[df['roa'] > 0.05]
        df = df.sort_values(['roa', 'pb_ratio'], ascending=[False, True]).head(context.stock_num * 10)
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 60, '1d', 'close')
            if closes is None or len(closes) < 60:
                continue
            closes = np.array(closes, dtype=float)
            returns = np.diff(closes) / closes[:-1]
            vol = np.std(returns)
            roa = df.loc[stock, 'roa'] if stock in df.index else 0
            pb = df.loc[stock, 'pb_ratio'] if stock in df.index else 5
            scores[stock] = -vol * 0.4 + (roa / 100) * 0.4 - (pb / 10) * 0.2
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
