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


# WY大神龙头打板策略小改 - RiceQuant版本
# 逻辑：选近期有涨停的小市值股票，MACD金叉时买入

import numpy as np


def ema(prices, period):
    result = np.zeros_like(prices, dtype=float)
    result[0] = prices[0]
    k = 2.0 / (period + 1)
    for i in range(1, len(prices)):
        result[i] = prices[i] * k + result[i-1] * (1 - k)
    return result


def init(context):
    context.stock_num = 5
    context.candidates = []
    context.last_week_date = None
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(stop_loss, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def update_pool(context, bar_dict):
    today_key = context.now.strftime('%Y-%m-%d')
    if today_key == context.last_week_date:
        return

    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    all_stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8', '3'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 10]
        df = df[df['market_cap'] < 100]
        df = df.sort_values('market_cap')
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 40, '1d', 'close')
            if closes is None or len(closes) < 40:
                continue
            closes = np.array(closes, dtype=float)
            has_limit = any(closes[-i] / closes[-i-1] >= 1.095 for i in range(1, 6))
            if not has_limit:
                continue
            dif = ema(closes, 12) - ema(closes, 26)
            dea = ema(dif, 9)
            if dif[-1] > dea[-1] and dif[-2] <= dea[-2]:
                result.append(stock)
        except Exception:
            continue

    context.candidates = result[:context.stock_num * 3]
    context.last_week_date = today_key


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = [s for s in context.candidates if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def stop_loss(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        if bar.close / pos.avg_cost - 1 < -0.06:
            order_target_value(stock, 0)
