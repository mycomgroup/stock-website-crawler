# 原文链接：https://www.joinquant.com/post/跟着基金报团174回撤7.33
# 策略：跟着基金报团！！！174%  回撤  7.33%
# 核心逻辑：选基金重仓股（沪深300成分股中高ROE低PE），跟随机构持仓，季度调仓。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.index_code = '000300.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 从沪深300成分股中选高ROE低PE的机构重仓股
    hs300 = index_components(context.index_code)
    prev_date = context.now.date()
    factor_df = get_factor(
        hs300,
        ['pe_ratio', 'pb_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 35.0]
    df = df[df['roe'] > 0.15]
    df = df[df['pb_ratio'] > 0.0]
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
    logger.info(f"基金报团股调仓完成，持仓: {target}")
