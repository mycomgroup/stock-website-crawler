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


# NCAR-AER-ATR6-VOL20 多因子策略 - RiceQuant版本
# 因子：净现金资产比(NCAR/ROA代理) + 资产效率(AER/ROA) + 6月动量(ATR6) + 低20日波动(VOL20)
# 逻辑：选高ROA、低波动、6个月动量强的股票，月度调仓

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
            ['market_cap', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[df['market_cap'] > 10]
        df = df[df['roa'] > 0.04]
        df = df.sort_values(['roa', 'market_cap'], ascending=[False, True]).head(context.stock_num * 10)
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 130, '1d', 'close')
            if closes is None or len(closes) < 130:
                continue
            closes = np.array(closes, dtype=float)
            atr6 = closes[-1] / closes[-126] - 1
            returns = np.diff(closes[-21:]) / closes[-21:-1]
            vol20 = np.std(returns)
            roa = df.loc[stock, 'roa'] if stock in df.index else 0
            scores[stock] = atr6 * 0.35 - vol20 * 0.3 + (roa / 100) * 0.35
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
