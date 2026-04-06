# 原文链接：https://www.joinquant.com/post/52xxx
# 策略：机器学习滚动训练价投策略
# 核心逻辑：滚动窗口多因子评分（替代ML），用近期因子表现动态调整权重，价值投资选股

import numpy as np

HOLD_NUM = 10
WINDOW = 3  # 滚动窗口（月）

def init(context):
    context.factor_weights = {'pe': 1.0, 'pb': 1.0, 'roe': 1.0}
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def update_factor_weights(context):
    """根据近期持仓表现动态调整因子权重（简化版滚动训练）"""
    # 简化：根据市场状态调整权重
    try:
        closes = history_bars('000300.XSHG', 60, '1d', 'close')
        if len(closes) < 60:
            return
        recent_ret = (closes[-1] - closes[-20]) / closes[-20]
        if recent_ret > 0.05:
            # 上涨市：动量权重提升
            context.factor_weights = {'pe': 0.8, 'pb': 0.8, 'roe': 1.4}
        elif recent_ret < -0.05:
            # 下跌市：价值权重提升
            context.factor_weights = {'pe': 1.4, 'pb': 1.4, 'roe': 0.8}
        else:
            context.factor_weights = {'pe': 1.0, 'pb': 1.0, 'roe': 1.0}
    except Exception:
        pass

def rebalance(context, bar_dict):
    update_factor_weights(context)

    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pe_ratio', 'pb_ratio', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] < 2e10]
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 40]
    df = df[df['pb_ratio'] > 0]
    df = df[df['roe'] > 0.08]
    df = df.head(200)
    if df.empty:
        return

    w = context.factor_weights
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True, pct=True) * w['pe']
    df['pb_rank'] = df['pb_ratio'].rank(ascending=True, pct=True) * w['pb']
    df['roe_rank'] = df['roe'].rank(ascending=False, pct=True) * w['roe']
    df['score'] = df['pe_rank'] + df['pb_rank'] + df['roe_rank']
    df = df.sort_values('score', ascending=False)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}，权重 {w}")
