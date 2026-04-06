# PNF-TPtCR-ITR 价值+质量策略 - RiceQuant版本
# 因子：低PB(PNF代理) + 高ROE(TPtCR) + 资产周转率(ITR/ROA代理)
# 逻辑：价值+质量组合，低PB高ROE高ROA，月度调仓

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
            ['pb_ratio', 'market_cap', 'roe', 'roa'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=-1).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 5.0]
        df = df[df['market_cap'] > 2e+09]
        df = df[df['roe'] > 0.10]
        df = df[df['roa'] > 0.05]
        df = df.sort_values(['pb_ratio', 'roe', 'roa'], ascending=[True, False, False]).head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    target = [s for s in candidates if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]
    if not target:
        target = candidates[:context.stock_num]

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
