# 韶华研究之一_布林突破+均线金叉 - RiceQuant版本
# 逻辑：布林带上轨突破 + MA5/MA20金叉，月度调仓

import numpy as np


def init(context):
    context.stock_num = 15
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
            ['pb_ratio', 'market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 2e+09]
        df = df[df['market_cap'] < 5e+10]
        df = df[df['pb_ratio'] > 0.0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 25, '1d', 'close')
            if closes is None or len(closes) < 25:
                continue
            closes = np.array(closes, dtype=float)
            ma5 = np.mean(closes[-5:])
            ma20 = np.mean(closes[-20:])
            std20 = np.std(closes[-20:])
            upper = ma20 + 2 * std20
            # 布林上轨突破 + MA5>MA20金叉
            if closes[-1] > upper and ma5 > ma20:
                result.append(stock)
        except Exception:
            continue

    target = [s for s in candidates if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
