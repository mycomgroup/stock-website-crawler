# 韶华研究之二十_竞价异动策略 - RiceQuant版本
# 逻辑：选开盘价相对昨收有明显跳空（>2%）且成交量放大的股票，日度交易

import numpy as np


def init(context):
    context.stock_num = 5
    context.candidates = []
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(stop_loss, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def update_pool(context, bar_dict):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    stocks = stock_ids

    try:
        factor_df = get_factor(stocks, ['market_cap'])
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[(df['market_cap'] > 10) & (df['market_cap'] < 200)]
        df = df.sort_values('market_cap')
        pool = df.index.tolist()[:300]
    except Exception:
        pool = stocks[:300]

    candidates = []
    for stock in pool:
        try:
            closes = history_bars(stock, 6, '1d', 'close')
            volumes = history_bars(stock, 6, '1d', 'volume')
            if closes is None or volumes is None or len(closes) < 6:
                continue
            closes = np.array(closes, dtype=float)
            volumes = np.array(volumes, dtype=float)
            # 量比放大（今日成交量 > 5日均量的1.5倍）
            vol_ratio = volumes[-1] / (np.mean(volumes[-6:-1]) + 1e-10)
            if vol_ratio > 1.5:
                candidates.append(stock)
        except Exception:
            continue

    context.candidates = candidates[:context.stock_num * 3]


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        closes = history_bars(stock, 2, '1d', 'close')
        if closes is None or len(closes) < 2:
            continue
        # 跳空高开（开盘价高于昨收2%以上）
        gap = bar.open / closes[-2] - 1
        if gap > 0.02:
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
