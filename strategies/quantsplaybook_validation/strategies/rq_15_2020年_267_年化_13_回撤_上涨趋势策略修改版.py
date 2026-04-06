# 2020年267%年化13%回撤上涨趋势策略修改版 - RiceQuant版本
# 逻辑：大盘上涨趋势时持有小市值股票，趋势转弱时切换到债券ETF

import numpy as np


def init(context):
    context.stock_num = 20
    context.bond_etf = '511010.XSHG'
    context.index = '000300.XSHG'
    context.month = -1
    context.in_stock = False


def handle_bar(context, bar_dict):
    # 趋势判断：MA20 > MA60
    idx_closes = history_bars(context.index, 65, '1d', 'close')
    if idx_closes is None or len(idx_closes) < 65:
        return
    idx_closes = np.array(idx_closes, dtype=float)
    ma20 = np.mean(idx_closes[-20:])
    ma60 = np.mean(idx_closes[-60:])
    uptrend = ma20 > ma60 and idx_closes[-1] > ma20

    if not uptrend:
        if context.in_stock:
            for stock in list(context.portfolio.positions.keys()):
                if stock != context.bond_etf:
                    order_target_value(stock, 0)
            bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
            if bar is not None and bar.is_trading:
                order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
            context.in_stock = False
        return

    current_month = context.now.month
    if current_month == context.month:
        return

    # 清仓债券ETF
    if context.bond_etf in context.portfolio.positions:
        order_target_value(context.bond_etf, 0)

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
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 3e8]
        df = df[df['market_cap'] < 8e+09]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
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
    context.in_stock = True
