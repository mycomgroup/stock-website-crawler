# 三因子策略 - RiceQuant版本
# 逻辑：市场因子(大盘MA择时) + 规模因子(小市值) + 价值因子(低PB)，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1
    context.index = '000300.XSHG'


def handle_bar(context, bar_dict):
    closes = history_bars(context.index, 60, '1d', 'close')
    if closes is None or len(closes) < 60:
        return
    closes = np.array(closes, dtype=float)
    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:])
    bull = closes[-1] > ma20 and ma20 > ma60

    current_month = context.now.month
    if current_month == context.month:
        if not bull and context.portfolio.positions:
            for stock in list(context.portfolio.positions.keys()):
                order_target_value(stock, 0)
        return

    if not bull:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 3.0]
        df = df[df['market_cap'] > 3e+08]
        df = df[df['market_cap'] < 1e+10]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = [s for s in candidates if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
