# 别人"拿的住"的股票最赚钱 - RiceQuant版本
# 原文：别人"拿的住"的股票最赚钱
# 逻辑：选换手率低（持股稳定）、ROE高、市值适中的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
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
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 5e+09]
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 5.0]
        df = df[df['roe'] > 0.10]
        candidates = df.index.tolist()
    except Exception:
        return
    # 换手率稳定性：用成交量波动率代理（波动率低 = 持股稳定）
    scores = {}
    for stock in candidates:
        try:
            volumes = history_bars(stock, 60, '1d', 'volume')
            if volumes is None or len(volumes) < 60:
                continue
            vol_cv = np.std(volumes) / (np.mean(volumes) + 1e-10)  # 变异系数
            roe = df.loc[stock, 'roe'] if stock in df.index and 'roe' in df.columns else 0
            # 换手率稳定（低CV）且ROE高
            scores[stock] = roe / 100 - vol_cv * 0.5
        except Exception:
            continue

    if not scores:
        return

    context.month = current_month

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = []
    for stock in sorted_stocks:
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
