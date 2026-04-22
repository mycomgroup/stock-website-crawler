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


# 均线黏合突破选股法 - RiceQuant版本
# 原文：均线黏合，突破前三十个交易日最高点选股法
# 逻辑：选均线黏合（MA5/MA10/MA20接近）且价格突破近30日高点的股票

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]
    factor_df = get_factor(
        stocks,
        ['market_cap']
    )
    if factor_df is None or factor_df.empty:
        return
    df = _normalize_factor_frame(factor_df)
    if not hasattr(df, 'columns'):
        df = df.to_frame(name='market_cap')
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 50000000000]
    df = df.sort_values('market_cap').head(200)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 35, '1d', 'close')
            if closes is None or len(closes) < 30:
                continue
            closes = np.array(closes, dtype=float)

            ma5 = np.mean(closes[-5:])
            ma10 = np.mean(closes[-10:])
            ma20 = np.mean(closes[-20:])
            cur = closes[-1]

            # 均线黏合：三条均线最大差距 < 3%
            ma_max = max(ma5, ma10, ma20)
            ma_min = min(ma5, ma10, ma20)
            if ma_min == 0:
                continue
            adhesion = (ma_max - ma_min) / ma_min

            # 突破近30日高点
            high_30 = np.max(closes[-31:-1])
            breakout = cur > high_30

            if adhesion < 0.03 and breakout:
                result.append(stock)
        except Exception:
            continue

    target = []
    for stock in result:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return
    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
