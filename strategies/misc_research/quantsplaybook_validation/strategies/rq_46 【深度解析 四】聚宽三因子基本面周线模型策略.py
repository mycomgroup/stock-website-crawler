# 原文链接：https://www.joinquant.com/post/深度解析四聚宽三因子基本面周线模型策略
# 策略：【深度解析 四】聚宽三因子基本面周线模型策略
# 核心逻辑：三因子模型（市值+账面市值比+动量），周线级别调仓，选因子暴露最优的股票。

import numpy as np

def init(context):
    context.n_stocks = 20
    context.momentum_n = 20
    scheduler.run_weekly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 三因子：市值（SMB）+ 账面市值比（HML）+ 动量
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'pb_ratio', 'market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 500000000]
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 80.0]
    df = df.head(300)
    candidates = df.index.tolist()
    if df.empty:
        return

    # SMB因子：小市值
    df['smb_score'] = df['market_cap'].rank(ascending=True, pct=True)
    # HML因子：高账面市值比（低PB）
    df['hml_score'] = df['pb_ratio'].rank(ascending=True, pct=True)

    # 动量因子
    mom_dict = {}
    for s in df.index:
        try:
            p = history_bars(s, context.momentum_n + 1, '1d', 'close')
            if len(p) > context.momentum_n:
                mom_dict[s] = (p[-1] - p[0]) / p[0]
        except Exception:
            mom_dict[s] = 0.0

    df['momentum'] = df.index.map(lambda s: mom_dict.get(s, 0.0))
    df['mom_score'] = df['momentum'].rank(ascending=False, pct=True)

    # 三因子等权综合评分
    df['total_score'] = (df['smb_score'] + df['hml_score'] + df['mom_score']) / 3
    df = df.sort_values('total_score', ascending=False)
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
    logger.info(f"三因子周线模型调仓完成，持仓: {target}")
