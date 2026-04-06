# 原文链接：https://www.joinquant.com/post/回撤二波2.0透过一次过拟合的机器学习摸底策略的收益上限
# 策略：【回撤二波2.0】透过一次过拟合的机器学习摸底策略的收益上限
# 核心逻辑：用MACD+BOLL+动量三因子组合信号，控制最大回撤，月度调仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def calc_boll(p, n=20, k=2):
    ma = np.mean(p[-n:]); std = np.std(p[-n:])
    return ma + k * std, ma, ma - k * std

def init(context):
    context.n_stocks = 15
    context.bond_etf = '511010.XSHG'
    context.index_etf = '510300.XSHG'
    context.max_drawdown_threshold = 0.10  # 最大回撤阈值10%
    context.peak_value = 0
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(check_drawdown, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def check_drawdown(context, bar_dict):
    """监控回撤，超过阈值时清仓"""
    current_value = context.portfolio.total_value
    if current_value > context.peak_value:
        context.peak_value = current_value
    if context.peak_value > 0:
        drawdown = (context.peak_value - current_value) / context.peak_value
        if drawdown > context.max_drawdown_threshold:
            for s in list(context.portfolio.positions.keys()):
                order_target_value(s, 0)
            order_target_value(context.bond_etf, current_value * 0.95)
            logger.info(f"回撤{drawdown:.2%}超过阈值，清仓切换债券")

def rebalance(context, bar_dict):
    # 大盘MACD信号
    prices = history_bars(context.index_etf, 40, '1d', 'close')
    if len(prices) < 30:
        return
    dif, dea, macd = calc_macd(prices)
    upper, mid, lower = calc_boll(prices, 20, 2)
    current_price = prices[-1]

    # 三因子信号：MACD金叉 + 价格在布林中轨以上 + 近20日动量为正
    momentum = (prices[-1] - prices[-21]) / prices[-21] if len(prices) >= 21 else 0
    signal_score = 0
    if macd[-1] > 0:
        signal_score += 1
    if current_price > mid:
        signal_score += 1
    if momentum > 0:
        signal_score += 1

    if signal_score < 2:
        # 信号弱，持债
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info(f"三因子信号={signal_score}，持债")
        return

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
    df = df[df['pe_ratio'] < 40.0]
    df = df[df['roe'] > 0.1]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]

    if context.bond_etf in context.portfolio.positions:
        order_target_value(context.bond_etf, 0)
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
    logger.info(f"三因子信号={signal_score}，持股: {target}")
