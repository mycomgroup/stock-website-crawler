# 穿越牛熊稳健高收益策略 - RiceQuant版本
# 原文：14年初到23年7月，年化37，夏普1.25，稳健高收益！
# 作者：侧耳闻鹿鸣
# 原文：https://www.joinquant.com/post/43194
# 逻辑：全市场选ROE>4%、PB低的股票，短均线>长均线时持仓，周度调仓

import numpy as np


def init(context):
    context.week = -1


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return
    context.week = current_week

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 5.0]
        df = df[df['roe'] > 0.04]
        df = df.head(200)
        candidates = df.index.tolist()
        if df is None or len(df) == 0:
            return
        candidates = df.index.tolist()
    except Exception:
        return

    # 短均线 > 长均线（20日 > 100日）
    buy = []
    for stock in candidates:
        try:
            prices = history_bars(stock, 100, '1d', 'close')
            if prices is None or len(prices) < 100:
                continue
            p = np.array(prices, dtype=float)
            if np.mean(p[-20:]) > np.mean(p):
                buy.append(stock)
        except Exception:
            continue

    for stock in list(context.portfolio.positions.keys()):
        if stock not in buy:
            order_target_value(stock, 0)

    if not buy:
        return

    cash_per = context.portfolio.cash / len(buy)
    for stock in buy:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if stock not in context.portfolio.positions:
            order_target_value(stock, cash_per)
