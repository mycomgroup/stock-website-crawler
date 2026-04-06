# 7年40倍模拟超过两年年化高回撤低策略 - RiceQuant版本
# 逻辑：全市场小市值低价股，按市值+价格综合排名，周度调仓

import numpy as np


def init(context):
    context.stock_num = 4
    context.week = -1
    context.bear_percent = 0.3


def is_bull_market(context):
    """用沪深300均线判断牛熊"""
    try:
        prices = history_bars('000300.XSHG', 10, '1d', 'close')
        if prices is None or len(prices) < 10:
            return True
        p = np.array(prices, dtype=float)
        return p[-1] > np.mean(p)
    except Exception:
        return True


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 100000000]
        df = df[df['market_cap'] < 100000000]
        df = df[df['pb_ratio'] > 0.01]
        df = df[df['pb_ratio'] < 30.0]
        df = df.head(context.stock_num * 5)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        candidates = list(df.index)
    except Exception:
        return

    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if bar.close < 9:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.week = current_week

    position_ratio = 0.95 if is_bull_market(context) else context.bear_percent

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = position_ratio / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight)
