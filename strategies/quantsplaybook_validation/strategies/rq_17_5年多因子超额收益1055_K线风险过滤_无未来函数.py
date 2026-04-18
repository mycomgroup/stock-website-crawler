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


# 5年多因子超额收益+K线风险过滤 - RiceQuant版本
# 逻辑：ROE+PB+动量多因子选股，加入K线风险过滤（近期大阴线过滤），月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
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
            ['pb_ratio', 'market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 5.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['roe'] > 0.08]
        df = df[df['inc_net_profit_year_on_year'] > 0]
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            opens = history_bars(stock, 5, '1d', 'open')
            if closes is None or opens is None or len(closes) < 21 or len(opens) < 5:
                continue
            closes = np.array(closes, dtype=float)
            opens = np.array(opens, dtype=float)

            # K线风险过滤：近5日有大阴线（跌幅>5%）则跳过
            has_big_drop = any((closes[-i] - opens[-i]) / opens[-i] < -0.05 for i in range(1, 6))
            if has_big_drop:
                continue

            momentum = closes[-1] / closes[0] - 1
            roe = df.loc[stock, 'roe'] if stock in df.index else 0
            pb = df.loc[stock, 'pb_ratio'] if stock in df.index else 5
            growth = df.loc[stock, 'inc_net_profit_year_on_year'] if stock in df.index else 0
            scores[stock] = momentum * 0.3 + (roe / 100) * 0.4 - (pb / 10) * 0.1 + (growth / 100) * 0.2
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]

    if not target:
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
