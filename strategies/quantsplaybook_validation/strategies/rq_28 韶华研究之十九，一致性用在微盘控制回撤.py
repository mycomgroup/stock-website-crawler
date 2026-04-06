# 原文链接：https://www.joinquant.com/post/45400
# 策略：韶华研究之十九，一致性用在微盘控制回撤
# 作者：韶华研究
# 核心逻辑：微盘股+一致性风控（持仓股票涨跌一致性过滤），控制回撤

import numpy as np


def calc_consistency(stocks, n=5):
    """计算持仓股票近N日涨跌一致性（同涨同跌的比例）"""
    if not stocks:
        return 1.0
    directions = []
    for s in stocks:
        prices = history_bars(s, n + 1, '1d', 'close')
        if prices is None or len(prices) < n:
            continue
        p = np.array(prices, dtype=float)
        ret = p[-1] / p[0] - 1
        directions.append(1 if ret > 0 else -1)
    if not directions:
        return 1.0
    d = np.array(directions)
    # 一致性：同方向的比例
    pos_ratio = np.sum(d > 0) / len(d)
    neg_ratio = np.sum(d < 0) / len(d)
    return max(pos_ratio, neg_ratio)


def init(context):
    context.n_stocks = 20
    context.stock_pool = []
    context.consistency_threshold = 0.7  # 一致性阈值
    scheduler.run_monthly(select_stocks, tradingday=1, time_rule=market_open(minute=5))
    scheduler.run_daily(risk_control, time_rule=market_open(minute=20))


def handle_bar(context, bar_dict):
    pass


def select_stocks(context, bar_dict):
    """月度选微盘股"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()
    if df is not None and len(df) > 0:
        context.stock_pool = list(df.index)[:context.n_stocks]
    logger.info(f"[微盘一致性] 股票池={len(context.stock_pool)}")

    # 初始建仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)


def risk_control(context, bar_dict):
    """日度一致性风控"""
    held = list(context.portfolio.positions.keys())
    if not held:
        return

    consistency = calc_consistency(held, n=3)
    logger.info(f"[微盘一致性] 一致性={consistency:.2f}")

    if consistency < context.consistency_threshold:
        # 一致性低（分化严重），减仓50%
        for s in held:
            pos = context.portfolio.positions.get(s)
            if pos is not None:
                current_val = pos.market_value
                order_target_value(s, current_val * 0.5)
        logger.info("[微盘一致性] 一致性低，减仓50%")
    else:
        # 一致性高，维持满仓
        n = len(context.stock_pool)
        if n == 0:
            return
        value = context.portfolio.total_value * 0.95 / n
        for s in context.stock_pool:
            if s in bar_dict and bar_dict[s].is_trading:
                order_target_value(s, value)
