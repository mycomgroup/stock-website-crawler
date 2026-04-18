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


# 234板介入策略 - RiceQuant版本
# 原文：234板介入-2023年14倍-无未来
# 逻辑：选近期有连续涨停（2-4板）记录的股票，在回调时介入

import numpy as np


def init(context):
    context.stock_num = 3
    context.candidates = []
    scheduler.run_daily(get_stock_list, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_all, time_rule=market_open(minute=5))
    scheduler.run_daily(sell_lt, time_rule=market_open(minute=232))


def handle_bar(context, bar_dict):
    pass


def count_consecutive_limit_up(closes):
    """统计最近的连续涨停板数"""
    count = 0
    for i in range(len(closes) - 1, 0, -1):
        if closes[i] / closes[i-1] >= 1.095:
            count += 1
        else:
            break
    return count


def get_stock_list(context, bar_dict):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8', '3'))]

    try:
        factor_df = get_factor(stocks, ['market_cap'])
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        df = df[(df['market_cap'] > 5) & (df['market_cap'] < 50)]
        df = df.sort_values('market_cap')
        pool = df.index.tolist()[:300]
    except Exception:
        pool = stocks[:300]

    candidates = []
    for stock in pool:  # FIX: was undefined variable pool
        try:
            closes = history_bars(stock, 10, '1d', 'close')
            if closes is None or len(closes) < 10:
                continue
            closes = np.array(closes, dtype=float)

            # 近5日内有2-4连板记录
            total_limit_ups = sum(1 for i in range(1, min(6, len(closes)))
                                  if closes[-i] / closes[-i-1] >= 1.095)

            if 2 <= total_limit_ups <= 4:
                bar = (bar_dict[stock] if stock in bar_dict else None)
                if bar is None or bar.is_trading:
                    candidates.append(stock)
        except Exception:
            continue

    context.candidates = candidates[:context.stock_num * 3]


def buy_all(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        # 低开介入（开盘价低于昨收）
        closes = history_bars(stock, 2, '1d', 'close')
        if closes is None or len(closes) < 2:
            continue
        if bar.open <= closes[-2] * 1.02:  # 开盘不超涨2%
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


def sell_lt(context, bar_dict):
    """尾盘止损"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        avg_cost = getattr(pos, 'avg_cost', getattr(pos, 'avg_price', 0))
        loss = bar.close / avg_cost - 1 if avg_cost > 0 else 0
        if loss < -0.06:
            order_target_value(stock, 0)
