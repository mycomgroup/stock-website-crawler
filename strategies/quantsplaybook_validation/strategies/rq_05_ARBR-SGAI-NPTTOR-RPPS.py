# ARBR-SGAI-NPTTOR-RPPS 多因子策略 - RiceQuant版本
# 因子：价格动量(ARBR) + 营收增速(SGAI) + 净利润率(NPTTOR) + EPS(RPPS)
# 逻辑：综合动量、成长、盈利质量、每股收益多因子选股，月度调仓

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
            ['market_cap', 'pe_ratio', 'net_profit_margin', 'inc_net_profit_year_on_year', 'eps'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=-1).last().dropna()
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['net_profit_margin'] > 0.05]
        df = df[df['inc_net_profit_year_on_year'] > 0.05]
        df = df.sort_values(['inc_net_profit_year_on_year', 'net_profit_margin', 'eps'], ascending=[False, False, False]).head(context.stock_num * 10)
        candidates = df.index.tolist()
    except Exception:
        return
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            momentum = closes[-1] / closes[0] - 1
            npm = df.loc[stock, 'net_profit_margin'] if stock in df.index else 0
            eps = df.loc[stock, 'eps'] if stock in df.index else 0
            growth = df.loc[stock, 'inc_net_profit_year_on_year'] if stock in df.index else 0
            scores[stock] = momentum * 0.3 + (npm / 100) * 0.25 + (eps / 10) * 0.2 + (growth / 100) * 0.25
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
