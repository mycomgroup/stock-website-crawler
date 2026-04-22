# ETF日内动量策略 - RiceQuant版本
# 来源：《另类ETF交易策略：日内动量》
# 核心逻辑：基于噪声区域突破的日内动量，使用分钟K线信号
# 注：原版使用分钟数据，RiceQuant日频版本用日内开盘价偏离度近似
#
# ⚠️ 未来函数修复说明：
#    原版用当天的 open/close 计算动量信号并在当天交易，存在未来函数风险
#    （当天收盘价尚未确定时无法知道信号方向）。
#    修复后改用前一天（bars[-2]）的 open/close 生成信号，决定今天的操作，
#    确保信号在交易时点已完全确定，无未来函数问题。

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
    opens = history_bars(security, context.lookback + 2, '1d', 'open')
    closes = history_bars(security, context.lookback + 2, '1d', 'close')
    highs = history_bars(security, context.lookback + 2, '1d', 'high')
    lows = history_bars(security, context.lookback + 2, '1d', 'low')
    if opens is None or closes is None or len(opens) < context.lookback + 1:
        return

    # 用日线近似：计算过去N天的日内波动（|close-open| / open）作为噪声基准
    daily_moves = np.abs(closes[:-2] / opens[:-2] - 1)
    noise_upper = np.mean(daily_moves) * context.threshold

    # 使用昨天（bars[-2]）的数据生成信号，决定今天的操作
    prev_open = opens[-2]
    prev_close = closes[-2]
    prev_move = (prev_close - prev_open) / prev_open

    # 突破噪声上边界：做多信号
    if prev_move > noise_upper and not context.pos:
        order_target_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: prev_move={prev_move:.4f}, noise={noise_upper:.4f}")

    # 突破噪声下边界：平仓信号
    elif prev_move < -noise_upper and context.pos:
        order_target_value(security, 0)
        context.pos = False
        print(f"卖出: prev_move={prev_move:.4f}, noise={noise_upper:.4f}")
