# 原文链接：https://www.joinquant.com/post/44880
# 策略：截止到21年12月依然有效的小市值适配因子
# 作者：因子研究员
# 核心逻辑：小市值+低换手率选股，月度调仓
# 注：原版用jqfactor，此处改为用市值+换手率因子

import numpy as np


def calc_turnover(stock, n=20):
    """计算近N日平均换手率"""
    volumes = history_bars(stock, n, '1d', 'volume')
    # 用成交量的变异系数近似换手率稳定性
    if volumes is None or len(volumes) < n:
        return None
    v = np.array(volumes, dtype=float)
    if np.mean(v) < 1e-9:
        return None
    return np.mean(v)  # 返回平均成交量作为换手率代理


def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：小市值+低换手率"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]

    # 先用基本面筛选小市值
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df.head(100)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    small_cap_stocks = list(df.index)

    # 在小市值中选低换手率（低成交量）的股票
    turnover_dict = {}
    for s in small_cap_stocks:
        t = calc_turnover(s, 20)
        if t is not None:
            turnover_dict[s] = t

    if not turnover_dict:
        return

    # 按换手率升序（低换手率优先）
    sorted_stocks = sorted(turnover_dict.keys(), key=lambda x: turnover_dict[x])
    context.stock_pool = sorted_stocks[:context.n_stocks]
    logger.info(f"[小市值适配因子] 选股={context.stock_pool}")

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
