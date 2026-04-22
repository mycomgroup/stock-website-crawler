# 原文链接：https://www.joinquant.com/post/低代码迁移成本的实盘方案jqtrade+one quant
# 策略：低代码迁移成本的实盘方案：jqtrade+one quant
# 核心逻辑：简单的沪深300成分股等权持有策略，季度调仓，低换手率。

import numpy as np

def init(context):
    context.n_stocks = 30
    context.index_code = '000300.XSHG'
    # 季度调仓：每季度第一个交易日
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    context.rebalance_months = [1, 4, 7, 10]  # 季度月份

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 只在季度月份调仓
    current_month = context.now.month
    if current_month not in context.rebalance_months:
        return

    # 获取沪深300成分股
    hs300 = index_components(context.index_code)

    # 选高ROE低PE的优质成分股
    prev_date = context.now.date()
    factor_df = get_factor(
        hs300,
        ['pe_ratio', 'pb_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 40.0]
    df = df[df['roe'] > 0.1]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()
    target = list(df.index)[:context.n_stocks]

    if not target:
        return

    # 等权持有
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"季度调仓完成（{current_month}月），等权持有{n}只沪深300成分股")
