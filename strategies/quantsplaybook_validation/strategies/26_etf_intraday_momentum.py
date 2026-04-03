# ETF日内动量策略 - RiceQuant版本
# 来源：《另类ETF交易策略：日内动量》
# 核心逻辑：基于噪声区域突破的日内动量，使用分钟K线信号
# 注：原版使用分钟数据，RiceQuant日频版本用日内开盘价偏离度近似

import numpy as np


def init(context):
    # 沪深300ETF
    context.security = '510300.XSHG'
    context.lookback = 14       # 噪声区域计算窗口（天）
    context.threshold = 1.5     # 突破倍数阈值
    context.pos = False


def handle_bar(context, bar_dict):
    security = context.security

    # 获取历史日线数据
    bars = history_bars(security, context.lookback + 2, '1d',
                        ['open', 'close', 'high', 'low'])
    if bars is None or len(bars) < context.lookback + 1:
        return

    # 用日线近似：计算过去N天的日内波动（high-open / open）作为噪声基准
    daily_moves = np.abs(bars['close'][:-1] / bars['open'][:-1] - 1)
    noise_upper = np.mean(daily_moves) * context.threshold

    today_open = bars['open'][-1]
    today_close = bars['close'][-1]
    today_move = (today_close - today_open) / today_open

    # 突破噪声上边界：做多信号
    if today_move > noise_upper and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: move={today_move:.4f}, noise={noise_upper:.4f}")

    # 突破噪声下边界：平仓信号
    elif today_move < -noise_upper and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: move={today_move:.4f}, noise={noise_upper:.4f}")
