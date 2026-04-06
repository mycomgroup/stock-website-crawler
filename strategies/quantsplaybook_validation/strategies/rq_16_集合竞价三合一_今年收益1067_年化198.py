# 集合竞价三合一策略 - RiceQuant版本
# 逻辑：选近期有涨停、低开、量比放大的小市值股票，日度交易

import numpy as np


def _build_stock_pool(min_cap=20, max_cap=500, max_size=600):
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


def init(context):
    context.stock_num = 3
    context.candidates = []
    context.last_update_day = None
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(stop_loss, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def update_pool(context, bar_dict):
    today_key = context.now.strftime('%Y-%m-%d')
    if today_key == context.last_update_day:
        return
    pool = _build_stock_pool(min_cap=20, max_cap=520, max_size=600)
    result = []
    for stock in pool:
        try:
            bars = history_bars(stock, 6, '1d', ['open', 'close', 'volume', 'limit_up'])
            if bars is None or len(bars) < 5:
                continue
            latest = bars[-1]
            prev = bars[-2]
            latest_close = float(latest['close'])
            latest_limit = float(latest['limit_up']) if latest['limit_up'] is not None else 0
            if latest_limit <= 0 or latest_close < latest_limit * 0.995:
                continue
            prior_limit_hits = sum(
                1 for row in bars[-4:-1]
                if row['limit_up'] is not None and float(row['close']) >= float(row['limit_up']) * 0.995
            )
            if prior_limit_hits > 1:
                continue
            closes = np.array([float(row['close']) for row in bars], dtype=float)
            volumes = np.array([float(row['volume']) for row in bars], dtype=float)
            price_change = closes[-1] / max(closes[-4], 1e-6) - 1
            if price_change > 0.28:
                continue
            if latest_close < float(latest['open']) * 0.95:
                continue
            vol_ratio = volumes[-1] / (np.mean(volumes[-4:-1]) + 1e-10)
            if vol_ratio < 1.2:
                continue
            score = vol_ratio + latest_close / max(float(prev['close']), 1e-6)
            result.append((score, stock))
        except Exception:
            continue

    result.sort(key=lambda item: item[0], reverse=True)
    context.candidates = [stock for _, stock in result[:context.stock_num * 15]]
    context.last_update_day = today_key


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
        if prev_limit <= 0 or abs(prev_close - prev_limit) / prev_limit >= 0.005:
            continue
        open_ratio = bar.open / max(prev_close, 1e-6)
        last_ratio = bar.close / max(prev_close, 1e-6)
        if (
            0.955 <= open_ratio <= 1.06 and
            last_ratio > open_ratio and
            last_ratio > 0.98
        ):
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
        if avg_cost > 0 and bar.close / avg_cost - 1 < -0.05:
            order_target_value(stock, 0)
