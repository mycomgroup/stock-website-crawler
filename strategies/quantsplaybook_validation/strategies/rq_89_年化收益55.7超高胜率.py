# 年化收益55.7%超高胜率策略 - RiceQuant版本
# 原文：年化收益55.7%，超高胜率0.799
# 逻辑：多因子选股 + 大盘择时，选高ROE、低PB、近期动量强的股票

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
    context.stock_num = 10
    context.hold_cycle = 20
    context.day_count = 0
    scheduler.run_daily(fun_main, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def fun_main(context, bar_dict):
    context.day_count += 1
    if context.day_count % context.hold_cycle != 0:
        # 日内止损检查
        for stock in list(context.portfolio.positions.keys()):
            pos = context.portfolio.positions.get(stock)
            if pos is None:
                continue
            bar = (bar_dict[stock] if stock in bar_dict else None)
            if bar is None:
                continue
            if bar.close / pos.avg_cost - 1 < -0.08:
                order_target_value(stock, 0)
        return

    # 大盘择时
    index_closes = history_bars('000300.XSHG', 60, '1d', 'close')
    if index_closes is None or len(index_closes) < 60:
        return
    ma20 = np.mean(index_closes[-20:])
    ma60 = np.mean(index_closes[-60:])
    if index_closes[-1] < ma20 and ma20 < ma60:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 5.0]
        df = df[df['market_cap'] > 2e+09]
        df = df[df['market_cap'] < 5e+10]
        df = df[df['roe'] > 0.10]
        df = df[df['inc_net_profit_year_on_year'] > 0.05]
        candidates = df.index.tolist()
    except Exception:
        return
    # 动量因子
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            momentum = closes[-1] / closes[0] - 1
            roe = df.loc[stock, 'roe'] if stock in df.index and 'roe' in df.columns else 0
            pb = df.loc[stock, 'pb_ratio'] if stock in df.index and 'pb_ratio' in df.columns else 5
            scores[stock] = momentum * 0.4 + (roe / 100) * 0.4 - (pb / 10) * 0.2
        except Exception:
            continue

    if not scores:
        return

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
