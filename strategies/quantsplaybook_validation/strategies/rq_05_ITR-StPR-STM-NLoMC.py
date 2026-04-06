# ITR-StPR-STM-NLoMC 多因子策略 - RiceQuant版本
# 因子：资产周转率(ITR) + 短期反转(StPR) + 20日动量(STM) + 中等市值(NLoMC)
# 逻辑：选中等市值、资产效率高、短期反转+动量共振的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8'))]

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=-1).last().dropna()
        df = df[df['market_cap'] > 5e+09]
        df = df[df['market_cap'] < 5e+10]
        df = df[df['roa'] > 0.03]
        df = df.sort_values(['roa', 'market_cap'], ascending=[False, True]).head(context.stock_num * 10)
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 25, '1d', 'close')
            if closes is None or len(closes) < 25:
                continue
            closes = np.array(closes, dtype=float)
            stm = closes[-1] / closes[-20] - 1
            stpr = -(closes[-20] / closes[0] - 1)
            roa = df.loc[stock, 'roa'] if stock in df.index else 0
            scores[stock] = stm * 0.35 + stpr * 0.25 + (roa / 100) * 0.4
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]
    if not target:
        target = sorted_stocks[:context.stock_num]

    if not target:
        return
    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
