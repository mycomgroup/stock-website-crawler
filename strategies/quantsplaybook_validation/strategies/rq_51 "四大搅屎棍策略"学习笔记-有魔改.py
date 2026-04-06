# 原文链接：https://www.joinquant.com/post/35000
# 策略："四大搅屎棍策略"学习笔记-有魔改
# 核心逻辑：四大因子（市值+PE+PB+动量）等权打分，选综合评分最高的股票，月度调仓

import numpy as np


def init(context):
    context.n_stocks = 10
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]

    # 获取财务数据
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'pb_ratio', 'market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 100.0]
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 20000000000]
    df = df.head(300)
    candidates = df.index.tolist()
    if df is None or len(df) < context.n_stocks:
        return

    # 四因子打分（越小越好：市值、PE、PB；动量越大越好）
    df['cap_rank'] = df['market_cap'].rank(ascending=True)
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True)
    df['pb_rank'] = df['pb_ratio'].rank(ascending=True)

    # 动量因子：近20日涨幅
    mom = {}
    for s in df.index[:100]:
        try:
            bars = history_bars(s, 21, '1d', 'close')
            if bars is not None and len(bars) >= 21:
                mom[s] = (bars[-1] - bars[0]) / (bars[0] + 1e-9)
        except Exception:
            mom[s] = 0.0

    df['momentum'] = df.index.map(lambda x: mom.get(x, 0.0))
    df['mom_rank'] = df['momentum'].rank(ascending=False)

    # 等权综合评分
    df['score'] = df['cap_rank'] + df['pe_rank'] + df['pb_rank'] + df['mom_rank']
    df = df.sort_values('score', ascending=True)
    target = list(df.index[:context.n_stocks])

    # 卖出不在目标中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    # 等权买入
    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)

    logger.info(f"[四大搅屎棍] 调仓完成，持仓: {target}")
