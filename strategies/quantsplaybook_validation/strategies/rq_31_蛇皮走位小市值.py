# 蛇皮走位小市值策略 - RiceQuant版本
# 逻辑：选中小板小市值+ROE高的股票，市场一致性信号控制买卖

import numpy as np


def init(context):
    context.stock_num = 10
    context.week = -1


def get_target_stocks(context, bar_dict):
    try:
        all_stocks = all_instruments('CS')['order_book_id'].tolist()
        stocks = [s for s in all_stocks
                  if not s.startswith(('688', '4', '8'))]
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        if df is None or len(df) == 0:
            return []
        df =         df = df[(df['roe'] > 0.15) & (df['roa'] > 0.1) & (df['market_cap'] > 0)]
        df = df.sort_values('market_cap', ascending=True)
        candidates = df.index.tolist()[:context.stock_num * 3]
    except Exception:
        return []

    target = []
    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break
    return target


def market_consistent(context):
    """检查市场一致性：近5日涨跌幅方差小且均值为正"""
    try:
        prices_20 = history_bars('000001.XSHG', 20, '1d', 'close')
        if prices_20 is None or len(prices_20) < 20:
            return True
        p = np.array(prices_20, dtype=float)
        returns = np.diff(p) / p[:-1]
        recent = returns[-5:]
        return np.mean(recent) > 0 and np.var(recent) < 0.0004
    except Exception:
        return True


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    target = get_target_stocks(context, bar_dict)

    if not market_consistent(context):
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    if not target:
        return

    context.week = current_week

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
