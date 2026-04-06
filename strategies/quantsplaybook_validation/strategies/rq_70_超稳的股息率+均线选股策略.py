# 超稳股息率+均线选股策略 - RiceQuant版本
# 逻辑：dividend_ratio>3% + 价格在MA20上方 + pb<3，月度调仓

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
            ['pb_ratio', 'market_cap', 'dividend_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 3.0]
        df = df[df['market_cap'] > 2e+09]
        df = df[df['dividend_ratio'] > 0.0300]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 均线过滤：价格在MA20上方
    target = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            closes = np.array(closes, dtype=float)
            ma20 = np.mean(closes[-20:])
            if closes[-1] > ma20:
                bar = (bar_dict[stock] if stock in bar_dict else None)
                if bar is not None and bar.is_trading:
                    target.append(stock)
        except Exception:
            continue
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)