# 原文链接：https://www.joinquant.com/post/错杀反弹掌握人性规律
# 策略：错杀反弹，掌握人性规律，开启投资新纪元
# 核心逻辑：选近期大幅下跌（超跌）但基本面良好（低PE高ROE）的股票，等待反弹。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.drop_threshold = -0.20  # 近20日跌幅超过20%视为超跌
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 获取基本面良好的股票
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 30.0]
    df = df[df['roe'] > 0.1]
    df = df[df['market_cap'] > 1000000000]
    df = df.head(200)
    candidates = df.index.tolist()
    candidates = list(df.index)

    # 筛选近20日超跌股票
    oversold = []
    for s in candidates:
        try:
            prices = history_bars(s, 21, '1d', 'close')
            if len(prices) < 21:
                continue
            ret = (prices[-1] - prices[0]) / prices[0]
            if ret < context.drop_threshold:
                oversold.append((s, ret))
        except Exception:
            continue

    # 按跌幅排序，选跌幅最大的（最超跌）
    oversold.sort(key=lambda x: x[1])
    target = [s for s, _ in oversold[:context.n_stocks]]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    if n == 0:
        logger.info("无超跌股票，空仓等待")
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"超跌反弹选股完成，持仓: {target}")
