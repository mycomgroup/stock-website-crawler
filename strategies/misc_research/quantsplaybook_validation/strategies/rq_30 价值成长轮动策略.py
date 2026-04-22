# 原文链接：https://www.joinquant.com/post/价值成长轮动策略
# 策略：价值成长轮动策略
# 核心逻辑：价值股（低PE低PB）和成长股（高营收增长）轮动，根据市场动量切换，月度调仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.etf_bond = '511010.XSHG'
    context.index_code = '000300.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 判断市场动量：用沪深300近20日涨跌幅
    prices = history_bars(context.index_code, 21, '1d', 'close')
    momentum = (prices[-1] - prices[0]) / prices[0]

    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    if momentum > 0:
        # 市场上涨：选成长股（高ROE + 低PE）
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 50.0]
        df = df[df['roe'] > 0.1]
        df = df.head(context.n_stocks + 10)
        candidates = df.index.tolist()
        df = df[df['pb_ratio'] < 2.0]
        df = df.head(context.n_stocks + 10)
        candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]

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
    logger.info(f"动量={momentum:.2%}，模式={'成长' if momentum>0 else '价值'}，持仓: {target}")
