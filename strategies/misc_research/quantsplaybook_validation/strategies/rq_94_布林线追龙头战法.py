# 布林线追龙头战法 - RiceQuant版本
# 原文：布林线追龙头战法
# 逻辑：选近期突破布林带上轨的强势股（龙头），追涨买入，跌破中轨止损

import numpy as np


def init(context):
    context.stocksnum = 8
    context.period = 20
    context.stock_list = []
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=0))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=0))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context, bar_dict):
    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 2e9]
        df = df[df['market_cap'] < 50e9]
        df = df.head(context.stocksnum * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, context.period + 5, '1d', 'close')
            if closes is None or len(closes) < context.period:
                continue
            closes = np.array(closes, dtype=float)
            ma = np.mean(closes[-context.period:])
            std = np.std(closes[-context.period:])
            upper = ma + 2 * std
            # 突破上轨
            if closes[-1] > upper:
                result.append(stock)
        except Exception:
            continue

    context.stock_list = result[:context.stocksnum * 2]


def market_open_trade(context, bar_dict):
    target = []
    for stock in context.stock_list:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stocksnum:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def after_market_close(context, bar_dict):
    # 跌破布林带中轨止损
    for stock in list(context.portfolio.positions.keys()):
        try:
            closes = history_bars(stock, context.period + 1, '1d', 'close')
            if closes is None or len(closes) < context.period:
                continue
            closes = np.array(closes, dtype=float)
            ma = np.mean(closes[-context.period:])
            if closes[-1] < ma:
                order_target_value(stock, 0)
        except Exception:
            continue
