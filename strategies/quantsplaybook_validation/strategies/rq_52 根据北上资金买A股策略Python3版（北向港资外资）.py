# 原文链接：https://www.joinquant.com/post/52xxx
# 策略：根据北上资金买A股策略Python3版（北向港资外资）
# 核心逻辑：选沪深港通标的中近期涨幅强+基本面好（低PE高ROE）的股票，月度调仓

import numpy as np

HOLD_NUM = 10
MOMENTUM_DAYS = 20

def init(context):
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    # 沪深港通标的（用沪深300代理）
    stocks = index_components('000300.XSHG')

    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 25]
    df = df[df['roe'] > 0.12]
    df = df.head(100)
    if df.empty:
        return

    # 计算动量
    momentum = {}
    for stock in df.index.tolist():
        try:
            closes = history_bars(stock, MOMENTUM_DAYS + 1, '1d', 'close')
            if len(closes) >= MOMENTUM_DAYS + 1:
                momentum[stock] = (closes[-1] - closes[0]) / closes[0]
        except Exception:
            momentum[stock] = 0

    df['momentum'] = df.index.to_series().map(momentum).fillna(0)
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True, pct=True)
    df['roe_rank'] = df['roe'].rank(ascending=False, pct=True)
    df['mom_rank'] = df['momentum'].rank(ascending=False, pct=True)
    df['score'] = df['pe_rank'] * 0.3 + df['roe_rank'] * 0.3 + df['mom_rank'] * 0.4
    df = df.sort_values('score', ascending=False)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入北向标的 {stock}")
