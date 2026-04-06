# SG-MS-PEG-HL 成长小市值PEG策略 - RiceQuant版本
# 原文：分享几个截止2022年3月仍有效的策略
# 来源：聚宽社区 rq_09
# 逻辑：筛选成长性好（净利润增速高）、小市值、低PEG的股票，结合52周高低点，月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    instruments_df = all_instruments('CS')
    all_stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in all_stocks if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap', 'peg_ratio', 'inc_net_profit_year_on_year', 'inc_revenue_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 60.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 2e+10]
        df = df[df['inc_net_profit_year_on_year'] > 0.05]
        df = df[df['inc_revenue_year_on_year'] > 0.1]
        df = df[df['inc_net_profit_year_on_year'] > 0]
        df = df[df['peg_ratio'] > 0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 52周高低点过滤
    scored = []
    for stock in candidates:
        try:
            highs = history_bars(stock, 252, '1d', 'high')
            lows = history_bars(stock, 252, '1d', 'low')
            closes = history_bars(stock, 252, '1d', 'close')
            if highs is None or lows is None or closes is None or len(highs) < 20:
                continue
            high_52w = np.max(highs)
            low_52w = np.min(lows)
            cur_close = closes[-1]
            if high_52w <= low_52w:
                continue
            hl_ratio = (cur_close - low_52w) / (high_52w - low_52w)
            scored.append((stock, hl_ratio))
        except Exception:
            continue

    if not scored:
        return

    scored.sort(key=lambda x: x[1], reverse=True)
    target = []
    for stock, _ in scored:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
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
