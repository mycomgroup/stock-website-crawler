# 韶华研究之十六指数增强 - RiceQuant版本
# 原文：韶华研究之十六，指数增强
# 逻辑：在中证500成分股中，用多因子（动量+价值+质量）做指数增强，周度调仓

import numpy as np

def _ols_beta_r2(x, y):
    """Pure numpy OLS: returns (beta, r2)"""
    xm, ym = x.mean(), y.mean()
    ss_xx = ((x - xm) ** 2).sum()
    if ss_xx == 0:
        return None, None
    beta = ((x - xm) * (y - ym)).sum() / ss_xx
    y_hat = ym + beta * (x - xm)
    ss_res = ((y - y_hat) ** 2).sum()
    ss_tot = ((y - ym) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r2



def init(context):
    context.index = '000905.XSHG'
    context.stock_num = 30
    context.week_day = -1
    scheduler.run_daily(rebalance_trade, time_rule=market_open(minute=0))


def handle_bar(context, bar_dict):
    pass


def rebalance_trade(context, bar_dict):
    # 每周调仓一次
    week = context.now.isocalendar()[1]
    if week == context.week_day:
        return
    context.week_day = week

    stocks = index_components(context.index)
    if not stocks or len(stocks) < 10:
        return

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['roe'] > 0.00]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 动量因子
    momentum_scores = {}
    for stock in df.index:
        try:
            closes = history_bars(stock, 61, '1d', 'close')
            if closes is None or len(closes) < 61:
                continue
            momentum_scores[stock] = closes[-1] / closes[0] - 1
        except Exception:
            continue

    if not momentum_scores:
        return

    # 综合评分
    scores = {}
    for stock in momentum_scores:
        if stock not in df.index:
            continue
        mom = momentum_scores[stock]
        roe = df.loc[stock, 'roe'] if 'roe' in df.columns else 0
        pb = df.loc[stock, 'pb_ratio'] if 'pb_ratio' in df.columns else 5
        growth = df.loc[stock, 'inc_net_profit_year_on_year'] if 'inc_net_profit_year_on_year' in df.columns else 0
        scores[stock] = mom * 0.3 + (roe / 100) * 0.4 + (growth / 100) * 0.3 - (pb / 10) * 0.1

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
