# 龙头首阴战法改版二 - RiceQuant版本
# 逻辑：选近期有涨停（龙头）后出现首阴（第一根阴线）的股票，低开介入

import numpy as np


def _build_stock_pool(min_cap=10, max_cap=100, max_size=500):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8', '3'))]
    try:
        factor_df = get_factor(stocks, ['market_cap'])
        if factor_df is None or len(factor_df) == 0:
            return stocks[:max_size]
        df = factor_df.groupby(level=0).last().dropna()
        if not hasattr(df, 'columns'):
            df = df.to_frame(name='market_cap')
        if 'market_cap' not in df.columns:
            return stocks[:max_size]
        df = df[(df['market_cap'] > min_cap) & (df['market_cap'] < max_cap)]
        df = df.sort_values('market_cap').head(max_size)
        return df.index.tolist()
    except Exception:
        return stocks[:max_size]


def _limit_up_count(bars):
    count = 0
    for row in bars:
        limit_up = float(row['limit_up']) if row['limit_up'] is not None else 0
        close = float(row['close'])
        if limit_up > 0 and close >= limit_up * 0.995:
            count += 1
    return count


def init(context):
    context.stock_num = 3
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
    pool = _build_stock_pool(min_cap=10, max_cap=120, max_size=500)
    result = []
    for stock in pool:
        try:
            bars = history_bars(stock, 10, '1d', ['open', 'close', 'high', 'low', 'limit_up'])
            if bars is None or len(bars) < 8:
                continue
            recent_bars = bars[-8:]
            limit_ups = _limit_up_count(recent_bars)
            if limit_ups < 2 or limit_ups > 6:
                continue
            latest = recent_bars[-1]
            prev = recent_bars[-2]
            latest_open = float(latest['open'])
            latest_close = float(latest['close'])
            latest_high = float(latest['high'])
            latest_low = float(latest['low'])
            latest_limit = float(latest['limit_up']) if latest['limit_up'] is not None else 0
            prev_close = float(prev['close'])
            bearish_first_pullback = (
                latest_close < latest_high * 0.985 and
                latest_close >= prev_close * 0.99 and
                latest_open >= latest_high * 0.99
            )
            hammer_rebound = (
                latest_limit > 0 and
                latest_close >= latest_limit * 0.995 and
                latest_open < latest_high * 0.96 and
                latest_low < prev_close * 0.93
            )
            if bearish_first_pullback or hammer_rebound:
                score = limit_ups * 10 + latest_close / max(prev_close, 1e-6)
                result.append((score, stock))
        except Exception:
            continue

    result.sort(key=lambda item: item[0], reverse=True)
    context.candidates = [stock for _, stock in result[:context.stock_num * 12]]
    context.last_week_date = today_key


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        daily = history_bars(stock, 2, '1d', ['close', 'limit_up'])
        if daily is None or len(daily) < 2:
            continue
        prev_close = float(daily[-1]['close'])
        prev_limit = float(daily[-1]['limit_up']) if daily[-1]['limit_up'] is not None else 0
        today_limit = getattr(bar, 'limit_up', None)
        last_price = getattr(bar, 'close', None)
        if today_limit is None or last_price is None:
            continue
        breakout_buy = (
            prev_limit > 0 and
            last_price > prev_limit * 0.99 and
            last_price > prev_close * 1.03 and
            bar.open > prev_close * 1.01 and
            last_price < today_limit * 0.995
        )
        limit_extension_buy = (
            prev_limit > 0 and
            abs(prev_close - prev_limit) / prev_limit < 0.005 and
            last_price > prev_limit * 1.05 and
            bar.open > prev_limit * 0.95 and
            last_price < today_limit * 0.995
        )
        if breakout_buy or limit_extension_buy:
            target.append(stock)
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


def stop_loss(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        avg_cost = getattr(pos, 'avg_cost', getattr(pos, 'avg_price', 0))
        if avg_cost > 0 and bar.close / avg_cost - 1 < -0.06:
            order_target_value(stock, 0)
