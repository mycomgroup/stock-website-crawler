# 原文链接：https://www.joinquant.com/post/RSRS择时货币基金6年8倍行业周期股策略
# 策略：RSRS择时+货币基金--6年8倍行业周期股策略
# 核心逻辑：行业周期股+RSRS择时，RSRS>阈值时持股，否则切换到货币基金ETF(511880)。

import numpy as np

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:]); y = np.array(high[-n:])
    b = np.polyfit(x, y, 1); return b[0]

def init(context):
    context.n_stocks = 10
    context.money_etf = '511880.XSHG'  # 货币基金ETF
    context.index_etf = '510300.XSHG'
    context.rsrs_threshold = 1.0
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # RSRS择时
    try:
        high = history_bars(context.index_etf, 20, '1d', 'high')
        low = history_bars(context.index_etf, 20, '1d', 'low')
        rsrs = calc_rsrs(high, low, 18)
    except Exception:
        rsrs = 1.0

    if rsrs < context.rsrs_threshold:
        # 切换到货币基金
        for s in list(context.portfolio.positions.keys()):
            if s != context.money_etf:
                order_target_value(s, 0)
        order_target_value(context.money_etf, context.portfolio.total_value * 0.95)
        logger.info(f"RSRS={rsrs:.2f}<{context.rsrs_threshold}，切换货币基金")
        return

    # 选行业周期股：低PE + 高ROE + 中等市值
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 25.0]
    df = df[df['roe'] > 0.12]
    df = df[df['market_cap'] > 3000000000]
    df = df[df['market_cap'] < 50000000000]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]

    # 清仓货币基金
    if context.money_etf in context.portfolio.positions:
        order_target_value(context.money_etf, 0)

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"RSRS={rsrs:.2f}，持股模式，持仓: {target}")
