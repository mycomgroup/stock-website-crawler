# 原文链接：https://www.joinquant.com/post/65000
# 策略：搭建量化交易模型从零开始择时选股仓位管理和因子分析
# 核心逻辑：量化模型框架，包含择时（MACD）+选股（多因子）+仓位管理（等权）的完整流程。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def calc_boll(p, n=20, k=2):
    ma = np.mean(p[-n:])
    std = np.std(p[-n:])
    return ma + k * std, ma, ma - k * std

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:])
    y = np.array(high[-n:])
    b = np.polyfit(x, y, 1)
    return b[0]

# ============ 择时模块 ============
def market_timing(index_etf='510300.XSHG'):
    """MACD择时：返回True表示可以持股"""
    closes = history_bars(index_etf, 60, '1d', 'close')
    if closes is None or len(closes) < 40:
        return True  # 数据不足时默认持股
    dif, dea, macd = calc_macd(closes)
    return dif[-1] > dea[-1]

# ============ 仓位管理模块 ============
def position_sizing(total_value, n_stocks):
    """等权仓位管理"""
    if n_stocks == 0:
        return 0
    return total_value * 0.95 / n_stocks


# ============ 策略主体 ============
def init(context):
    context.n_stocks = 10
    context.index_etf = '510300.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度调仓：MACD择时 + 多因子选股 + 等权仓位"""
    # 步骤1：择时
    if not market_timing(context.index_etf):
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        logger.info("MACD择时：空仓")
        return

    # 步骤2：选股
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    q = query(
        fundamentals.eod_derivative_indicator.market_cap,
        fundamentals.eod_derivative_indicator.pe_ratio,
        fundamentals.financial_indicator.roe,
    ).filter(
        fundamentals.eod_derivative_indicator.order_book_id.in_(stocks),
        fundamentals.eod_derivative_indicator.pe_ratio > 0,
        fundamentals.eod_derivative_indicator.pe_ratio < 50,
        fundamentals.financial_indicator.roe > 0.08,
    ).order_by(
        fundamentals.eod_derivative_indicator.market_cap.asc()
    ).limit(context.n_stocks + 10)

    df = get_fundamentals(q, entry_date=context.now.date())
    if df is None or len(df) == 0:
        return

    # 步骤3：因子分析打分
    df['cap_rank'] = df['market_cap'].rank(ascending=False)
    df['pe_rank']  = df['pe_ratio'].rank(ascending=False)
    df['roe_rank'] = df['roe'].rank(ascending=True)
    df['total_score'] = df['cap_rank'] + df['pe_rank'] + df['roe_rank']
    df = df.sort_values('total_score', ascending=False)
    target = list(df.index)[:context.n_stocks]

    # 步骤4：仓位管理
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    if n == 0:
        return
    value = position_sizing(context.portfolio.total_value, n)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)

    logger.info(f"量化框架调仓完成 | 择时=持股 | 选股={target[:3]}... | 单股仓位={value:.0f}")
