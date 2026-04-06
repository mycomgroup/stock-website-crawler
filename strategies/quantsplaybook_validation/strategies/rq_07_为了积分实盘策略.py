# 为了挣点积分自己实盘的策略 - RiceQuant版本
# 原文：为了挣点积分自己实盘的策略分享出来
# 原文：https://www.joinquant.com/post/43194
# 逻辑：全市场选股，ROE>4%，PB低，净利润增长高，短均线>长均线买入

import numpy as np


def init(context):
    context.week = -1
    context.stock_num = 10


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    instruments_df = all_instruments('CS')
    instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]
    factor_df = get_factor(
        stocks,
        ['pb_ratio', 'roe', 'inc_net_profit_year_on_year']
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=-1).last().dropna()
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 5.0]
    df = df[df['roe'] > 0.04]
    df = df[df['inc_net_profit_year_on_year'] > 0.0]
    if df is None or len(df) == 0:
        return
    df = df.sort_values(['inc_net_profit_year_on_year', 'roe', 'pb_ratio'], ascending=[False, False, True]).head(50)
    candidates = list(df.index)
    # 短均线 > 长均线过滤
    buy = []
    for stock in candidates:
        try:
            prices = history_bars(stock, 120, '1d', 'close')
            if prices is None or len(prices) < 120:
                continue
            p = np.array(prices, dtype=float)
            ma20 = np.mean(p[-20:])
            ma100 = np.mean(p[-100:])
            if ma20 > ma100:
                buy.append(stock)
        except Exception:
            continue

    if not buy:
        return
    target = buy[:context.stock_num]
    if not target:
        return

    context.week = current_week

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
