# 原文链接：https://www.joinquant.com/post/最适合上班族的策略神奇公式策略
# 策略：最适合上班族的策略-神奇公式策略
# 核心逻辑：格林布拉特神奇公式（高EBIT/EV + 高ROC），选排名前20的股票，年度调仓。

import numpy as np

def init(context):
    context.n_stocks = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 神奇公式：EBIT/EV（盈利收益率）+ ROC（资本回报率）
    # 用EV/EBITDA的倒数近似EBIT/EV，用ROE近似ROC
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
    df = df[df['roe'] > 0.05]
    df = df[df['market_cap'] > 1000000000]
    df = df.head(300)
    candidates = df.index.tolist()
    if df.empty:
        return

    # 神奇公式排名：EBIT/EV排名 + ROC排名
    df['ebit_ev_score'] = df['pe_ratio'].rank(ascending=True)   # EV/EBITDA越低，EBIT/EV越高
    df['roc_score'] = df['roe'].rank(ascending=False)  # ROE越高越好
    df['magic_score'] = df['ebit_ev_score'] + df['roc_score']
    df = df.sort_values('magic_score', ascending=True)
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
    logger.info(f"神奇公式选股完成，持仓: {target}")
