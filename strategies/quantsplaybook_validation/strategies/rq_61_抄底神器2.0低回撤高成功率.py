# 抄底神器2.0 - RiceQuant版本
# 原文：抄底神器2.0，低回撤，高成功率
# 逻辑：选市值适中、PE低、近期大幅下跌的超跌股，等待反弹

import numpy as np


def init(context):
    context.stock_num = 5
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=-1).last().dropna()
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 40.0]
        df = df[df['market_cap'] > 500000000]
        df = df[df['market_cap'] < 50000000000]
        if df is None or len(df) == 0:
            return
        df = df.sort_values(['market_cap', 'pe_ratio']).head(context.stock_num * 10)
        candidates = list(df.index)
    except Exception:
        return
    # 选近20日跌幅最大的超跌股
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            drawdown = closes[-1] / closes[0] - 1
            if drawdown < -0.15:  # 跌幅超过15%才考虑
                scores[stock] = drawdown
        except Exception:
            continue

    if not scores:
        return

    # 跌幅最大的（最超跌）
    sorted_stocks = sorted(scores, key=scores.get)
    target = []
    for stock in sorted_stocks:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
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
