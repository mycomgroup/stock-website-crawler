# 原文链接：https://www.joinquant.com/post/45310
# 策略：人工智能强化学习DQN交易智能体（回馈社区公开训练代码）
# 作者：AI量化
# 核心逻辑：用近期动量信号（N日涨幅）作为DQN的简化替代，选强势股
# 注：原版用DQN强化学习，此处改为简单动量策略代替

import numpy as np


def init(context):
    context.n_stocks = 5
    context.lookback = 20   # 动量回看期
    context.stock_pool = []
    scheduler.run_monthly(select_stocks, tradingday=1, time_rule=market_open(minute=5))
    scheduler.run_daily(momentum_trade, time_rule=market_open(minute=20))


def handle_bar(context, bar_dict):
    pass


def select_stocks(context, bar_dict):
    """月度选股：中证500成分股"""
    stocks = index_components('000905.XSHG')
    context.stock_pool = [s for s in stocks if not s.startswith('688')]
    logger.info(f"[DQN替代] 股票池大小={len(context.stock_pool)}")


def momentum_trade(context, bar_dict):
    """日度动量交易（DQN简化替代）"""
    if not context.stock_pool:
        return

    # 计算各股动量
    momentum = {}
    for s in context.stock_pool[:200]:  # 限制数量
        prices = history_bars(s, context.lookback + 1, '1d', 'close')
        if prices is None or len(prices) < context.lookback:
            continue
        p = np.array(prices, dtype=float)
        ret = p[-1] / p[0] - 1
        # 额外：近5日动量
        ret5 = p[-1] / p[-6] - 1 if len(p) >= 6 else ret
        momentum[s] = ret * 0.6 + ret5 * 0.4

    if not momentum:
        return

    # 选动量最强的前N只
    sorted_stocks = sorted(momentum.keys(), key=lambda x: momentum[x], reverse=True)
    target = sorted_stocks[:context.n_stocks]

    # 卖出不在目标中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    # 买入目标股票
    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)

    logger.info(f"[DQN替代] 持仓={target[:3]}... 动量={[round(momentum[s]*100,1) for s in target[:3]]}%")
