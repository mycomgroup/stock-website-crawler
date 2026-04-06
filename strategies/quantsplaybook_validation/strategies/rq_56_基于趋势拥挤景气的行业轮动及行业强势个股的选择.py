# 原文链接：https://www.joinquant.com/post/56002
# 策略：基于趋势拥挤景气的行业轮动及行业强势个股的选择
# 核心逻辑：行业轮动，选近期涨幅最强的行业ETF，在强势行业中选基本面好的个股。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.industry_etfs = {
        '512010.XSHG': '军工',
        '512800.XSHG': '银行',
        '512880.XSHG': '证券',
        '515030.XSHG': '新能源',
        '159915.XSHE': '创业板',
        '159928.XSHE': '消费',
        '512760.XSHG': '芯片',
        '515700.XSHG': '新能源车',
    }
    context.n_stocks = 5
    context.momentum_days = 20
    context.top_etf = None
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 选最强行业ETF
    etf_scores = {}
    for etf in context.industry_etfs:
        try:
            closes = history_bars(etf, context.momentum_days + 1, '1d', 'close')
            if closes is not None and len(closes) >= context.momentum_days + 1:
                etf_scores[etf] = (closes[-1] - closes[0]) / closes[0]
        except Exception:
            continue

    if not etf_scores:
        return

    best_etf = max(etf_scores, key=etf_scores.get)
    best_mom = etf_scores[best_etf]

    if best_mom < 0:
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        logger.info("行业动量为负，空仓")
        return

    # 在强势行业中选基本面好的个股（用沪深300成分股代替）
    stocks = index_components('000300.XSHG')
    stocks = [s for s in stocks if not s.startswith('688')]
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
    if df is None or len(df) == 0:
        return

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
    logger.info(f"行业轮动选股，强势行业={context.industry_etfs.get(best_etf)}，持仓: {target}")
