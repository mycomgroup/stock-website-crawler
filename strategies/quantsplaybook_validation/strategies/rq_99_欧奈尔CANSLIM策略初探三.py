# 欧奈尔CANSLIM策略初探三 - RiceQuant版本
# 原文：欧奈尔CANSLIM策略初探三
# 逻辑：CANSLIM核心要素：C(当季EPS增速)、A(年度EPS增速)、N(新高)、S(小市值)、L(强者)、I(机构)、M(大盘)
# 用RiceQuant可用的因子近似实现

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    # M: 大盘择时（沪深300均线）
    index_closes = history_bars('000300.XSHG', 60, '1d', 'close')
    if index_closes is None or len(index_closes) < 60:
        return
    if index_closes[-1] < np.mean(index_closes[-60:]):
        # 大盘弱势，清仓
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
            ['pe_ratio', 'market_cap', 'roe', 'inc_net_profit_year_on_year'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 50.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['inc_net_profit_year_on_year'] > 0.2]
        df = df[df['roe'] > 0.10]
        candidates = df.index.tolist()
    except Exception:
        return
    # N: 价格接近52周新高（强者恒强）
    scores = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 252, '1d', 'close')
            if closes is None or len(closes) < 60:
                continue
            closes = np.array(closes, dtype=float)
            high_52w = np.max(closes)
            cur = closes[-1]
            # 接近新高（在高点的90%以上）
            hl_ratio = cur / high_52w
            if hl_ratio < 0.85:
                continue
            # 近20日动量
            momentum = closes[-1] / closes[-20] - 1 if len(closes) >= 20 else 0
            growth = df.loc[stock, 'inc_net_profit_year_on_year'] if stock in df.index else 0
            scores[stock] = hl_ratio * 0.4 + momentum * 0.3 + (growth / 100) * 0.3
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
