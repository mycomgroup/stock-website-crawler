# 原文链接：https://www.joinquant.com/post/64001
# 策略：基于XGBoost_6m滚动选股全A小市值开板止盈策略
# 核心逻辑：用多因子评分替代XGBoost，小市值+低PE+高ROE，6个月滚动调仓，开板止盈。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.take_profit = 0.20  # 20%止盈
    context.stop_loss = 0.10   # 10%止损
    context.entry_prices = {}
    # 6个月滚动调仓（每月调仓）
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(check_profit_loss, time_rule=market_open(minute=60))

def handle_bar(context, bar_dict):
    pass

def check_profit_loss(context, bar_dict):
    """开板止盈/止损检查"""
    for s, entry in list(context.entry_prices.items()):
        if s in bar_dict and entry > 0:
            price = bar_dict[s].close
            pnl = (price - entry) / entry
            if pnl >= context.take_profit:
                order_target_value(s, 0)
                context.entry_prices.pop(s, None)
                logger.info(f"止盈触发: {s}，盈利={pnl:.2%}")
            elif pnl <= -context.stop_loss:
                order_target_value(s, 0)
                context.entry_prices.pop(s, None)
                logger.info(f"止损触发: {s}，亏损={pnl:.2%}")

def rebalance(context, bar_dict):
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
    df = df[df['pe_ratio'] < 50.0]
    df = df[df['roe'] > 0.08]
    df = df.head(100)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    # 多因子评分（替代XGBoost）
    df['cap_rank'] = df['market_cap'].rank(ascending=False)
    df['pe_rank'] = df['pe_ratio'].rank(ascending=False)
    df['roe_rank'] = df['roe'].rank(ascending=True)
    df['score'] = df['cap_rank'] + df['pe_rank'] + df['roe_rank']
    df = df.sort_values('score', ascending=False)
    target = list(df.index)[:context.n_stocks]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)
            context.entry_prices.pop(s, None)

    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
            context.entry_prices[s] = bar_dict[s].close
    logger.info(f"XGBoost替代多因子调仓，持仓: {target}")
