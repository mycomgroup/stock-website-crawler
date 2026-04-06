# MACD多周期共振策略 - RiceQuant版本
# 逻辑：计算日线MACD，选MACD金叉且在零轴上方的股票，月度调仓

import numpy as np


def ema(prices, period):
    result = np.zeros_like(prices, dtype=float)
    result[0] = prices[0]
    k = 2.0 / (period + 1)
    for i in range(1, len(prices)):
        result[i] = prices[i] * k + result[i-1] * (1 - k)
    return result


def calc_macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal:
        return None, None
    dif = ema(closes, fast) - ema(closes, slow)
    dea = ema(dif, signal)
    return dif, dea


def init(context):
    context.stock_num = 15
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
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
        df = df[df['market_cap'] > 2e+09]
        df = df[df['market_cap'] < 5e+10]
        df = df[df['pb_ratio'] > 0.0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 60, '1d', 'close')
            if closes is None or len(closes) < 40:
                continue
            closes = np.array(closes, dtype=float)
            dif, dea = calc_macd(closes)
            if dif is None:
                continue
            if dif[-1] > dea[-1] and dif[-2] <= dea[-2] and dif[-1] > 0:
                result.append(stock)
        except Exception:
            continue

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
