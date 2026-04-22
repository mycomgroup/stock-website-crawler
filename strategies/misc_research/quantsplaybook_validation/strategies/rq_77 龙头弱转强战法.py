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


# 龙头弱转强战法 - RiceQuant版本
# 原文：龙头弱转强战法
# 逻辑：选近期有涨停（龙头）后出现弱转强信号（低开后拉升）的股票

import numpy as np


def init(context):
    context.stock_num = 5
    context.candidates = []
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=5))
    scheduler.run_daily(check_stop, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context, bar_dict):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8', '3'))]

    # Get small-cap stocks via fundamentals (market_cap in 亿元)
    try:
        factor_df = get_factor(
            stocks,
            ['market_cap']
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            pool = stocks[:300]
        else:
            if not hasattr(df, 'columns'):
                df = df.to_frame(name='market_cap')
            if 'market_cap' not in df.columns:
                return
            df = df[(df['market_cap'] > 10) & (df['market_cap'] < 100)]
            df = df.sort_values('market_cap').head(500)
            pool = df.index.tolist()
    except Exception:
        pool = stocks[:300]

    candidates = []
    for stock in pool:
        try:
            closes = history_bars(stock, 8, '1d', 'close')
            if closes is None or len(closes) < 8:
                continue
            closes = np.array(closes, dtype=float)
            # 近5日有涨停
            has_limit = any(closes[-i] / closes[-i-1] >= 1.095 for i in range(1, 6))
            if not has_limit:
                continue
            # 昨日收盘在5日均线附近（弱转强前的整理）
            ma5 = np.mean(closes[-5:])
            if 0.95 <= closes[-1] / ma5 <= 1.05:
                candidates.append(stock)
        except Exception:
            continue

    context.candidates = candidates[:context.stock_num * 3]


def market_open_trade(context, bar_dict):
    if not context.candidates:
        return

    # 弱转强：开盘低开但快速拉升（用开盘价判断）
    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        closes = history_bars(stock, 2, '1d', 'close')  # FIX: was undefined variable s
        if closes is None or len(closes) < 2:
            continue
        # 低开（开盘低于昨收2%以内）
        if bar.open >= closes[-2] * 0.98:
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


def check_stop(context, bar_dict):
    """止损：跌幅超过5%"""
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
