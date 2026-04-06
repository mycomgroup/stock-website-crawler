# 龙虎榜挖掘V2.0策略 - RiceQuant版本
# 逻辑：用近期涨停+成交量放大代替龙虎榜数据，选近5日有涨停且量比>2的小市值股票

import numpy as np


def init(context):
    context.stock_num = 5
    context.candidates = []
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(stop_loss, time_rule=market_open(minute=225))


def handle_bar(context, bar_dict):
    pass


def update_pool(context, bar_dict):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8', '3'))]

    try:
        factor_df = get_factor(stocks, ['market_cap'])
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[(df['market_cap'] > 5) & (df['market_cap'] < 100)]
        df = df.sort_values('market_cap')
        pool = df.index.tolist()[:300]
    except Exception:
        pool = stocks[:300]

    candidates = []
    for stock in pool:  # FIX: was undefined variable pool
        try:
            closes = history_bars(stock, 8, '1d', 'close')
            volumes = history_bars(stock, 8, '1d', 'volume')
            if closes is None or volumes is None or len(closes) < 8:
                continue
            closes = np.array(closes, dtype=float)
            volumes = np.array(volumes, dtype=float)
            # 近5日有涨停
            has_limit = any(closes[-i] / closes[-i-1] >= 1.095 for i in range(1, 6))
            if not has_limit:
                continue
            # 量比>2
            vol_ratio = volumes[-1] / (np.mean(volumes[-6:-1]) + 1e-10)
            if vol_ratio > 2.0:
                candidates.append((stock, vol_ratio))
        except Exception:
            continue

    candidates.sort(key=lambda x: x[1], reverse=True)
    context.candidates = [s for s, _ in candidates[:context.stock_num * 3]]


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
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
