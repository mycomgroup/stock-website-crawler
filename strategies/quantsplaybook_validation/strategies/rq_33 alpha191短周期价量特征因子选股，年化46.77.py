# 原文链接：https://www.joinquant.com/post/alpha191短周期价量特征因子选股年化46.77
# 策略：alpha191短周期价量特征因子选股，年化46.77
# 核心逻辑：用alpha191因子中的价量相关性因子（近20日价格与成交量相关系数）选股，选相关性最低的股票。

import numpy as np

def init(context):
    context.n_stocks = 20
    context.corr_n = 20  # 计算相关系数的窗口
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def calc_price_volume_corr(stock, n):
    """计算价量相关系数（alpha191因子）"""
    try:
        closes = history_bars(stock, n, '1d', 'close')
        volumes = history_bars(stock, n, '1d', 'volume')
        if len(closes) < n or len(volumes) < n:
            return None
        corr = np.corrcoef(closes, volumes)[0, 1]
        return corr
    except Exception:
        return None

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 先用基本面过滤
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 60.0]
    df = df[df['market_cap'] > 1000000000]
    df = df.head(200)
    candidates = df.index.tolist()
    candidates = list(df.index)

    # 计算价量相关系数，选相关性最低的（量价背离，价涨量缩）
    corr_list = []
    for s in candidates:
        corr = calc_price_volume_corr(s, context.corr_n)
        if corr is not None:
            corr_list.append((s, corr))

    # 相关系数越低越好（价涨量缩，主力控盘）
    corr_list.sort(key=lambda x: x[1])
    target = [s for s, _ in corr_list[:context.n_stocks]]

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
    logger.info(f"alpha191价量相关性选股完成，持仓: {target}")
