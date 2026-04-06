# 三阳三阴战法 - RiceQuant版本
# 逻辑：选近期出现三连阳（连续3根阳线）的股票，月度调仓

import numpy as np

def init(context):
    context.stock_num = 15
    context.month = -1
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]
    factor_df = get_factor(
        stocks,
        ['market_cap']
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    if not hasattr(df, 'columns'):
        df = df.to_frame(name='market_cap')
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 50000000000]
    df = df.sort_values('market_cap').head(200)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 6, '1d', 'close')
            opens = history_bars(stock, 6, '1d', 'open')
            if closes is None or opens is None or len(closes) < 4:
                continue
            closes = np.array(closes, dtype=float)
            opens = np.array(opens, dtype=float)
            if all(closes[-i] > opens[-i] for i in range(1, 4)):
                result.append(stock)
        except Exception:
            continue

    target = [s for s in result if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
