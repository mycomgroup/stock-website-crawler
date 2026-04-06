# 基本面01加RSI择时 - RiceQuant版本
# 原文：基本面01加RSI择时
# 逻辑：选低PB、高ROE的基本面优质股，结合RSI择时（RSI超卖时买入）

import numpy as np


def calc_rsi(closes, period=14):
    """计算RSI指标"""
    if len(closes) < period + 1:
        return 50.0
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def init(context):
    context.stock_num = 10
    context.month = -1
    context.index = '000300.XSHG'


def handle_bar(context, bar_dict):
    # RSI择时：大盘RSI < 40 时才买入
    index_closes = history_bars(context.index, 30, '1d', 'close')
    if index_closes is None or len(index_closes) < 20:
        return
    index_rsi = calc_rsi(np.array(index_closes, dtype=float))

    # 大盘RSI超卖（<40）或已持仓时继续持有
    if index_rsi > 70 and context.portfolio.positions:
        # 大盘超买，清仓
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    if index_rsi > 65:
        return  # 大盘过热，不买入

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 4.0]
        df = df[df['market_cap'] > 3e+09]
        df = df[df['roe'] > 0.10]
        df = df[df['roa'] > 0.05]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 个股RSI过滤：选个股RSI < 50 的（相对超卖）
    target = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 30, '1d', 'close')
            if closes is None or len(closes) < 20:
                continue
            rsi = calc_rsi(np.array(closes, dtype=float))
            if rsi < 55:
                bar = (bar_dict[stock] if stock in bar_dict else None)
                if bar is not None and bar.is_trading:
                    target.append(stock)
        except Exception:
            continue
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)